# CB-MANAGE Agent Registry

## Active Agents

| Agent | Persona | Contract | Purpose | Required skill |
| --- | --- | --- | --- | --- |
| Managing Agent (Arthur) | Defined by `AGENTS.md` and `AGENTS-master.md` | Repository policy | Coordinate repository construction, routing, governance, and handoff | None by default |
| Agent Usage Accounting | `skills/agents/AGENTS-Usage-Accounting.md` | `docs/agents/contracts/Usage_Accounting_Agent.md` | Maintain privacy-preserving event and usage accounting without controlling work | `agent-usage-accounting` |

## Registration Rules

- Every active specialist needs a persona, contract, routing entry, and stable identifier.
- Skills are loaded only when the routed task requires them.
- Logging and accounting agents observe work; they do not grant permissions or change task scope.

