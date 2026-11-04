---
name: agent-usage-accounting
description: Track and reconcile token usage and configured model costs for Codex agents, skills, contracts, tools, and bounded tasks. Use for usage ledgers, session cost summaries, token budgets, cache accounting, exit-report reconciliation, and token-efficiency reviews without accessing secrets or changing task behavior.
---

# Agent Usage Accounting Skill

Use this skill as an observational accounting lane. It measures or estimates
resource use; it does not supervise, redirect, or authorize the work being
measured.

## Operating sequence

1. Identify the session, task, agent, skill, and contract labels in scope.
2. Prefer authoritative runtime usage or the user’s exit summary; record local
   estimates separately when authoritative telemetry is unavailable.
3. Keep input, cached input, output, reasoning, tool calls, wall time, and price
   distinct. Cached input is diagnostic and must not be silently added to total.
4. Apply pricing only from an explicitly named, dated pricing configuration.
   If pricing is missing or ambiguous, report tokens and mark cost `unpriced`.
5. Attribute usage only when evidence supports attribution. Mark shared,
   allocated, or unknown and document the allocation method.
6. Reconcile estimates against final runtime values. Preserve both values and
   variance; never overwrite the estimate.
7. Redact secrets, prompts containing sensitive data, database results, and
   full transcripts unless separately approved.
8. Stop on missing dimensions, unknown model identity, unreconciled totals, or
   unsupported cost assumptions.

## Accounting boundaries

- Never access passwords, tokens, API keys, cookies, connection strings, or
  other credentials.
- Never connect to a database, execute SQL, inspect rows, or capture task content.
- Never cancel, redirect, rewrite, or authorize another agent’s work.
- Never claim token totals equal vendor billing without provider evidence.
- Never double-count reasoning as output or cached input as active input.
- Never publish raw prompts, private tool output, or PII in an accounting log.

## Required record fields

Record `record_id`, timestamp, session/task identifiers, runtime (`codex-cli`,
`vscode`, or `other`), host, agent, skill, contract, model label, source
(`runtime`, `exit-summary`, `manual`, or `estimate`), input tokens,
cached input tokens, output tokens, reasoning tokens, total tokens, pricing
profile or `unpriced`, allocation method, confidence, reconciliation status, and
redaction statement.

Read [`references/accounting-governance.md`](references/accounting-governance.md)
for the ledger schema, formulas, confidence levels, and review gates.

## Routing

Use this agent for ledger design, reconciliation, and reporting; use Arthur for
documentation/registry updates. Sensitive publication requires explicit Richard
approval and Managing Agent review.
