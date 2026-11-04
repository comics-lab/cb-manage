# CB-MANAGE

Pinky’s Brain: the Comic Book Super Organizer.

CB-MANAGE is the management and knowledge workspace for the electronic comic
book archive and its related software repositories. It provides durable
operating instructions, agent routing, logging, and project documentation. It
is not the comic archive application itself.

## Table of Contents

- [Purpose and current status](#purpose-and-current-status)
- [Start here](#start-here)
- [What is implemented](#what-is-implemented)
- [Repository map](#repository-map)
- [Skills and agents](#skills-and-agents)
- [Logging and usage accounting](#logging-and-usage-accounting)
- [Planned work](#planned-work)
- [Wiki and discussions](#wiki-and-discussions)
- [Construction record](#construction-record)

## Purpose and Current Status

CB-MANAGE is intended to coordinate a collection of comic archive and software
repositories. Planned utility work may include organizing and renaming comic
files, converting archive formats such as CBR/CBZ, and maintaining project
documentation. Those utilities are not implemented yet.

The initial repository structure and privacy-preserving logging subsystem are
in place. Broader project-specific agent roles, repo-management tools, and
comic archive utilities remain planned work.

## Start Here

For a new Codex session:

1. Read [`AGENTS.md`](AGENTS.md), then [`AGENTS-master.md`](AGENTS-master.md).
2. Read [`Codex_Startup_Guide.md`](Codex_Startup_Guide.md).
3. Review the [agent system index](docs/agents/system/registry/Agent_System_Index.md)
   and [construction record](docs/agents/chats/cb_manage_repository_construction.md).
4. Read the relevant persona, contract, and skill for the task.
5. Check `git status` and the current handoff before changing files.

Pinky is the CB-MANAGE managing-agent identity. Arthur remains the SSO-MANAGE
identity; do not carry Arthur-specific identity or SSO-MANAGE truth into this
repository unless a future decision explicitly calls for it.

## What Is Implemented

- Repository scaffold and non-secret project configuration in
  [`config/local.yaml`](config/local.yaml).
- Repository Codex lifecycle hooks in [`.codex/hooks.json`](.codex/hooks.json).
- A privacy-preserving usage-accounting skill, persona, and contract.
- Human-readable daily/topic logging policy and structured event/usage
  accounting procedures.
- JSON schemas, Python capture/record/validate/report scripts, regression tests,
  an initial event ledger, and generated aggregate reports.
- Initial agent registry, routing matrix, and system index.
- A running repository construction record.

The current reporting ledger records lifecycle metadata and decisions. It has
no token usage records yet, so usage and cost totals remain unknown/unpriced.

## Repository Map

| Path | Purpose | Current state |
| --- | --- | --- |
| `AGENTS.md`, `AGENTS-master.md` | Runtime entrypoint and shared policy | Initial outlines with logging rules; broader operating content remains to be completed |
| `.agents/skills/` | Codex-discoverable repository skills | `agent-usage-accounting` is installed |
| `skills/agents/` | Agent persona documents | Usage-accounting persona is installed |
| `docs/agents/contracts/` | Agent contracts | Usage-accounting contract is installed |
| `docs/agents/system/registry/` | Agent inventory, routing, and system map | Initial logging-focused registry is present |
| `docs/agents/system/runbooks/` | Operating procedures | Logging and usage-accounting runbooks are present |
| `docs/agents/system/schemas/` | Structured record schemas | Event and usage schemas are present |
| `docs/agents/chats/` | Append-only topic records | Topic template and repository construction record are present |
| `config/` | Non-secret project identity and runtime defaults | `local.yaml` is present |
| `.codex/` | Repository Codex hooks | Lifecycle capture hooks are present; hooks need review/trust in Codex |
| `scripts/`, `tests/` | Local tooling and checks | Usage-accounting tools and tests are present |
| `logs/` | Daily logs, event ledger, usage records, and reports | Initial daily/event records and reports are present |
| `docs/handoff/` | Handoff and resume files | Directory exists; initial handoff/resume pair is planned |
| `truth/` | Approved and candidate source records | Truth index and source architecture are initialized; eleven candidate URLs are listed for review, none promoted to authoritative status |
| `.github/` | GitHub workflows and helpers | Wiki/discussion automation is not installed |

## Skills and Agents

The active registry is [`Agent_Registry.md`](docs/agents/system/registry/Agent_Registry.md);
requests are routed by [`Director_Routing_Matrix.md`](docs/agents/system/registry/Director_Routing_Matrix.md).
Currently, the usage-accounting agent is the only installed specialist. Add
agents, contracts, and skills as CB-MANAGE responsibilities become concrete.

Repository skills live under `.agents/skills/<skill-name>/`. Persona files live
under `skills/agents/`; contracts live under `docs/agents/contracts/`.

## Logging and Usage Accounting

The [extended logging runbook](docs/agents/system/runbooks/Extended_Logging_Runbook.md)
defines daily/topic logging, session-scoped detail modes, error escalation, and
redaction. The [invocation and accounting runbook](docs/agents/system/runbooks/Agent_Invocation_and_Accounting_Runbook.md)
documents lifecycle events, usage records, validation, and reports.

Useful commands:

```bash
python3 scripts/record_agent_event.py --help
python3 scripts/validate_agent_ledger.py logs/agent_events/agent-events.jsonl
python3 scripts/validate_agent_ledger.py --kind usage logs/usage/usage.jsonl
python3 scripts/report_agent_usage.py
python3 -m unittest tests/test_agent_usage_tracking.py
```

Review and trust `.codex/hooks.json` with Codex’s `/hooks` command, then start a
new session to verify automatic lifecycle capture. The hooks record allowlisted
metadata; they are not a transcript logger.

## Planned Work

- Complete CB-MANAGE operating policy and startup instructions.
- Define the comic archive repositories, their owners, boundaries, and
  authoritative truth sources.
- Add only the agent personas, contracts, and skills needed for those projects.
- Build a first handoff/resume pair and validate a fresh-session reconstruction.
- Design and test comic archive utilities after their input/output rules are
  established.
- Decide later whether wiki publication or discussion workflows are useful.

Progress and decisions are tracked in the
[CB-MANAGE repository construction record](docs/agents/chats/cb_manage_repository_construction.md).

## Wiki and Discussions

GitHub Wiki and Discussions are enabled for the repository. Automated wiki
publishing is not configured; the README and documentation are currently
maintained in Git. Discussions may be used for project conversation, but no
repository-specific discussion workflow has been defined.

## Construction Record

The [construction record](docs/agents/chats/cb_manage_repository_construction.md)
is the running outline of completed setup, open work, and validation evidence.
Update it as repository structure and operating capabilities are added. The
initial truth registry is in place. Candidate comic archive and software URLs
are recorded in the external manifest; their authority remains unverified.
