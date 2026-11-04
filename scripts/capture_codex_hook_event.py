#!/usr/bin/env python3
"""Capture allowlisted Codex hook metadata without storing hook content."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from record_agent_event import append_record, build_record


EVENT_MAP = {
    "SessionStart": "session_started",
    "UserPromptSubmit": "task_started",
    "SubagentStart": "agent_loaded",
    "PostToolUse": "tool_completed",
    "Stop": "task_completed",
    "SessionEnd": "session_closed",
}


def runtime_identity(runtime_override: str | None, host_override: str | None) -> tuple[str, str]:
    if runtime_override:
        runtime = runtime_override
    elif os.environ.get("VSCODE_PID") or os.environ.get("TERM_PROGRAM") == "vscode":
        runtime = "vscode"
    else:
        runtime = "codex-cli"
    if host_override:
        host = host_override
    else:
        host = "Codex IDE extension" if runtime == "vscode" else "Codex CLI"
    return runtime, host


def event_to_record(event: dict[str, object], runtime: str, host: str) -> dict[str, object] | None:
    hook_event = event.get("hook_event_name")
    if not isinstance(hook_event, str) or hook_event not in EVENT_MAP:
        return None
    session_id = event.get("session_id")
    if not isinstance(session_id, str) or not session_id:
        raise ValueError("hook event is missing session_id")

    turn_id = event.get("turn_id") if isinstance(event.get("turn_id"), str) else None
    values: dict[str, object] = {
        "session_id": session_id,
        "event_type": EVENT_MAP[hook_event],
        "runtime": runtime,
        "host": host,
        "source": "runtime",
        "status": "started" if hook_event in {"SessionStart", "UserPromptSubmit"} else "completed",
        "confidence": "high",
        "hook_event": hook_event,
    }
    if turn_id:
        values["turn_id"] = turn_id
        values["task_id"] = turn_id
    for field in ("model", "permission_mode"):
        if isinstance(event.get(field), str):
            values[field] = event[field]

    if hook_event == "SubagentStart":
        agent_type = event.get("agent_type")
        agent_id = event.get("agent_id")
        if isinstance(agent_type, str):
            values["agent"] = agent_type
            values["actual_agent"] = agent_type
        if isinstance(agent_id, str):
            values["agent_instance_id"] = agent_id
    elif hook_event == "PostToolUse":
        if isinstance(event.get("tool_name"), str):
            values["tool_name"] = event["tool_name"]
        if isinstance(event.get("tool_use_id"), str):
            values["tool_use_id"] = event["tool_use_id"]

    return build_record(**values)


def hook_response(event: dict[str, object]) -> dict[str, object]:
    hook_event = event.get("hook_event_name")
    turn_id = event.get("turn_id")
    if hook_event == "UserPromptSubmit" and isinstance(turn_id, str):
        return {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    f"Usage tracking is active for task_id {turn_id}. Before completing "
                    "the task, record one governance_declared event and record only "
                    "material observable decisions as decision_recorded events. Use "
                    "not_required, bypassed, or unknown explicitly instead of guessing."
                ),
            }
        }
    return {}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ledger", default="logs/agent_events/agent-events.jsonl")
    p.add_argument("--reports-dir", default="logs/agent_events/reports")
    p.add_argument("--runtime", choices=("codex-cli", "vscode", "other"))
    p.add_argument("--host")
    p.add_argument("--no-report", action="store_true")
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict):
            raise ValueError("hook input must be a JSON object")
        runtime, host = runtime_identity(args.runtime, args.host)
        record = event_to_record(event, runtime, host)
        if record is not None:
            append_record(record, Path(args.ledger))

        if event.get("hook_event_name") == "SessionEnd" and not args.no_report:
            from report_agent_usage import generate_reports

            generate_reports(
                ledger=Path(args.ledger),
                usage_ledger=Path("logs/usage/usage.jsonl"),
                output_dir=Path(args.reports_dir),
            )
        print(json.dumps(hook_response(event), sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"agent tracking hook failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
