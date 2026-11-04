# Agent Usage Accounting Governance

> Status: ACTIVE — operational baseline
> Date: 2026-08-10
> Owner: Richard
> Managing agent: Arthur
> Scope: token usage, attribution, reconciliation, and configured cost estimates

## Decision

Create a narrow `Agent Usage Accounting Agent` backed by the
`agent-usage-accounting` skill. It observes usage and reports uncertainty; it
does not control execution. Runtime/provider summaries are authoritative when
available. Local estimates are useful for budgeting but are never billing.

## Tracked and excluded data

Track session/task, agent/skill/contract, model, source time, token dimensions,
safe tool-call/wall-time aggregates, attribution, confidence, reconciliation,
variance, and cost only with a complete dated pricing profile.

Exclude credentials, API keys, cookies, connection strings, raw prompts, SQL,
database results, PII, hidden reasoning, and full transcripts. The accounting
agent must not connect to databases or inspect task content.

## Interpretation and reconciliation

The exit summary is the authoritative session reference when supplied by the
runtime. Cached input is separate and is not automatically added to active input
or total. Reasoning is normally a subset of output and must not be added twice.
Reports preserve estimates and measured values side by side, with source,
confidence, allocation method, formula, variance, and unallocated shared context.
Missing or contradictory dimensions are warnings, not invitations to guess.

## Documentation and implementation status

Accounting reports contain aggregates and approved identifiers only, state that
accounting is not necessarily provider billing, and include a redaction statement.

- Established: skill, governance reference, contract, persona, and routing docs.
- Established: JSONL event ledger, Codex hook adapter, lifecycle-completeness
  validation, explicit governance/decision declarations, and aggregate
  Markdown/JSON reports.
- Pending: configure approved pricing profiles and validate a sample runtime or
  exit-summary usage record without recording surrounding content.
