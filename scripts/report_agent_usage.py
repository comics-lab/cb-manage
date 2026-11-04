#!/usr/bin/env python3
"""Generate redaction-safe Markdown and JSON agent-usage reports."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from validate_agent_ledger import V2_TASK_REQUIRED, load_jsonl


def clean(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def count_field(records: list[dict[str, object]], field: str) -> dict[str, int]:
    counts = Counter(str(record[field]) for record in records if record.get(field))
    return dict(sorted(counts.items()))


def summarize_usage(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {"available": False, "record_count": 0}
    records, errors = load_jsonl(path)
    dimensions = (
        "input_tokens", "cached_input_tokens", "output_tokens",
        "reasoning_tokens", "total_tokens",
    )
    totals: dict[str, int] = {}
    for dimension in dimensions:
        totals[dimension] = sum(
            value for record in records
            if isinstance((value := record.get(dimension)), int)
        )
    return {
        "available": True,
        "record_count": len(records),
        "parse_errors": errors,
        "totals": totals,
        "sources": count_field(records, "source"),
        "note": "Usage totals are accounting records, not necessarily provider billing.",
    }


def build_report(
    records: list[dict[str, object]], *, ledger: Path, usage_ledger: Path
) -> dict[str, object]:
    visible_records = [
        {key: value for key, value in record.items() if key != "_line"}
        for record in records
    ]
    tasks: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for record in visible_records:
        session_id = record.get("session_id")
        task_id = record.get("task_id")
        if isinstance(session_id, str) and isinstance(task_id, str):
            tasks[(session_id, task_id)].append(record)

    assessments: list[dict[str, object]] = []
    for (session_id, task_id), task_records in sorted(tasks.items()):
        event_types = {str(record.get("event_type")) for record in task_records}
        declarations = [
            record for record in task_records
            if record.get("event_type") == "governance_declared"
        ]
        declaration = declarations[-1] if declarations else {}
        decisions = [
            record for record in task_records
            if record.get("event_type") == "decision_recorded"
        ]
        is_v2 = any(record.get("schema_version") == 2 for record in task_records)
        missing = sorted(V2_TASK_REQUIRED - event_types) if is_v2 else []
        assessments.append({
            "session_id": session_id,
            "task_id": task_id,
            "schema_version": 2 if is_v2 else 1,
            "governance_status": declaration.get("governance_status", "missing"),
            "actual_agent": declaration.get("actual_agent"),
            "actual_skills": declaration.get("actual_skills", []),
            "actual_contracts": declaration.get("actual_contracts", []),
            "decision_count": len(decisions),
            "event_count": len(task_records),
            "missing_lifecycle_events": missing,
            "complete": is_v2 and not missing,
        })

    decisions = [
        record for record in visible_records
        if record.get("event_type") == "decision_recorded"
    ]
    v2_tasks = [task for task in assessments if task["schema_version"] == 2]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "event_ledger": str(ledger),
        "record_count": len(visible_records),
        "session_count": len({record.get("session_id") for record in visible_records}),
        "task_count": len(assessments),
        "v2_task_count": len(v2_tasks),
        "complete_v2_task_count": sum(bool(task["complete"]) for task in v2_tasks),
        "event_counts": count_field(visible_records, "event_type"),
        "agent_counts": count_field(visible_records, "agent"),
        "skill_counts": count_field(visible_records, "skill"),
        "contract_counts": count_field(visible_records, "contract"),
        "governance_status_counts": dict(sorted(Counter(
            str(task["governance_status"]) for task in assessments
        ).items())),
        "decision_type_counts": count_field(decisions, "decision_type"),
        "decision_governance_counts": count_field(decisions, "governance_status"),
        "tasks": assessments,
        "usage": summarize_usage(usage_ledger),
        "redaction": (
            "Aggregates and identifiers only; no prompts, tool content, SQL, PII, "
            "credentials, or hidden reasoning."
        ),
    }


def markdown_report(report: dict[str, object]) -> str:
    lines = [
        "# Agent Usage Tracking Report",
        "",
        f"> Generated: {clean(report['generated_at'])}",
        "> Status: observational metadata; not a provider billing statement.",
        "",
        "## Summary",
        "",
        f"- Event records: {report['record_count']}",
        f"- Sessions: {report['session_count']}",
        f"- Tasks: {report['task_count']}",
        f"- Schema-v2 tasks: {report['v2_task_count']}",
        f"- Complete schema-v2 tasks: {report['complete_v2_task_count']}",
        "",
    ]
    for heading, key in (
        ("Event Counts", "event_counts"),
        ("Agent Counts", "agent_counts"),
        ("Skill Counts", "skill_counts"),
        ("Contract Counts", "contract_counts"),
        ("Governance Status", "governance_status_counts"),
        ("Decision Types", "decision_type_counts"),
        ("Decision Governance", "decision_governance_counts"),
    ):
        lines.extend([f"## {heading}", "", "| Value | Count |", "| --- | ---: |"])
        values = report[key]
        if isinstance(values, dict) and values:
            lines.extend(f"| {clean(name)} | {count} |" for name, count in values.items())
        else:
            lines.append("| none | 0 |")
        lines.append("")

    lines.extend([
        "## Task Coverage",
        "",
        "| Session | Task | Governance | Decisions | Complete | Missing lifecycle events |",
        "| --- | --- | --- | ---: | --- | --- |",
    ])
    tasks = report["tasks"]
    if isinstance(tasks, list) and tasks:
        for task in tasks:
            if task["schema_version"] == 1:
                missing = "legacy schema; lifecycle not assessed"
                complete = "n/a"
            else:
                missing = ", ".join(task["missing_lifecycle_events"]) or "none"
                complete = "yes" if task["complete"] else "no"
            lines.append(
                f"| {clean(task['session_id'])} | {clean(task['task_id'])} | "
                f"{clean(task['governance_status'])} | {task['decision_count']} | "
                f"{complete} | {clean(missing)} |"
            )
    else:
        lines.append("| none | none | missing | 0 | no | no tracked tasks |")

    usage = report["usage"]
    lines.extend(["", "## Usage", ""])
    if isinstance(usage, dict) and usage.get("available"):
        lines.append(f"- Usage records: {usage['record_count']}")
        totals = usage.get("totals", {})
        if isinstance(totals, dict):
            for name, total in totals.items():
                lines.append(f"- {name}: {total}")
        lines.append("- These totals are not necessarily provider billing.")
    else:
        lines.append("No usage ledger is available; token and cost totals are unpriced/unknown.")
    lines.extend(["", f"Redaction: {report['redaction']}", ""])
    return "\n".join(lines)


def generate_reports(ledger: Path, usage_ledger: Path, output_dir: Path) -> dict[str, object]:
    records, errors = load_jsonl(ledger)
    if errors:
        raise ValueError("; ".join(errors))
    report = build_report(records, ledger=ledger, usage_ledger=usage_ledger)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "agent-usage-latest.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "agent-usage-latest.md").write_text(
        markdown_report(report), encoding="utf-8"
    )
    return report


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--ledger", type=Path,
        default=Path("logs/agent_events/agent-events.jsonl"),
    )
    p.add_argument(
        "--usage-ledger", type=Path,
        default=Path("logs/usage/usage.jsonl"),
    )
    p.add_argument(
        "--output-dir", type=Path,
        default=Path("logs/agent_events/reports"),
    )
    args = p.parse_args()
    report = generate_reports(args.ledger, args.usage_ledger, args.output_dir)
    print(f"Generated reports for {report['record_count']} events in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
