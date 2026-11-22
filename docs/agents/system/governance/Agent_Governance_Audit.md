# CB-MANAGE Agent Governance Audit

Run this audit after changing policy, personas, contracts, skills, routing,
truth references, or logging behavior.

```bash
python3 scripts/verify_agent_governance.py
python3 -m unittest discover -s tests -q
python3 scripts/validate_agent_ledger.py --no-lifecycle logs/agent_events/agent-events.jsonl
git diff --check
```

The full event-ledger lifecycle check remains useful, but historical records
may predate the current lifecycle contract. Do not rewrite append-only history
to repair those records; document the gap in the handoff.

Review SQLite3 scope, truth-source status, dry-run behavior, archive backups,
validation, rollback, and redaction-safe handoff continuity.
