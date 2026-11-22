# AGENTS-master.md - CB-MANAGE Master Profile

## Purpose

CB-MANAGE is a durable operating layer for comic-archive tooling,
documentation, provenance, handoff, and safe automation. It coordinates work;
it is not itself a comic archive or a license to modify one.

## Authority and Precedence

Use `AGENTS.md` for repository overrides, this file for shared policy, the
registry and routing matrix for agent structure, `truth/` for authoritative
facts, and scripts only after inspecting their current behavior. A lower-level
document cannot silently override policy or truth.

## Safety and Boundaries

- Default to read-only inspection and dry-run planning.
- Back up and validate archives before any approved write.
- Preserve unknown metadata and unrelated files.
- Never expose credentials, tokens, private keys, raw prompts, unrestricted
  tool output, database results, PII, or hidden reasoning.
- Do not perform destructive or remote actions without explicit approval.
- Record uncertainty as `unknown`; do not manufacture provenance or coverage.

## Agent Structure

Pinky is the managing agent. Specialists require a persona, contract, registry
entry, routing rule when distinct, and a discoverable skill when a repeatable
workflow warrants one. The usage-accounting agent observes resource use and
does not authorize or redirect domain work.

## Source and Tool Discipline

Read relevant code, configuration, scripts, tests, and truth records before
documenting behavior. Link to source-of-truth files instead of duplicating
volatile details. Keep shell wrappers dry-run safe and make validation
commands executable as written.

## Logging and Accounting

- Start in basic/standard logging mode.
- Escalate to extended logging for unresolved errors, failed validation,
  blocked actions, permission problems, or unresolved ambiguity; notify Richard
  when escalation starts and ends.
- Keep daily, topic, event, and usage records append-only.
- Record exactly one governance declaration per tracked task.
- Record only material observable decisions.
- Token and cost accounting is observational; absent telemetry is unknown and
  absent pricing is `unpriced`.

## Handoff and Resume

Before substantial work or a session boundary, update `docs/handoff/HANDOFF.md`
and `docs/handoff/RESUME.md` with scope, current state, validation evidence,
open risks, and the next safe action. Do not include secrets or raw transcripts.

## Configuration

- Non-secret workspace configuration: `config/local.yaml`
- Repository hooks: `.codex/hooks.json`
- Machine-local Codex configuration remains outside Git.

## Validation

Use the governance validator, structural event validation, domain-specific
tests, script help checks, and `git diff --check` as applicable. Historical
append-only ledger gaps must be reported, not silently repaired.

## Operating Summary

The quality bar is a reproducible, dry-run-safe, source-backed workflow with
explicit provenance, validation, rollback guidance, and a usable handoff.
