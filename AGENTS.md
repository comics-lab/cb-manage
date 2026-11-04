# AGENTS.md - CB-MANAGE Project Entrypoint

## Master Profile Reference

## Repository-Specific Overrides

## Runtime Identity

## Recommended Read Order

## Startup Permission and Approval Boundary

## Directory Roles

## Agent Setup and Routing

- Agent registry: `docs/agents/system/registry/Agent_Registry.md`
- Routing matrix: `docs/agents/system/registry/Director_Routing_Matrix.md`
- Usage-accounting persona: `skills/agents/AGENTS-Usage-Accounting.md`
- Usage-accounting contract: `docs/agents/contracts/Usage_Accounting_Agent.md`
- Usage-accounting skill: `.agents/skills/agent-usage-accounting/SKILL.md`

## Logging Requirements

- Authoritative policy: `docs/agents/system/runbooks/Extended_Logging_Runbook.md`
- Invocation/accounting procedure: `docs/agents/system/runbooks/Agent_Invocation_and_Accounting_Runbook.md`
- Daily log: `logs/Dialog_YYYY-MM-DD.md`
- Topic logs: `docs/agents/chats/`
- Event ledger: `logs/agent_events/agent-events.jsonl`
- Usage ledger: `logs/usage/usage.jsonl`, when authoritative or explicitly estimated usage exists
- Logs are append-only; corrections are additive.
- Every tracked task records exactly one `governance_declared` event and only material observable decisions.
- Never log credentials, raw prompts, unrestricted tool output, SQL/database results, PII, or hidden reasoning.

## Prompt Style

## First Session

## Operating Summary
