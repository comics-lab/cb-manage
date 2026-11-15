# Comics Expansion: Execution Plan Draft

## Objective

Evaluate `clu-comics` as a possible Mylar replacement and define a staged, reversible expansion of Cirrus's comic acquisition, metadata, storage, library, and reading services.

## Investigation order

1. Establish the current Cirrus truth: storage mounts, Mylar/Kavita state, intake scripts, metadata contracts, and existing databases.
2. Inventory every Cirrus shell and Python script, plus relevant `clu-comics` utilities. Record purpose, inputs, outputs, side effects, dependencies, permissions, dry-run behavior, failure modes, and a safe runnable example. Identify undocumented, duplicate, obsolete, and dangerous tools.
3. Inventory `clu-comics`: runtime, deployment model, configuration, database schema, file watcher, acquisition clients, provider abstractions, Metron integration, ComicInfo/`series.json` writers, APIs, OPDS, permissions, and test coverage.
4. Trace the end-to-end paths in source: wanted issue → provider lookup → download → conversion → metadata → rename/move → database/library state.
5. Compare those paths against Mylar's required behavior and Cirrus's existing Stage-01 contract.
6. Evaluate the reader/library path independently: Kavita, Komga, COPS/Calibre OPDS, and Panels on iPad. Test OPDS discovery, authentication, cover/title/series fields, pagination, CBZ/PDF download, resumability, file naming, progress/bookmarks, and behavior after a Mylar replacement.
7. Verify current Metron API documentation, authentication, pagination, conditional requests, rate-limit headers, dataset/export options, and any timing exclusions. Design a polite cache-first client; never assume “unlimited” means unrestricted.
8. Verify the current DieselTech metadata conventions and identify exactly what “series.json v2” and the updated ComicInfo template change. Treat unverified files as proposals until version and schema are confirmed.
9. Evaluate AirDC++ and Usenet components for fit, security, storage, licensing, maintenance, and integration boundaries.
10. Produce a recommendation: replace, coexist, or reject; include migration, pilot, rollback, acceptance criteria, and explicit “should” guidance.

## Proposed implementation phases

### Phase 0 — Evidence and contracts

- Freeze current Mylar/Kavita behavior as a baseline.
- Define canonical storage ownership and immutable source/provenance rules.
- Define a versioned JSON resolution/materialization plan shared by inspection, metadata, and promotion stages.
- Define metadata authority and conflict rules: local embedded metadata, GCD, CBL, Metron, ComicVine only where necessary.
- Capture API credentials and secrets only through the host's secret mechanism; never place them in this repository.

### Phase 1 — Read-only adapter

- Build an adapter around `clu-comics` or its data model without moving production files.
- Import a small inventory into an isolated test database and staging tree.
- Compare issue identity, series identity, edition handling, filenames, XML, duplicate decisions, and readiness flags against current reports.

### Phase 2 — Disposable pilot

- Use a disposable subset containing ordinary issues, TPBs, annuals, variants, missing metadata, duplicate editions, CBR/CBZ/PDF, and known Mylar edge cases.
- Run acquisition and materialization with network requests cached and bounded.
- Validate Mylar and Kavita compatibility independently.
- Require an operator-approved manifest before any promotion.

### Phase 3 — Coexistence

- Keep Mylar as rollback target while `clu-comics` handles only an explicitly scoped lane.
- Avoid two writers owning the same intake or library path.
- Reconcile databases and filesystem state through reports, not blind synchronization.

### Phase 4 — Decision and migration

- Replace Mylar only if the pilot meets functional, metadata, reliability, security, and rollback gates.
- Otherwise retain `clu-comics` as an acquisition/metadata companion or reject it for Cirrus.

## Service candidates

- Metron: likely metadata authority candidate, subject to documented rate limits, caching, attribution, and API policy.
- Calibre/COPS: reading/distribution experiment, not a comic-library authority; test OPDS and CBZ/PDF behavior separately.
- AirDC++: optional acquisition source; isolate downloads, credentials, ports, and incomplete files from the library.
- Usenet client: optional acquisition source; prefer a well-supported client with SABnzbd/Newznab-compatible integration if `clu-comics` supports it cleanly.

## Required deliverables before implementation

- Complete script library/catalog for Cirrus shell and Python tooling, with one documentation page or section and one safe example per tool.
- Architecture and dependency map.
- Mylar-vs-`clu-comics` capability matrix.
- Metron API and dataset policy note.
- Metadata schema/version comparison.
- Reader/library compatibility matrix for Kavita, Komga, COPS/Calibre OPDS, and Panels.
- OPDS contract and test results, including authentication and download behavior.
- Storage and permissions plan.
- Threat model and network exposure matrix.
- Pilot test catalog and acceptance criteria.
- Migration/rollback runbook.
- Final recommendation for each optional service.
