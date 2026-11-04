#!/usr/bin/env python3
"""Validate CB-MANAGE agent-event or usage JSONL records."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


EVENT_TYPES = {
    "session_started", "task_started", "agent_routed", "agent_loaded",
    "skill_loaded", "contract_applied", "tool_started", "tool_completed",
    "validation_completed", "error_escalated", "error_resolved",
    "governance_declared", "decision_recorded", "task_completed",
    "session_closed", "usage_reconciled",
}
EVENT_REQUIRED = {
    "event_id", "timestamp", "session_id", "event_type", "runtime", "host",
    "source", "status", "confidence", "redaction",
}
USAGE_REQUIRED = {
    "record_id", "timestamp", "session_id", "runtime", "source",
    "confidence", "reconciliation",
}
ENUMS = {
    "runtime": {"codex-cli", "vscode", "other"},
    "source": {"runtime", "exit-summary", "manual", "estimate"},
    "confidence": {"high", "medium", "low", "unknown"},
    "governance_status": {"applied", "not_required", "bypassed", "unknown"},
    "decision_type": {"routing", "implementation", "policy", "exception", "other"},
}
TASK_EVENTS = EVENT_TYPES - {"session_started", "session_closed"}
V2_TASK_REQUIRED = {
    "task_started", "governance_declared", "validation_completed", "task_completed",
}
LIST_FIELDS = {
    "expected_skills", "actual_skills", "expected_contracts", "actual_contracts",
}


def string_set(record: dict[str, object], field: str) -> set[str]:
    value = record.get(field, [])
    if not isinstance(value, list):
        return set()
    return {item for item in value if isinstance(item, str)}


def load_jsonl(path: Path) -> tuple[list[dict[str, object]], list[str]]:
    records: list[dict[str, object]] = []
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [], [f"ERROR: {exc}"]
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {number}: invalid JSON ({exc.msg})")
            continue
        if not isinstance(record, dict):
            errors.append(f"line {number}: record must be a JSON object")
            continue
        record["_line"] = number
        records.append(record)
    return records, errors


def validate_event_records(
    records: list[dict[str, object]], *, lifecycle: bool = True
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[object] = set()
    tasks: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)

    for record in records:
        number = record.get("_line", "?")
        missing = sorted(EVENT_REQUIRED - record.keys())
        if missing:
            errors.append(f"line {number}: missing {', '.join(missing)}")
        identifier = record.get("event_id")
        if identifier in seen_ids:
            errors.append(f"line {number}: duplicate identifier {identifier}")
        if identifier:
            seen_ids.add(identifier)
        event_type = record.get("event_type")
        if event_type not in EVENT_TYPES:
            errors.append(f"line {number}: invalid event_type")
        for field, allowed in ENUMS.items():
            if field in record and record[field] not in allowed:
                errors.append(f"line {number}: invalid {field}={record[field]!r}")
        for field in LIST_FIELDS:
            if field not in record:
                continue
            value = record[field]
            if not isinstance(value, list) or not all(
                isinstance(item, str) for item in value
            ):
                errors.append(f"line {number}: {field} must be an array of strings")
        if record.get("schema_version", 1) not in {1, 2}:
            errors.append(f"line {number}: unsupported schema_version")

        if event_type in TASK_EVENTS and record.get("schema_version") == 2:
            if not record.get("task_id"):
                errors.append(f"line {number}: {event_type} requires task_id")
        if event_type in {"agent_routed", "agent_loaded"} and not record.get("agent"):
            errors.append(f"line {number}: {event_type} requires agent")
        if event_type == "skill_loaded" and not record.get("skill"):
            errors.append(f"line {number}: skill_loaded requires skill")
        if event_type == "contract_applied" and not record.get("contract"):
            errors.append(f"line {number}: contract_applied requires contract")
        if event_type == "governance_declared":
            for field in ("governance_status", "basis"):
                if not record.get(field):
                    errors.append(f"line {number}: governance_declared requires {field}")
        if event_type == "decision_recorded":
            for field in ("decision_id", "decision_type", "governance_status", "basis"):
                if not record.get(field):
                    errors.append(f"line {number}: decision_recorded requires {field}")

        session_id = record.get("session_id")
        task_id = record.get("task_id")
        if isinstance(session_id, str) and isinstance(task_id, str):
            tasks[(session_id, task_id)].append(record)

    if lifecycle:
        for (session_id, task_id), task_records in sorted(tasks.items()):
            if not any(record.get("schema_version") == 2 for record in task_records):
                continue
            event_types = {str(record.get("event_type")) for record in task_records}
            missing_events = sorted(V2_TASK_REQUIRED - event_types)
            if missing_events:
                errors.append(
                    f"task {session_id}/{task_id}: missing lifecycle events "
                    + ", ".join(missing_events)
                )
            declarations = [
                record for record in task_records
                if record.get("event_type") == "governance_declared"
            ]
            if len(declarations) > 1:
                warnings.append(
                    f"task {session_id}/{task_id}: multiple governance declarations; "
                    "the latest declaration is used for coverage checks"
                )
            if not declarations:
                continue
            declaration = declarations[-1]
            governance_status = declaration.get("governance_status")
            if governance_status in {"bypassed", "unknown"}:
                warnings.append(
                    f"task {session_id}/{task_id}: governance status is {governance_status}"
                )
            if governance_status != "applied":
                continue

            actual_agent = declaration.get("actual_agent")
            loaded_agents = {
                record.get("agent") for record in task_records
                if record.get("event_type") in {"agent_routed", "agent_loaded"}
            }
            if not actual_agent:
                errors.append(
                    f"task {session_id}/{task_id}: applied governance requires actual_agent"
                )
            elif actual_agent not in loaded_agents:
                errors.append(
                    f"task {session_id}/{task_id}: declared agent {actual_agent!r} "
                    "has no agent_routed/agent_loaded event"
                )

            actual_skills = string_set(declaration, "actual_skills")
            loaded_skills = {
                record.get("skill") for record in task_records
                if record.get("event_type") == "skill_loaded"
            }
            for skill in sorted(actual_skills - loaded_skills):
                errors.append(
                    f"task {session_id}/{task_id}: declared skill {skill!r} "
                    "has no skill_loaded event"
                )

            actual_contracts = string_set(declaration, "actual_contracts")
            loaded_contracts = {
                record.get("contract") for record in task_records
                if record.get("event_type") == "contract_applied"
            }
            if not actual_contracts:
                errors.append(
                    f"task {session_id}/{task_id}: applied governance requires actual_contracts"
                )
            for contract in sorted(actual_contracts - loaded_contracts):
                errors.append(
                    f"task {session_id}/{task_id}: declared contract {contract!r} "
                    "has no contract_applied event"
                )
    return errors, warnings


def validate_usage_records(records: list[dict[str, object]]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    seen_ids: set[object] = set()
    for record in records:
        number = record.get("_line", "?")
        missing = sorted(USAGE_REQUIRED - record.keys())
        if missing:
            errors.append(f"line {number}: missing {', '.join(missing)}")
        identifier = record.get("record_id")
        if identifier in seen_ids:
            errors.append(f"line {number}: duplicate identifier {identifier}")
        if identifier:
            seen_ids.add(identifier)
        for field, allowed in ENUMS.items():
            if field in record and record[field] not in allowed:
                errors.append(f"line {number}: invalid {field}={record[field]!r}")
    return errors, []


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("ledger", type=Path)
    p.add_argument("--kind", choices=("events", "usage"), default="events")
    p.add_argument(
        "--no-lifecycle", action="store_true",
        help="Validate event records individually without checking task completeness",
    )
    args = p.parse_args()
    records, parse_errors = load_jsonl(args.ledger)
    if args.kind == "events":
        errors, warnings = validate_event_records(records, lifecycle=not args.no_lifecycle)
    else:
        errors, warnings = validate_usage_records(records)
    errors = parse_errors + errors
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Valid {args.kind} ledger: {len(records)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
