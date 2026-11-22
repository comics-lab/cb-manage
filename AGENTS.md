# AGENTS.md - CB-MANAGE Project Entrypoint

CB-MANAGE is the comic-archive management workspace. Load this file first,
then apply `AGENTS-master.md` and the task-specific references below.

## Master Profile Reference

- Master policy: `AGENTS-master.md`
- Owner: Richard
- Managing-agent identity: Pinky
- Repository role: operating layer and domain-tool workspace, not the archive itself

## Repository-Specific Overrides

- Preserve the comic-domain boundary; do not copy SSO-MANAGE identity, truth,
  credentials, or historical logs into this repository.
- Default to read-only and dry-run behavior for archive, metadata, Mylar, and
  external-service work.
- No destructive filesystem, Git, remote, credential, publication, or
  access-control action without explicit Richard approval.
- Use `python3` for maintained scripts and prefer fixture-backed validation
  before touching live comic archives.

## Recommended Read Order

1. `AGENTS.md`
2. `AGENTS-master.md`
3. `docs/agents/system/registry/Agent_System_Index.md`
4. `docs/agents/system/registry/Agent_Registry.md`
5. `docs/agents/system/registry/Director_Routing_Matrix.md`
6. `truth/TRUTHS_INDEX.md` and relevant `truth/` records
7. The selected persona, contract, and `.agents/skills/*/SKILL.md`
8. `docs/handoff/RESUME.md` and the relevant runbook

## Startup Permission and Approval Boundary

At startup ask Richard for session-scoped read/write access to the resolved
checkout and, separately, `/tmp` when temporary artifacts may be needed.
Permission is not implied by this file, Workspace Trust, or a model label.
Explicit approval is required before destructive changes, remote operations,
credential use, publication, or access-control changes.

## Directory Roles

- `docs/`: durable plans, runbooks, handoffs, and domain knowledge.
- `logs/`: append-only human-readable and structured operational records.
- `skills/agents/`: persona documents.
- `.agents/skills/`: discoverable reusable skills.
- `tools/`: comic-domain utilities and shell wrappers.
- `truth/`: source authority, provenance, and candidate external references.
- `config/`: non-secret workspace configuration.

## Agent Setup and Routing

- Registry: `docs/agents/system/registry/Agent_Registry.md`
- Routing: `docs/agents/system/registry/Director_Routing_Matrix.md`
- Usage-accounting persona: `skills/agents/AGENTS-Usage-Accounting.md`
- Usage-accounting contract: `docs/agents/contracts/Usage_Accounting_Agent.md`
- Usage-accounting skill: `.agents/skills/agent-usage-accounting/SKILL.md`
- Governance validator: `scripts/verify_agent_governance.py`

Route repository setup, coordination, handoff, and domain triage to Pinky.
Route usage, cost, or ledger reconciliation to the usage-accounting agent.
Use `not_required`, `bypassed`, or `unknown` when attribution is unavailable;
never infer it.

## Logging Requirements

- Human-readable policy: `docs/agents/system/runbooks/Extended_Logging_Runbook.md`
- Structured procedure: `docs/agents/system/runbooks/Agent_Invocation_and_Accounting_Runbook.md`
- Daily log: `logs/Dialog_YYYY-MM-DD.md`
- Topic logs: `docs/agents/chats/`
- Event ledger: `logs/agent_events/agent-events.jsonl`
- Optional usage ledger: `logs/usage/usage.jsonl`
- Logs are append-only; corrections are additive.
- Every tracked task records one `governance_declared` event and only material
  observable `decision_recorded` events.
- Never log credentials, raw prompts, unrestricted tool output, SQL/database
  results, PII, or hidden reasoning.

## Validation

Run the applicable checks before handoff:

```bash
python3 scripts/verify_agent_governance.py
python3 scripts/validate_agent_ledger.py --no-lifecycle logs/agent_events/agent-events.jsonl
python3 -m unittest discover -s tests -q
git diff --check
```

The full ledger lifecycle check may report historical gaps. Do not rewrite
append-only history merely to make an old record pass; document the gap.

## First Session

Start with a bounded prompt identifying the goal, context, inputs, constraints,
desired output, and whether the work is read-only, dry-run, or approved for
write operations. Inspect `docs/handoff/RESUME.md` before continuing prior work.

## Operating Summary

Pinky coordinates the workspace, protects source authority and archive safety,
and leaves durable, validated handoffs. Comic-domain changes must identify
their target archives, provenance, dry-run behavior, backups, validation, and
rollback path before implementation.
