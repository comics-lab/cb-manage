# Cirrus and CB-MANAGE agents/skills comparison

Date: 2026-11-05

## Executive conclusion

CB-MANAGE currently provides governance, truth-record structure, logging, and a
usage-accounting agent. Cirrus provides the substantive comic-library operations
and host skills. CB-MANAGE should become the orchestration and record-management
home by importing or adapting Cirrus’s comic-specific contracts and skills, while
keeping Cirrus-specific host administration local to Cirrus.

## Current inventory

| Area | Cirrus | CB-MANAGE |
| --- | --- | --- |
| Agent contracts | Archive Inspector; ComicInfo Materializer; Comic Metadata Intake; Library Ingest; Mylar Handoff | Usage Accounting |
| Comic/archive skills | comic-archive-inspection; comic-metadata-intake; comicinfo-materialization; library-ingest; shared-library-storage | None yet |
| Host skills | host-hardening-baseline; host-resume-handoff; host-storage-baseline; host-truth-capture; service-baseline-review | None |
| Governance | AGENTS.md, local logs, source precedence and intake contracts | Master/entry instructions, truth architecture, registry, routing matrix, append-only event and usage ledgers |
| External truth | Distributed across Cirrus docs and reports | `truth/EXTERNAL/manifest.md` plus source records |

## Recommended CB-MANAGE target agents

1. Director / Router: classify requests and dispatch bounded specialists.
2. External Source Researcher: maintain manifest records and provenance.
3. Archive Inspector: validate CBZ/CBR/PDF/EPUB inputs and preserve provenance.
4. Metadata Resolver: apply local GCD, CBL, Metron, sidecar, and embedded metadata precedence.
5. Metadata Materializer: write and validate ComicInfo.xml and MetronInfo.xml from approved plans.
6. Library Ingest: stage, deduplicate, and promote archives with machine-readable reports.
7. Comic Library Manager: coordinate Mylar, Kavita, Komga, Codex, and OPDS boundaries.
8. Reading List / Record Manager: manage CBL lists, series records, identifiers, and provenance.
9. Host/Service Adapter: consume Cirrus host facts without becoming a general host administrator.
10. Usage Accounting: retain the existing CB-MANAGE governance role.

## Recommended migration order

1. Copy the Cirrus comic agent contracts into CB-MANAGE as adapted contracts, preserving Cirrus as the host-local implementation source.
2. Move or mirror the comic skills into CB-MANAGE with explicit scope and source precedence.
3. Add registry and routing entries for each specialist.
4. Make every mutating agent emit a plan, provenance record, result record, and rollback/disposition before promotion.
5. Keep host hardening, storage, and service-baseline skills in Cirrus; expose their conclusions through host capability records.
6. Link the external manifest/source records to resolver and materializer agents.
7. Add cross-repository tests for routing, schema validation, and append-only logging.

## Boundary decisions

- CB-MANAGE owns cross-application comic records, source authority, provenance, and orchestration.
- Cirrus owns Cirrus host state, deployment paths, service configuration, and host-local execution.
- No agent may silently overwrite authoritative source rows or rename production archives.
- Remote metadata requests remain rate-limited and cache-backed.

## Gaps to close

- CB-MANAGE needs a comic-agent registry and routing contracts.
- CB-MANAGE needs a shared metadata contract and archive result schema.
- Source records need periodic re-verification and version/commit pinning.
- Integration tests should cover Mylar-ready versus reader-only disposition.
