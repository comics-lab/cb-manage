# Agent Invocation and Usage Accounting Runbook

## Purpose

This runbook adds portable, structured attribution to the existing human-readable
logging standard. It applies to Codex CLI and the Codex VS Code extension without
assuming that either host exposes identical commands or token telemetry.

The authoritative human-readable logging policy remains
[`Extended_Logging_Runbook.md`](Extended_Logging_Runbook.md). This runbook records
event metadata; it must not become a storage location for prompts, credentials,
raw tool output, SQL results, PII, or hidden reasoning.

## Runtime-neutral identifiers

Every task should identify:

- `session_id`: one host session;
- `task_id`: one bounded user objective;
- `agent`: stable registry ID;
- `skill`: stable skill directory/name;
- `contract`: stable contract filename or ID;
- `runtime`: `codex-cli`, `vscode`, or `other`;
- `source`: `runtime`, `exit-summary`, `manual`, or `estimate`.

The host is evidence about where the work occurred, not a different governance
system. CLI wrappers may add more events; VS Code sessions may depend on explicit
agent-side event records and a user-provided exit summary.

## Automated Codex lifecycle capture

The repository-local [`.codex/hooks.json`](../../../../.codex/hooks.json) sends
allowlisted lifecycle metadata to `scripts/capture_codex_hook_event.py`. It
records session start/end, turn start/stop, subagent start, and tool completion.
The adapter deliberately discards prompts, assistant messages, tool inputs,
tool responses, and transcript contents.

On first use, review and trust the project hooks with `/hooks`. Hook changes
produce a new trust hash and require another review. Start a new Codex session
after enabling or changing hooks.

Automatic lifecycle events do not prove that a registry persona, skill, or
contract governed a decision. Each tracked task must therefore add one
`governance_declared` event. Use `applied`, `not_required`, `bypassed`, or
`unknown`; do not infer missing attribution.

## Event ledger

Append events to:

```text
logs/agent_events/agent-events.jsonl
```

The schema is [`agent-event.schema.json`](../schemas/agent-event.schema.json).
Use `scripts/record_agent_event.py` for a minimal redaction-safe record:

```bash
python3 scripts/record_agent_event.py \
  --event-type task_started \
  --session-id session-YYYYMMDD-shortid \
  --task-id task-short-description \
  --runtime vscode \
  --host "Codex IDE extension" \
  --agent agent_managing \
  --contract Managing_Agent \
  --source manual \
  --status started \
  --confidence medium
```

Required lifecycle events are `session_started`, `task_started`, `agent_routed`,
`agent_loaded`, `skill_loaded`, `contract_applied`, `governance_declared`,
`validation_completed`, `task_completed`, and `session_closed`. Skills may be
explicitly `not_required` when the routing matrix requires none. Add decision,
tool, and error events when useful; do not copy unrestricted tool output into
the ledger.

Example applied-governance declaration:

```bash
python3 scripts/record_agent_event.py \
  --event-type governance_declared \
  --session-id SESSION_ID \
  --task-id TURN_ID \
  --runtime vscode \
  --host "Codex IDE extension" \
  --governance-status applied \
  --expected-agent agent_usage_accounting \
  --actual-agent agent_usage_accounting \
  --expected-skill agent-usage-accounting \
  --actual-skill agent-usage-accounting \
  --expected-contract Usage_Accounting_Agent \
  --actual-contract Usage_Accounting_Agent \
  --basis docs/agents/system/registry/Director_Routing_Matrix.md \
  --source manual \
  --confidence high
```

Record only material observable decisions. A decision event is an outcome and
source reference, not hidden reasoning:

```bash
python3 scripts/record_agent_event.py \
  --event-type decision_recorded \
  --session-id SESSION_ID \
  --task-id TURN_ID \
  --runtime vscode \
  --host "Codex IDE extension" \
  --decision-id DEC-SESSION-SHORT \
  --decision-type implementation \
  --governance-status applied \
  --basis docs/agents/system/runbooks/Agent_Invocation_and_Accounting_Runbook.md \
  --source manual \
  --confidence high
```

## Usage ledger

Store usage records separately under:

```text
logs/usage/
```

The schema is [`usage-record.schema.json`](../schemas/usage-record.schema.json).
Use authoritative runtime data or the user’s exit summary when available. If
only an estimate exists, preserve it as `source: estimate` and mark its
confidence. Missing pricing remains `unpriced`; do not infer billing.

## CLI and VS Code rules

- Do not require CLI-only commands in the common logging contract.
- Record `runtime` and `host` on every event and usage record.
- Treat IDE sessions as valid even when per-turn token telemetry is unavailable.
- Use `source: exit-summary` for a final usage report supplied by the host/user.
- Use `source: manual` for an agent-recorded lifecycle event.
- Use `source: estimate` only for explicitly labeled reconstruction.
- Never claim that identical interfaces imply identical telemetry.

## Validation

Validate event records with:

```bash
python3 scripts/validate_agent_ledger.py logs/agent_events/agent-events.jsonl
```

Validate usage records with:

```bash
python3 scripts/validate_agent_ledger.py --kind usage logs/usage/usage.jsonl
```

The validator checks JSON shape, required fields, stable identifiers, and
portable enum values. For schema-v2 tasks it also checks lifecycle completeness
and expected-versus-actual declarations. Use `--no-lifecycle` only for
structural diagnosis of an incomplete ledger. It does not inspect or infer
sensitive content.

## Reports

Generate the current Markdown and JSON reports with:

```bash
python3 scripts/report_agent_usage.py
```

Outputs are written to:

```text
logs/agent_events/reports/agent-usage-latest.md
logs/agent_events/reports/agent-usage-latest.json
```

The `SessionEnd` hook generates the same reports automatically. Reports expose
aggregates, identifiers, lifecycle gaps, governance status, and decision counts.
They do not contain prompt, response, tool, SQL, credential, PII, or hidden
reasoning content.

## Session closeout

1. Complete the standard daily/topic log.
2. Append lifecycle and validation events.
3. Record the authoritative usage summary, if available.
4. Reconcile estimates without overwriting source values.
5. Validate the JSONL ledger.
6. Confirm that temporary detail/extended logging has ended.
