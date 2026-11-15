# Comic Library Application and Tool Evaluation Queue

Updated: 2026-09-25

This document preserves the current Cirrus comic-application inventory and the
future tools that need to be examined, tested, and possibly integrated. An item
marked `evaluation status unknown` has not been confirmed as previously evaluated;
do not treat its presence in older notes as a completed assessment.

## Current installed and running applications

| Application | Current state | Role |
| --- | --- | --- |
| Mylar 3 | Installed and running | Comic acquisition, import management, and library writing |
| Kavita | Installed and running | Read-only comic-library reader and presentation layer |
| Calibre | Installed and running | EPUB library, content server, and OPDS candidate |
| JDownloader2 | Installed and running | Download intake |

Current Compose locations:

```text
/srv/compose/mylar3
/srv/compose/kavita
/srv/compose/calibre
/srv/compose/jdownloader2
/srv/compose/komga
/srv/compose/transmission
```

## Prepared but not running

| Application | Current state | Remaining work |
| --- | --- | --- |
| Komga | Compose prepared; no running container | Review configuration, initialize, start read-only, and test library behavior |
| Transmission | Compose prepared; no running container | Review credentials, download paths, permissions, and bandwidth policy before startup |

## Previously identified but not deployed

| Tool or service | Status | Planned purpose |
| --- | --- | --- |
| `clu-comics` | Investigated; not deployed | Possible Mylar replacement or complementary intake/metadata service |
| Calibre-Web / COPS | Not installed | OPDS and web-reader comparison for Panels and other clients |
| AirDC++ client | Not installed | Alternative acquisition source |
| Usenet client | Not installed | Alternative acquisition source; client selection remains open |

## New evaluation queue

The following items were added on 2026-09-25. Their prior evaluation status is
currently unknown and must be verified from project documentation, source code,
and reproducible tests.

| Item | Reference | Initial evaluation questions |
| --- | --- | --- |
| Codex GitHub project | `github:codex` | Identify the exact repository, scope, license, comic-library relevance, and whether it is an application, agent, or integration component |
| Comicbox | `github:comicbox` | Determine archive inspection, metadata extraction, ComicInfo/Metron support, CLI/API behavior, and overlap with Cirrus helpers |
| Comicalibre | `github:comicalibre` | Determine whether it is a Calibre integration, comic metadata tool, reader, or library manager; test supported formats and OPDS implications |
| BigIron comic-library metadata guide | [Comic library metadata, ComicVine scraping, and ComicInfo.xml](https://www.bigiron.cc/guides/comic-library-metadata-comicvine-scraping-and-comicinfo-xml) | Compare its metadata model, ComicVine scraping approach, rate-limit behavior, XML mappings, and safety against the Cirrus metadata contract |
| Rager's Comic Importer | [itch.io project](https://thomas-rager.itch.io/ragerscomicimporter) | Test supported sources, archive formats, metadata providers, naming rules, duplicate handling, and compatibility with Mylar/Kavita/Komga |
| Kapowarr | `kapowarr` | Evaluate as an acquisition and automation alternative to Mylar; inspect metadata sources, download clients, post-processing, Docker support, and migration path |

## Evaluation order

Evaluate each candidate in this order:

1. Identify the exact upstream repository or release and confirm license, version,
   maintenance activity, and supported platform.
2. Read documentation and inspect source/configuration before running it.
3. Compare archive, metadata, identifier, naming, and provenance behavior with
   the Cirrus comic metadata contract.
4. Test only against disposable copies or a small read-only sample set.
5. Record network/API behavior, rate limiting, credentials, write paths, and
   failure/rollback behavior.
6. Test interoperability with Mylar, Kavita, Komga, Calibre, Panels, ComicInfo,
   MetronInfo, CBL, GCD, and ComicVine as applicable.
7. Classify the result as `adopt`, `complement`, `keep for reference`, `defer`,
   or `reject`, with evidence and a rollback plan.

## Existing helper inventory

The current Cirrus helper library includes:

- Calibre import, lookup, removal, startup, and cover-update helpers.
- Mylar v3 tree/buildout and import helpers.
- ComicInfo/Metron metadata enrichment and batch processing.
- CBZ audit, normalization, conversion, promotion, and quarantine tools.
- ComicVine ambiguity verification.
- CBL cache construction, refresh, matching, and reporting.
- Local metadata-to-ComicVine resolution.
- Series metadata seeding and legacy metadata conversion.

## Immediate queue before new integrations

1. Finish Mylar configuration and controlled-import validation.
2. Decide whether Komga is needed alongside Kavita; if so, initialize it and test
   it against the read-only comic library.
3. Review Transmission credentials, paths, permissions, and bandwidth policy.
4. Test Calibre OPDS/content-server behavior with Panels.
5. Compare Kavita, Komga, and Calibre/OPDS for comic discovery and reading.
6. Continue the `clu-comics` replacement analysis before changing the production
   Mylar workflow.
7. Complete and validate the 2000 AD metadata materialization cycle.
8. Begin the new candidate evaluations above, starting with tools most likely to
   overlap with metadata intake or Mylar replacement.

## Evidence and decision records

Each evaluation should produce a dated report under this directory containing:

- exact project URL and version;
- license and maintenance observations;
- installation/test method;
- input and output paths;
- metadata fields and identifier behavior;
- API/network and rate-limit behavior;
- results against disposable test data;
- compatibility findings;
- security, permissions, and rollback notes;
- final recommendation and confidence.

Existing related documents:

- [`00-investigation-log.md`](00-investigation-log.md)
- [`01-execution-plan-draft.md`](01-execution-plan-draft.md)
- [`02-clu-capability-assessment.md`](02-clu-capability-assessment.md)
- [`03-script-library-plan.md`](03-script-library-plan.md)
- [`../comicvine-ambiguity-verification.md`](../comicvine-ambiguity-verification.md)
- [`../comic-metadata-intake-contract.md`](../comic-metadata-intake-contract.md)
