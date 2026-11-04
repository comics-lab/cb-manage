# Agent Logging Standard and Runbook

## Purpose and authority

This is the single active definition for CB-MANAGE agent logging. It combines
the topic-based logging standard with the basic, standard, merged
detail/verbatim, and extended operating rules.

Agents must use this document together with `AGENTS-master.md` and
`config/local.yaml`. Historical topic logs may refer to older policy wording;
they are records, not overrides.

Startup invariant: every new session begins in basic/standard logging mode.
Creating, reading, or appending a topic log never edits `config/local.yaml` and
never persists a temporary logging mode. Detail/verbatim and extended modes are
runtime session instructions only unless Richard explicitly declares a longer
timeframe.

## Logging framework

Logging is topic-based and append-only. The durable subject record lives under:

```text
docs/agents/chats/
```

Use one descriptive lowercase topic file per continuing subject, for example:

```text
docs/agents/chats/oracle_constraint_review.md
```

Create a topic file when a new investigation or concern begins. Append to the
existing file when the work continues the same subject. Before appending, read
the existing topic file so prior decisions, constraints, and open questions are
preserved.

The daily operational log remains separate:

```text
logs/Dialog_YYYY-MM-DD.md
```

The daily log is a concise session index. The topic log is the durable record
of a subject across sessions. Neither log may contain hidden reasoning,
credentials, secrets, unrestricted PII, or raw unrestricted database output.

## Required topic entry

Each topic file has one title and one current runtime-identity block near the
top. Every appended session should include:

```markdown
## Session — YYYY-MM-DD HH:MM America/Los_Angeles — Short summary

### User Prompt
Concise summary unless merged detail/verbatim logging is enabled.

### Agent Response
Concise outcome summary unless merged detail/verbatim logging is enabled.

### Artifacts / References
- Relative paths to relevant files
- Reports, decisions, and external references

### Code Changes
- Files changed and why, or `None`

### Validation
- Checks run and results

### Notes
- Decisions, trade-offs, and unresolved questions

---
**Agent**: <agent name / tool>
```

Use the project timezone and 24-hour timestamps. Corrections are additive;
do not rewrite earlier entries.

## Modes

### Basic and standard

Basic and standard mean the same default operating mode. `standard` is the
configuration name:

```yaml
logging_mode: "standard"
```

Record concise summaries of the prompt, outcome, artifacts, changes,
validation, decisions, and open questions. Do not record the prompt or response
verbatim unless merged detail/verbatim mode is explicitly enabled.

### Detail or verbatim (merged session mode)

“Detail logging” and “verbatim logging” are equivalent invocation phrases for
the same explicit, session-scoped mode. Either phrase requests expanded context
and exact prompt/final-response capture. If no timeframe is stated, the mode
ends when the current session ends.

Either invocation is valid:

> Enable detail logging for topic `<topic>` for this session only.

> Enable verbatim logging for topic `<topic>` for this session only.

Create a secondary file:

```text
docs/agents/chats/<topic>__detail_YYYY-MM-DD.md
```

This merged mode includes expanded artifacts, decisions, validation, and open
questions. It captures the user prompt and final response verbatim. It does not
capture hidden reasoning, unrestricted tool transcripts, secrets, or raw
credentials. Link the secondary file from the standard topic entry.

### Extended

Extended logging includes everything in merged detail/verbatim mode plus timestamped
intermediate progress summaries, tool/command purposes, concise results, and
checkpoint validation.

Invocation:

> Enable extended logging for topic `<topic>` for this session only, including
> intermediate progress summaries and summarized tool actions.

Use:

```text
docs/agents/chats/<topic>__extended_YYYY-MM-DD.md
```

Extended logging is automatically enabled whenever an error or unresolved
inability to complete work occurs. Examples include missing files, failed
validation, blocked actions, tool failures, permission problems, or unresolved
ambiguity.

When automatic escalation occurs:

1. Notify Richard immediately and identify the condition without exposing
   secrets.
2. Record affected artifacts, attempted remedies, progress, and validation.
3. Continue extended logging until the condition is resolved.
4. Notify Richard when it is resolved; preserve an open condition in the
   handoff if it remains unresolved at session end.

The configuration default is off:

```yaml
verbatim_logging:  # compatibility key for the merged detail/verbatim mode
  enabled: false
```

The legacy configuration key remains for compatibility. An explicit request
using either “detail logging” or “verbatim logging” enables the same merged
session mode. That mode never authorizes hidden reasoning, unrestricted tool
output, secrets, credentials, or raw unrestricted database results.

## Mode precedence

Apply rules in this order:

1. Topic-based, append-only logging is always the framework.
2. Basic/standard applies unless another mode is requested.
3. Explicit detail/verbatim or extended requests override standard for their declared
   timeframe.
4. An unresolved error automatically escalates the current session to extended.
5. At session close, temporary modes end and standard logging resumes unless a
   longer timeframe was explicitly declared.

## Redaction and safety

Never log:

- passwords, tokens, API keys, cookies, or connection strings;
- hidden model reasoning;
- unrestricted tool transcripts;
- raw unrestricted database output;
- PII or Level 1 identity data unless explicitly approved, minimized, and
  redacted according to the applicable contract.

Use `[REDACTED]` for secret values and note that redaction occurred. Logging
mode does not expand filesystem, network, database, GitHub, or destructive-action
permissions.

## Compatibility

These rules apply equally to Codex CLI, VS Code, code-insiders, browser agents,
and other approved agents. No logger process is invoked automatically; the
active agent applies the standard when creating or updating the appropriate
daily and topic records.

## Exit checklist

1. Confirm the appropriate daily/topic log contains the requested fidelity.
2. Link any secondary detail or extended file from the standard topic entry.
3. Record artifacts, validation, decisions, and unresolved questions.
4. Confirm prohibited content was not recorded.
5. Close temporary detail/verbatim/extended mode and return to standard.
6. Apply archive eligibility rules later; do not archive current work.
