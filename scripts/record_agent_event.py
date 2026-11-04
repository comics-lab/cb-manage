#!/usr/bin/env python3
"""Append one redaction-safe agent event to a CB-MANAGE JSONL ledger."""

from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


EVENT_TYPES = {
    "session_started", "task_started", "agent_routed", "agent_loaded",
    "skill_loaded", "contract_applied", "tool_started", "tool_completed",
    "validation_completed", "error_escalated", "error_resolved",
    "governance_declared", "decision_recorded", "task_completed",
    "session_closed", "usage_reconciled",
}
SOURCES = {"runtime", "exit-summary", "manual", "estimate"}
RUNTIMES = {"codex-cli", "vscode", "other"}
STATUSES = {"started", "active", "completed", "failed", "resolved", "pending"}
CONFIDENCE = {"high", "medium", "low", "unknown"}
GOVERNANCE_STATUSES = {"applied", "not_required", "bypassed", "unknown"}
DECISION_TYPES = {"routing", "implementation", "policy", "exception", "other"}
REDACTION = "No secrets, raw prompts, tool output, PII, or hidden reasoning recorded."


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ledger", default="logs/agent_events/agent-events.jsonl")
    p.add_argument("--event-type", required=True, choices=sorted(EVENT_TYPES))
    p.add_argument("--session-id", required=True)
    p.add_argument("--task-id")
    p.add_argument("--turn-id")
    p.add_argument("--runtime", required=True, choices=sorted(RUNTIMES))
    p.add_argument("--host", required=True)
    p.add_argument("--agent")
    p.add_argument("--skill")
    p.add_argument("--contract")
    p.add_argument("--model")
    p.add_argument("--permission-mode")
    p.add_argument("--hook-event")
    p.add_argument("--tool-name")
    p.add_argument("--tool-use-id")
    p.add_argument("--agent-instance-id")
    p.add_argument("--decision-id")
    p.add_argument("--decision-type", choices=sorted(DECISION_TYPES))
    p.add_argument("--governance-status", choices=sorted(GOVERNANCE_STATUSES))
    p.add_argument("--expected-agent")
    p.add_argument("--actual-agent")
    p.add_argument("--expected-skill", action="append", default=[])
    p.add_argument("--actual-skill", action="append", default=[])
    p.add_argument("--expected-contract", action="append", default=[])
    p.add_argument("--actual-contract", action="append", default=[])
    p.add_argument("--basis", help="Short policy or evidence reference; never hidden reasoning")
    p.add_argument("--source", default="manual", choices=sorted(SOURCES))
    p.add_argument("--status", default="completed", choices=sorted(STATUSES))
    p.add_argument("--confidence", default="medium", choices=sorted(CONFIDENCE))
    p.add_argument("--note", help="Short non-sensitive note; never include secrets or raw prompts")
    return p


def build_record(**values: object) -> dict[str, object]:
    record = {
        "schema_version": 2,
        "event_id": f"evt-{uuid.uuid4().hex}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": values["session_id"],
        "event_type": values["event_type"],
        "runtime": values["runtime"],
        "host": values["host"],
        "source": values.get("source", "manual"),
        "status": values.get("status", "completed"),
        "confidence": values.get("confidence", "medium"),
        "redaction": REDACTION,
    }
    scalar_fields = (
        "task_id", "turn_id", "agent", "skill", "contract", "model",
        "permission_mode", "hook_event", "tool_name", "tool_use_id",
        "agent_instance_id", "decision_id", "decision_type",
        "governance_status", "expected_agent", "actual_agent", "basis", "note",
    )
    for name in scalar_fields:
        value = values.get(name)
        if value is not None and value != "":
            record[name] = value

    list_fields = (
        "expected_skills", "actual_skills", "expected_contracts", "actual_contracts",
    )
    for name in list_fields:
        value = values.get(name)
        if value:
            record[name] = list(value)  # type: ignore[arg-type]
    return record


def append_record(record: dict[str, object], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(record, sort_keys=True) + "\n").encode("utf-8")
    descriptor = destination.open("ab", buffering=0)
    try:
        descriptor.write(payload)
    finally:
        descriptor.close()


def main() -> int:
    args = parser().parse_args()
    values = vars(args).copy()
    values["expected_skills"] = values.pop("expected_skill")
    values["actual_skills"] = values.pop("actual_skill")
    values["expected_contracts"] = values.pop("expected_contract")
    values["actual_contracts"] = values.pop("actual_contract")
    destination = Path(values.pop("ledger"))
    record = build_record(**values)

    append_record(record, destination)
    print(record["event_id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
