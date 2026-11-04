import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from capture_codex_hook_event import event_to_record  # noqa: E402
from record_agent_event import append_record, build_record  # noqa: E402
from report_agent_usage import generate_reports  # noqa: E402
from validate_agent_ledger import validate_event_records  # noqa: E402


class AgentUsageTrackingTests(unittest.TestCase):
    def event(self, event_type, **values):
        defaults = {
            "session_id": "session-test",
            "task_id": "turn-test",
            "event_type": event_type,
            "runtime": "vscode",
            "host": "Codex IDE extension",
            "source": "manual",
            "status": "completed",
            "confidence": "high",
        }
        defaults.update(values)
        return build_record(**defaults)

    def complete_task(self):
        return [
            self.event("task_started", source="runtime", status="started"),
            self.event("agent_routed", agent="agent_usage_accounting"),
            self.event("agent_loaded", agent="agent_usage_accounting"),
            self.event("skill_loaded", skill="agent-usage-accounting"),
            self.event("contract_applied", contract="Usage_Accounting_Agent"),
            self.event(
                "governance_declared",
                governance_status="applied",
                actual_agent="agent_usage_accounting",
                actual_skills=["agent-usage-accounting"],
                actual_contracts=["Usage_Accounting_Agent"],
                basis="Director_Routing_Matrix.md",
            ),
            self.event("validation_completed"),
            self.event("task_completed", source="runtime"),
        ]

    def test_complete_v2_task_validates(self):
        errors, warnings = validate_event_records(self.complete_task())
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_missing_governance_is_a_lifecycle_error(self):
        records = [
            self.event("task_started", status="started"),
            self.event("validation_completed"),
            self.event("task_completed"),
        ]
        errors, _ = validate_event_records(records)
        self.assertTrue(any("governance_declared" in error for error in errors))

    def test_malformed_governance_list_is_reported_without_crashing(self):
        records = self.complete_task()
        declaration = next(
            record for record in records
            if record["event_type"] == "governance_declared"
        )
        declaration["actual_skills"] = "agent-usage-accounting"
        errors, _ = validate_event_records(records)
        self.assertTrue(any("actual_skills must be an array" in error for error in errors))

    def test_hook_adapter_discards_content_fields(self):
        hook = {
            "hook_event_name": "PostToolUse",
            "session_id": "session-test",
            "turn_id": "turn-test",
            "tool_name": "Bash",
            "tool_use_id": "tool-test",
            "model": "model-test",
            "prompt": "must not be stored",
            "tool_input": {"command": "must not be stored"},
            "tool_response": "must not be stored",
            "last_assistant_message": "must not be stored",
            "transcript_path": "/must/not/be/stored",
        }
        record = event_to_record(hook, "vscode", "Codex IDE extension")
        self.assertIsNotNone(record)
        payload = json.dumps(record)
        self.assertNotIn("must not be stored", payload)
        self.assertNotIn("transcript_path", record)
        self.assertEqual("Bash", record["tool_name"])

    def test_report_generation_writes_markdown_and_json(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ledger = root / "events.jsonl"
            for record in self.complete_task():
                append_record(record, ledger)
            output = root / "reports"
            report = generate_reports(ledger, root / "missing-usage.jsonl", output)
            self.assertEqual(1, report["complete_v2_task_count"])
            self.assertTrue((output / "agent-usage-latest.md").is_file())
            self.assertTrue((output / "agent-usage-latest.json").is_file())
            self.assertNotIn("must not be stored", (output / "agent-usage-latest.md").read_text())


if __name__ == "__main__":
    unittest.main()
