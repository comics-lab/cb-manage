# Metadata Staging and Comicbox Intake Workflow

## Purpose

This document defines a safe workflow for combining CBL-ReadingLists,
ComicVine, Metron, GCD, ISBN, Library of Congress, Amazon, existing archive
metadata, and other collector-relevant sources before materializing metadata into
comic archives.

The objective is not to make every endpoint application a metadata authority. The
objective is to preserve source evidence, resolve identity and conflicts once,
normalize approved records through Comicbox, and then produce compatible outputs
for Codex, Mylar3, Kavita, Komga, and other consumers.

## System boundary

Comicbox should be the normalization and metadata-materialization engine.
Comicbox Doctor should validate dependencies, archives, configuration, and output
prerequisites.

The Cirrus-developed Python tools should remain responsible for source ingestion,
cache refresh, matching, confidence, provenance, reports, review queues, and
promotion control.

Codex, Mylar3, Kavita, and Komga should remain downstream consumers. Their
databases should not be treated as a shared metadata staging area.

Comicbox does not appear to provide a generic database into which every source
should be dumped. Its canonical record is a normalized metadata model that can be
serialized to Comicbox JSON/YAML and projected into `ComicInfo.xml` or
`MetronInfo.xml`.

## Proposed data flow

```text
Raw sources
  ├─ CBL-ReadingLists
  ├─ ComicVine extracts/API
  ├─ Metron extracts/API
  ├─ GCD snapshot
  ├─ ISBN / Library of Congress
  ├─ Amazon or other retail metadata
  └─ existing embedded metadata
        ↓
Source-specific immutable caches
        ↓
Canonical identity and matching ledger
        ↓
Comicbox normalized metadata record
        ↓
Comicbox Doctor validation
        ↓
Human review for conflicts
        ↓
ComicInfo.xml + MetronInfo.xml + optional comicbox.json
        ↓
CBZ archive write
        ↓
Cirrus audit and promotion
        ↓
Codex / Kavita / Komga / Mylar scans
```

## Recommended workflow

### 1. Refresh source caches

Import or refresh each source independently:

- CBL-ReadingLists
- local GCD data
- Metron extracts or API responses
- ComicVine extracts or API responses
- ISBN and Library of Congress records
- Amazon or other retail metadata
- existing ComicInfo, MetronInfo, `series.json`, and filename evidence

Raw source records must remain immutable. A normalized or corrected value must not
overwrite the original source record.

### 2. Build a canonical identity ledger

Each candidate comic should receive a record containing:

- source identifiers
- candidate series, title, issue, year, and publisher
- edition and format data
- source confidence
- provenance for every significant field
- competing matches
- conflict state
- approved canonical identity, when resolved

This ledger is necessary for cases such as one ComicVine ID appearing under
several series labels, or a GCD issue matching multiple Metron records.

### 3. Resolve local evidence before remote APIs

The default precedence should be:

1. approved local metadata
2. exact identifiers embedded in the archive
3. local GCD data
4. local Metron and ComicVine caches
5. CBL reading-list relationships
6. ISBN and Library of Congress data
7. retail metadata such as Amazon
8. live ComicVine or Metron requests

Remote requests remain sequential, cached, and rate-limited. No concurrency should
be used to defeat provider throttles.

### 4. Generate a saved materialization plan

Before changing an archive, create a JSON plan containing:

- input CBZ path and hash
- proposed destination
- proposed canonical metadata
- source selected for each field
- confidence and conflicts
- output formats
- intended action

The plan becomes the execution boundary. Retries should replay the plan rather
than repeatedly rereading and re-resolving the same archive.

### 5. Normalize and serialize with Comicbox

Approved canonical patches should be passed to Comicbox. The preferred outputs
are:

- Comicbox JSON/YAML for the richest preservation record
- MetronInfo.xml for the richer portable comic schema
- ComicInfo.xml as a compatibility projection for Mylar, Kavita, Komga, and
  other readers

The safe direction is:

```text
canonical Comicbox record
    ├─→ MetronInfo.xml
    ├─→ ComicInfo.xml
    └─→ optional comicbox.json or comicbox.yaml
```

ComicInfo is not rich enough to be the sole canonical source for all fields in
MetronInfo or Comicbox.

### 6. Run Comicbox Doctor

Doctor should run before batch processing and against representative output
fixtures. Check:

- installed dependencies
- archive readability
- image and page validity
- metadata configuration
- online-source configuration
- output and write prerequisites

### 7. Run Cirrus validation

Cirrus validation should cover:

- CBZ inventory and structural validity
- ComicInfo and MetronInfo consistency
- ComicVine ambiguity
- GCD and local-cache matching
- filename and directory policy
- provenance and disposition
- Mylar, Kavita, Komga, and Codex readiness separately

### 8. Materialize archives only after approval

Write metadata into the CBZ only when:

- the archive is structurally valid
- identity confidence meets policy
- conflicts are resolved or explicitly accepted
- provenance is recorded
- the operation exists in the saved materialization plan

Writes should be atomic, reversible where practical, and followed by a validation
report.

### 9. Promote to endpoint applications

Maintain independent readiness states:

- `kavita_ready`
- `komga_ready`
- `codex_ready`
- `mylar_ready`

A book can be valid for Kavita or Codex while remaining unsuitable for Mylar if it
lacks a trustworthy ComicVine issue identifier.

## Proposed staging ledger

The missing shared layer should be implemented outside the endpoint databases:

```text
metadata_staging/
  raw_sources/
  source_records/
  canonical_records/
  materialization_plans/
  reports/
  conflicts/
```

The logical record model should include tables or equivalent structured files for:

```text
raw_sources
source_records
candidate_matches
canonical_records
field_provenance
conflicts
materialization_plans
materialization_events
```

Every field that changes the identity or classification of a comic should be able
to answer:

- where did this value come from?
- when was it obtained?
- what competing values existed?
- who or what approved it?
- which output files received it?

## Current components

The architecture can be assembled from existing pieces:

- Comicbox: canonical normalization, schema transforms, online lookup, validation,
  and archive writing
- Comicbox Doctor: dependency, archive, and configuration diagnostics
- `prepass_normalize.py`: local sidecar/cache prepass and initial organization
- `metadata_consistency_enrich.py`: ComicInfo/MetronInfo audit and enrichment
- `pass1_write_comicinfo.py`: conservative high-confidence ComicVine tagging
- `mylar_v3_buildout.py`: Mylar-oriented naming, sidecars, XML generation, and
  promotion
- `cbz_audit.py`: archive and metadata readiness audit
- local GCD/CBL/ComicVine ambiguity and resolution utilities

The existing architecture notes are in
`docs/metadata/Comicbox_Architecture_and_Workflows.md`.

## Remaining implementation work

The main missing pieces are:

1. a unified source-adapter interface;
2. immutable raw-source cache storage;
3. a canonical identity and matching ledger;
4. a field-level precedence policy;
5. a saved JSON materialization plan;
6. a Comicbox adapter for approved canonical patches;
7. source-license and attribution tracking;
8. conflict-resolution tooling;
9. one batch orchestrator joining Doctor, Comicbox, and Cirrus reports.

The saved-plan boundary is the highest-priority implementation because it prevents
repeated rescans, makes retries deterministic, and provides a reviewable record of
what will be written before any CBZ is modified.

## Storage and ownership rule

SQLite is common among the endpoint applications, but their schemas and migration
rules are independent. Do not point two applications at the same SQLite database.
Share media archives and deliberately generated metadata files; keep each
application's database private.
