# Stage-01 Role Response Workflow

`/mnt/phoenix/media/incoming/jdownloader` is the initial source for the file-driven
Stage-01 coordination area. It accepts complete, closed `.cbr`, `.cbz`, and `.pdf`
payloads and is upstream of the Mylar import basket.

## Current Role Directories

The current eight role directories are:

```text
archive-inspector
comicinfo-resolver
duplicate-analyst
metadata-materializer
metroninfo~specialist
migration-specialist
mylar-hand-off
application-services
```

The spelling, including `metroninfo~specialist` and `mylar-hand-off`, is part of the
current filesystem contract unless the directories are deliberately renamed and all
watchers are updated together.

## Queue Contract

Each role directory should contain these subdirectories:

```text
<role>/source/       input files or trees waiting for this role
<role>/working/      atomically claimed work; agents do not watch this directory
<role>/output/       completed work and a machine-readable result record
<role>/review/       ambiguous or unsafe work requiring human review
<role>/error/        processing failures with an error record
```

Only `source/` is a watch directory. Agents must claim a file or directory by moving
it into `working/` on the same filesystem before processing. This prevents two agents
from processing the same item. A result must be written before the item is moved out
of `working/`.

## File Movement Rules

- Never overwrite an existing destination file or directory.
- Preserve the original relative path, filename, hash, source, and timestamps in the result.
- Successful output moves to the next role's `source/` directory.
- Ambiguous work moves to the current role's `review/` directory.
- Unexpected failures move to the current role's `error/` directory.
- A move is not success by itself; the result record must state the disposition.
- Agents must be idempotent: rerunning an already completed item must not create copies.
- CBL source files and canonical cache rows are never changed automatically.

## Role Boundaries

The first transition is special: Archive Inspector consumes raw JDownloader payloads,
including nested archive bundles, and creates normalized CBZ series directories before
handing them to the resolver. Its detailed contract is in
[`Agent_Contracts/Archive_Inspector_Agent.md`](Agent_Contracts/Archive_Inspector_Agent.md).
Series metadata follows the contract's local-first precedence: current media tree, CBL
cache, GCD, Metron API, and ComicVine API last.
For XML materialization, embedded `ComicInfo.xml` is extracted first; `series.json` seeds
the document only when embedded XML is absent. The external `CV-...-CVID.xml` proposal is
created only after the ComicVine issue ID has been resolved.

| Role directory | Watches for | Performs | Sends successful work to |
| --- | --- | --- | --- |
| `archive-inspector` | Complete, closed CBR/CBZ/PDF payloads from JDownloader | Nested unpack, CBR/PDF to CBZ conversion, page validation, publisher/series directory, `series.json`, and `cvinfo` creation | `comicinfo-resolver/` |
| `comicinfo-resolver` | Valid archives lacking reliable identity | Sidecar/cache/local identity resolution; rate-limited remote lookup when approved | `duplicate-analyst/source` |
| `duplicate-analyst` | Resolved archives | Hash, normalized-name, and edition comparison | `metadata-materializer/source` |
| `metadata-materializer` | Approved identity records | ComicInfo XML and naming/tree materialization | `metroninfo~specialist/source` |
| `metroninfo~specialist` | ComicInfo-complete archives | MetronInfo creation/update and validation | `mylar-hand-off/source` |
| `migration-specialist` | Explicit transfer batches | Compare or migrate stable utilities, reports, and contracts | Declared migration destination; never implicit |
| `mylar-hand-off` | Fully validated archives | Final Mylar eligibility check and controlled promotion | Mylar import basket |
| `application-services` | Explicit service tasks | Mylar/Kavita scans, API calls, and log verification | Application state/report; not another archive queue |

## Agent Loop

Every watcher follows this loop:

1. Poll only its role's `source/` directory.
2. Claim one item into `working/` using an atomic rename.
3. Read the applicable contract, policy, and prior result records.
4. Inspect and process locally; keep remote ComicVine requests sequential and cached.
5. Write a result record containing status, source, destination, hashes, counts, warnings,
   and timestamps.
6. Move the item to the next role, `review/`, or `error/`.
7. Leave a concise append-only log entry.

The watcher must not repeatedly rescan the entire library. Queue state and result records
are the source of progress. A retry must use the saved result and increment a retry count.

## Gates

An archive may advance only when the current role's acceptance gate passes:

- Inspector: readable CBZ with at least one comic page.
- Resolver: identity source and confidence recorded; ambiguity is review, not a guess.
- Duplicate analyst: no unresolved duplicate or edition conflict.
- Materializer: XML and path changes are written only from an approved resolution.
- Metron specialist: valid, internally consistent XML and preserved archive contents.
- Mylar handoff: `mylar_ready=true`; Kavita readability alone is insufficient.
- Application services: API response and post-scan logs recorded.

## Current State And Next Setup

The `_Stage-01` role directories exist, but source/output queue subdirectories were not
present in the initial inspection. Before enabling watchers:

1. Agree on the exact `source`, `working`, `output`, `review`, and `error` names.
2. Create those queue directories without moving production archives yet.
3. Add one watcher per role with a lock/claim mechanism and structured result records.
4. Test the full chain with one disposable CBZ.
5. Enable larger batches only after duplicate and rollback behavior is verified.

The existing batch scripts remain the controlled fallback until these watchers are tested.
