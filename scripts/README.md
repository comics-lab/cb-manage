# CB-MANAGE Scripts

## Agent Invocation and Usage Tracking

| Script | Purpose | Mutation boundary |
| --- | --- | --- |
| `capture_codex_hook_event.py` | Convert allowlisted Codex hook metadata into lifecycle events | Appends event metadata; generates reports at session end |
| `record_agent_event.py` | Append one redaction-safe event | Appends only to the selected JSONL ledger |
| `validate_agent_ledger.py` | Validate event or usage JSONL records | Read-only |
| `report_agent_usage.py` | Aggregate lifecycle, governance, decision, and available usage metadata | Writes aggregate Markdown and JSON reports |

## Commands

```bash
python3 scripts/record_agent_event.py --help
python3 scripts/validate_agent_ledger.py --help
python3 scripts/report_agent_usage.py --help
python3 -m unittest tests/test_agent_usage_tracking.py
```

Repository hooks are defined in `.codex/hooks.json`. Review them with `/hooks`
and start a new Codex session after approving or changing the hook definition.

