# CB-MANAGE Agent System Index

## Core Entry Points

- `AGENTS.md` — repository runtime entrypoint.
- `AGENTS-master.md` — shared policy baseline.
- `docs/agents/system/registry/Agent_Registry.md` — active agent inventory.
- `docs/agents/system/registry/Director_Routing_Matrix.md` — request routing.
- `docs/agents/system/runbooks/Extended_Logging_Runbook.md` — human-readable logging policy.
- `docs/agents/system/runbooks/Agent_Invocation_and_Accounting_Runbook.md` — structured event and usage accounting.
- `docs/agents/system/governance/Agent_Usage_Accounting_Governance.md` — accounting policy and redaction boundary.
- `docs/agents/system/schemas/` — JSON schemas for event and usage records.
- `truth/TRUTHS_INDEX.md` — approved and candidate source inventory.
- `truth/EXTERNAL/manifest.md` — external documentation URL registry.
- `truth/sources_of_truth_architecture.md` — provenance and authority rules.

## Logging Implementation

- Persona: `skills/agents/AGENTS-Usage-Accounting.md`
- Contract: `docs/agents/contracts/Usage_Accounting_Agent.md`
- Skill: `.agents/skills/agent-usage-accounting/SKILL.md`
- Hooks: `.codex/hooks.json`
- Scripts: `scripts/capture_codex_hook_event.py`, `scripts/record_agent_event.py`, `scripts/validate_agent_ledger.py`, and `scripts/report_agent_usage.py`
- Tests: `tests/test_agent_usage_tracking.py`

