# AGENTS-master.md - CB-MANAGE Master Profile

## Purpose

## Authority and Precedence

## Recommended Read Order

## Startup Permission and Approval Boundary

## Directory Roles

## Agent Structure

## Multiple Agents and Skillsets

## What Not To Train

## Prompt Style

## Project Customization

## Analyst-Oriented Companion Material

## Key Companion Docs

## Configuration

- Non-secret workspace configuration: `config/local.yaml`
- Repository Codex hooks: `.codex/hooks.json`
- Machine-local Codex configuration remains outside Git.

## Logging

- Daily operational log: `logs/Dialog_YYYY-MM-DD.md`
- Durable topic logs: `docs/agents/chats/`
- Structured event ledger: `logs/agent_events/agent-events.jsonl`
- Optional usage ledger: `logs/usage/usage.jsonl`
- Generated aggregate reports: `logs/agent_events/reports/`
- All durable logs are append-only; corrections are additive.
- Every session starts in basic/standard logging mode.
- Detail/verbatim and extended modes are session-scoped unless Richard declares a longer timeframe.
- Any unresolved error, blocked action, failed validation, permission problem, or unresolved ambiguity escalates the session to extended logging until resolved.
- The active agent must notify Richard when extended logging begins and ends.
- Structured tracking records metadata and approved identifiers only; it must not store prompts, responses, tool payloads, credentials, SQL, database output, PII, or hidden reasoning.
- `governance_declared` is required once per tracked task. Use `applied`, `not_required`, `bypassed`, or `unknown` explicitly.
- `decision_recorded` is reserved for material observable outcomes and their source references.
- Token and cost accounting is observational. Unknown telemetry remains unknown, and pricing remains `unpriced` without an approved dated pricing profile.

## Validation

- Validate events with `python3 scripts/validate_agent_ledger.py logs/agent_events/agent-events.jsonl`.
- Validate usage with `python3 scripts/validate_agent_ledger.py --kind usage logs/usage/usage.jsonl`.
- Run regression tests with `python3 -m unittest tests/test_agent_usage_tracking.py`.
- Generate reports with `python3 scripts/report_agent_usage.py`.

## Handoff and Resume

## Operating Summary
