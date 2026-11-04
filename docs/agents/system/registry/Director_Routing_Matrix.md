# CB-MANAGE Director Routing Matrix

## Routing Table

| Request indicators | Primary agent | Required skill | Boundary |
| --- | --- | --- | --- |
| repository setup, governance, routing, handoff, general coordination | Managing Agent (Arthur) | None by default | Use the smallest applicable persona, contract, and skill set |
| logging policy, detail logging, extended logging, topic log, daily log | Managing Agent (Arthur) | `app-documentation` when available | Apply the active logging runbook; never expand permissions |
| token usage, cache accounting, exit summary, usage ledger, model cost | Agent Usage Accounting | `agent-usage-accounting` | Observe and reconcile; do not guess pricing or capture task content |

## Ambiguity Rules

- Route unmatched requests to the Managing Agent for triage.
- Use `not_required`, `bypassed`, or `unknown` rather than inventing governance attribution.
- Ask for clarification when a choice would materially change scope, permissions, or durable output.

