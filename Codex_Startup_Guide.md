# Codex Startup Guide

This is the umbrella guide for starting Codex in the SSO-MANAGE workspace.
It explains how to start Arthur, understand the agent system, and customize a
small, governed operating layer for a single downstream project.

## Purpose

Use this guide when you need a single entry point that explains:

- what to read first
- what each key directory is for
- how agents, skills, contracts, and truth sources fit together
- how to customize the operating layer for one project
- what not to train the agent to do
- when to be terse and when to be explicit in prompts

This guide is an orientation document, not a replacement for the governing
files. `AGENTS.md`, `AGENTS-master.md`, contracts, skills, and truth files
remain authoritative when this guide and another repository file disagree.

## Recommended Read Order

1. [`AGENTS.md`](AGENTS.md)
2. [`AGENTS-master.md`](AGENTS-master.md)
3. [`docs/agents/system/registry/Agent_System_Index.md`](docs/agents/system/registry/Agent_System_Index.md)
4. [`docs/agents/system/registry/Agent_Registry.md`](docs/agents/system/registry/Agent_Registry.md)
5. [`docs/agents/system/registry/Director_Routing_Matrix.md`](docs/agents/system/registry/Director_Routing_Matrix.md)
6. `truth/TRUTHS_INDEX.md` and relevant truth files, if present
7. The selected persona under [`skills/agents/`](skills/agents), matching contract under [`docs/agents/contracts/`](docs/agents/contracts), and required skill under `.agents/skills/*/SKILL.md`
8. [`docs/agents/system/runbooks/Startup_How_To_Guide.md`](docs/agents/system/runbooks/Startup_How_To_Guide.md)
9. [`docs/agents/system/runbooks/Extended_Logging_Runbook.md`](docs/agents/system/runbooks/Extended_Logging_Runbook.md)
10. [`docs/Template_Discipline.md`](docs/Template_Discipline.md)
11. [`docs/token-efficiency.md`](docs/token-efficiency.md)
12. Working handoff and resume files under [`docs/handoff/`](docs/handoff)
13. Recent logs under [`logs/`](logs), as context only

Do not load every persona, contract, or skill by default. Select the smallest
set that matches the request.

## Startup Permission and Approval Boundary

At initialization, explicitly request session-scoped read/write access to:

- the full resolved repository checkout; and
- `/tmp`, as a separate scope when temporary files or validation artifacts may
  be needed.

Repository policy can require this question, but it cannot grant host,
filesystem, IDE, or operating-system permissions. VS Code Workspace Trust is
not proof that Codex has either permission.

Richard's explicit approval is required before destructive file operations,
remote repository changes, credential use, publishing, or access-control
changes. Model names and agent personas do not grant permissions.

## Directory Roles

### `docs/`

Use for durable project knowledge, operating procedures, comparisons, indexes, runbooks, and handoffs.

### `logs/`

Use for append-only session logs and dated dialog records. Logs provide context and audit evidence; they do not override policy or truth files.

### `skills/`

Use for reusable agent skills, persona definitions, and behavior boundaries.

### `templates/`

Use for starter patterns, handoff templates, operating summaries, and repeatable project structures.

### `truth/`

Use for authoritative source-of-truth material that should override memory and
prompt drift. Start with `truth/TRUTHS_INDEX.md` when the directory exists.

### `config/`

Use for local identity values and runtime settings that should stay consistent across sessions.

### `scripts/`

Use for executable tooling. A script must be read and validated before its behavior is relied upon; a script is not authoritative merely because it exists.

## Agent Structure

The Manage model is layered:

- `AGENTS.md` defines the runtime entry point.
- `AGENTS-master.md` defines the shared policy baseline.
- `docs/agents/system/registry/Agent_Registry.md` defines which agents exist and what each one does.
- `docs/agents/system/registry/Director_Routing_Matrix.md` defines how work gets routed.
- `docs/agents/contracts/` defines what each agent is allowed to do.
- `skills/agents/` defines the persona and capability surface.
- `.agents/skills/*/SKILL.md` defines reusable workflow instructions and required
  operating constraints.

When adding a new agent:

1. Add or update the persona file under `skills/agents/`.
2. Add or update the matching contract under `docs/agents/contracts/`.
3. Register the agent in `docs/agents/system/registry/Agent_Registry.md`.
4. Route it in `docs/agents/system/registry/Director_Routing_Matrix.md` if it has a distinct responsibility.
5. Run the governance reference check documented in [`docs/agents/system/governance/Agent_Governance_Audit.md`](docs/agents/system/governance/Agent_Governance_Audit.md).

The repeatable validation command is:

```bash
python3 scripts/verify_agent_governance.py
```

Run it at least monthly and whenever contracts, personas, skills, routing,
truth references, or logging policy changes.

## Multiple Agents and Skillsets

Use multiple agents only when the work is genuinely separable.

- Choose one agent per bounded responsibility.
- Avoid making several agents read the same broad context unless the overlap is unavoidable.
- Use skills when the workflow repeats often enough to deserve a stable interface.
- Use contracts when the behavior needs guardrails.

Good examples:

- one agent gathers inventory while another writes documentation
- one skill normalizes links while another validates repo metadata
- one contract governs high-risk operations while another handles routine docs

Poor examples:

- splitting a narrow task across several agents
- using agents to compensate for missing state files
- training an agent to do everything by default

## What Not To Train

Do not train the agent to:

- rely on memory instead of files
- skip logging or overwrite history
- make destructive changes without approval
- expand scope silently
- infer facts that should come from truth files
- treat prompt verbosity as a substitute for durable documentation

## Prompt Style

Be prosaic when:

- asking for a durable plan
- defining policy
- documenting procedure
- describing a repo or system for future reuse

Be terse when:

- asking for a direct command
- confirming a narrow operational fact
- requesting a simple file change
- checking status or progress

The rule is simple: write enough detail to prevent drift, but not so much that the prompt becomes its own source of confusion.

## First Session With Arthur

Begin with a bounded request that identifies the goal, context, inputs,
constraints, and desired output. For example:

```text
Goal: help me understand this repository before I make changes.
Context: I am a new analyst working in <project path>.
Inputs: README.md, AGENTS.md, and the current project tree.
Constraints: read-only inspection; do not change files or contact remote services.
Output: summarize the project purpose, authoritative files, likely work areas,
and the next three safe actions.
```

Then ask Arthur to identify the responsible agent, contract, and skill before
specialized work begins. Ask for a plan and validation approach before any
material change.

## Customizing Arthur For One Project

For a single downstream project, use the smallest useful operating layer:

1. Decide whether durable handoffs, truth sources, routing, or logs justify
   adopting Manage. A tiny one-off task may not need it.
2. Use [`docs/Project_Bootstrap_Guide.md`](docs/Project_Bootstrap_Guide.md) and
   `scripts/spawn_project.py` when a new local scaffold is appropriate.
3. Create the downstream `AGENTS.md` and identify its project-specific
   `AGENTS-master.md` or equivalent policy source.
4. Record the project's owner, managing-agent identity, repository boundaries,
   truth sources, validation commands, and approval requirements.
5. Add only the personas, contracts, and skills the project actually needs.
6. Register and route any new agent, then run the governance validator.
7. Create a handoff/resume pair before substantial work begins.

Do not copy Richard's identity, local paths, credentials, logs, or
SSO-MANAGE-specific truth files into another project. Treat SSO-MANAGE as the
operating reference and customize the downstream project deliberately.

For the broader adoption decision, read
[`Arthur_Integration_How_To.md`](docs/agents/system/runbooks/Arthur_Integration_How_To.md).

## Analyst-Oriented Companion Material

Analysts doing governed Oracle/PeopleSoft work should also read the
[`New Analyst Reference Guide`](docs/reference/New_Analyst_Reference_Guide.md).
It explains metadata provenance, read-only boundaries, source-of-truth
distinctions, and usage accounting. The repository Markdown files remain the
authoritative sources; generated PDFs are reference copies and may become
outdated.

## Key Companion Docs

- [`docs/agents/system/runbooks/Startup_How_To_Guide.md`](docs/agents/system/runbooks/Startup_How_To_Guide.md)
- [`docs/Manage_Runbook.md`](docs/Manage_Runbook.md)
- [`docs/agents/system/runbooks/Arthur_Integration_How_To.md`](docs/agents/system/runbooks/Arthur_Integration_How_To.md)
- [`docs/Template_Discipline.md`](docs/Template_Discipline.md)
- [`docs/token-efficiency.md`](docs/token-efficiency.md)
- [`docs/agents/system/runbooks/Extended_Logging_Runbook.md`](docs/agents/system/runbooks/Extended_Logging_Runbook.md)
- [`docs/Project_Bootstrap_Guide.md`](docs/Project_Bootstrap_Guide.md)
- [`docs/reference/New_Analyst_Reference_Guide.md`](docs/reference/New_Analyst_Reference_Guide.md)

## Operating Summary

This guide is the umbrella. If a new session starts and the question is “what do I read first and why?”, start here, then follow the ordered list above.
