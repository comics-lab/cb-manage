# Comic-management expansion plan

Date: 2026-11-05
Status: Proposed — awaiting approval before installation or deployment

## Updated deployment constraint

The test deployments must use the existing shared media roots rather than
application-created library trees:

- Comics: `/mnt/phoenix/media/comics`, matching Kavita and Mylar.
- Books/ebooks: `/mnt/phoenix/media/books`, matching the existing Calibre library
  where an application supports ebooks.
- Application state may use separate service directories under
  `/mnt/phoenix/services/<application>`; these are not library roots.

CLU Comics and Codex must not initialize a second copy, import tree, or parallel
library structure. Their first mounts should be read-only against the shared comic
library. Writable mounts require a later explicit test gate.

## Objective

Evaluate and, if appropriate, integrate CLU Comics, Comicbox, and Codex into
CB-MANAGE as the comicbook management, library, metadata, and record-management
layer. Preserve Cirrus as the host-local implementation and deployment source.

## What the proposed tools can close

| Comparison gap | CLU Comics | Comicbox | Codex | Result |
| --- | --- | --- | --- | --- |
| Archive inspection and format handling | Possible; verify | Strong; reads/writes common comic formats | Uses Comicbox internally | Likely closes with contract and tests |
| ComicInfo/MetronInfo normalization | Verify | Strong; metadata synthesis and writing | Browser editing and tagging | Strong candidate; guardrails required |
| Online metadata matching | Verify | Metron/ComicVine tagging | Online tagging through Comicbox | Candidate, subject to rate limits and review |
| Library browsing/reading/OPDS | Possible; verify | Not its primary role | Strong | Codex provides a concrete reader/library target |
| Provenance and source-of-truth governance | No | No | No | Must be supplied by CB-MANAGE |
| Acquisition, wanted issues, downloader orchestration | Unknown/insufficient evidence | No | No | Mylar3 remains required unless another acquisition system is selected |
| Agent routing, contracts, audit, rollback | No | No | No | Must be built in CB-MANAGE |

Comicbox and Codex materially reduce the implementation gap, but they do not
eliminate the need for the CB-MANAGE agent framework or prove that Codex replaces
Mylar3. The first target should be “Codex plus existing acquisition workflow,”
followed by a controlled comparison against Mylar3.

## Phase 0 — approval and safety gate

1. Approve this plan and identify the test library root.
2. Confirm that all tests use a disposable copy or a staging subset, never the
   authoritative comic library.
3. Confirm whether installation should be Docker-only and which host owns the
   services.
4. Confirm whether CLU Comics should be installed for evaluation only or enabled
   as a live library manager.
5. Record current Mylar3, Kavita, and storage state before adding services.

No production files, database rows, reverse-proxy routes, or existing containers
will be modified before this gate is approved.

## Phase 1 — evidence and compatibility review

1. Pin current releases/commits for CLU Comics, Comicbox, and Codex.
2. Read their installation, metadata, API, storage, permissions, and upgrade docs.
3. Record supported archive formats, metadata schemas, online sources, rate limits,
   authentication, filesystem-watcher behavior, and rename semantics.
4. Compare their metadata output with the CB-MANAGE metadata contract and current
   ComicInfo v2 / MetronInfo formats.
5. Identify license, container image, CPU/RAM, and database requirements.

## Phase 2 — CB-MANAGE foundation

Create and register these bounded contracts and skills before enabling mutating
operations:

- External Source Researcher
- Archive Inspector
- Metadata Resolver
- Metadata Materializer
- Comic Library Ingest
- Reader/Library Adapter
- Reading List and Record Manager
- Acquisition Handoff / Mylar Adapter
- Test and Reconciliation Agent

Every mutating contract must require:

- dry-run plan;
- source, match, confidence, and provenance fields;
- schema validation;
- explicit disposition (`accepted`, `review`, `rejected`, or `quarantined`);
- rollback or untouched-original path;
- machine-readable result record;
- no silent rename, overwrite, deletion, or remote API concurrency.

## Phase 3 — install evaluation tooling

1. Install Comicbox in an isolated environment or pinned container.
2. Install CLU Comics in an isolated evaluation deployment if its current docs
   support a safe reproducible installation.
3. Install Codex using the official image or pinned native package, with its test
   library mounted read-only initially.
4. Do not expose any service through the public reverse proxy during the first
   evaluation.
5. Capture logs, versions, configuration, ports, volumes, and health checks.

## Phase 4 — non-mutating test matrix

Use a representative staging set containing clean archives, missing metadata,
conflicting ComicInfo/MetronInfo, malformed archives, alternate editions, and
reading-list references.

Measure:

- scan time and stability;
- supported formats;
- metadata extraction accuracy;
- ComicInfo.xml and MetronInfo.xml preservation/writing;
- Metron/GCD/ComicVine matching behavior;
- duplicate detection;
- series/volume/issue grouping;
- PDF and CBZ handling;
- OPDS behavior and Panels compatibility;
- database recovery and rescan behavior;
- logs and failure disposition.

## Phase 5 — controlled write tests

1. Work on copies only.
2. Permit Comicbox metadata writes for a small approved sample.
3. Validate archive readability before and after.
4. Compare generated metadata against GCD, Metron, existing local cache, and the
   CB-MANAGE contract.
5. Test Codex browser editing and online tagging with remote calls disabled or
   tightly limited first.
6. Test rename previews before enabling any rename.
7. Reconcile Codex’s library view with Kavita and Mylar3 without allowing multiple
   applications to own the same rename/move operation.

## Phase 6 — Codex versus Mylar3 decision

Codex can be considered a Mylar3 replacement only if it can satisfy the separately
tested acquisition requirements: wanted-issue tracking, provider/download
coordination, post-download handoff, rescan, rename, failure recovery, and API or
automation support. Its documented strengths as a reader, scanner, metadata editor,
online tagger, and OPDS server are not sufficient by themselves.

The likely near-term architecture is:

```text
Mylar3 or another acquisition tool -> CB-MANAGE intake/materialization -> Comicbox
metadata engine -> Codex/Kavita reader libraries -> OPDS clients such as Panels
```

## Required approval

Approve or revise the following before Phase 1 installation work begins:

- staging root for test archives;
- host and deployment method;
- whether CLU Comics is evaluation-only or may become an active manager;
- whether Codex may receive a writable staging library after read-only tests;
- whether existing Mylar3 remains active during comparison;
- whether public proxy exposure is prohibited until final acceptance.
