# CLU Capability Assessment — Initial

## Evidence reviewed

- `/home/rmleonard/Projects/clu-comics/README.md`
- `/home/rmleonard/Projects/clu-comics/FEATURES.md`
- `/home/rmleonard/Projects/clu-comics/docker-compose.yaml`
- `core/database.py`, `core/file_watcher.py`, `core/metadata_scanner.py`
- `models/metron.py`, `models/series_json.py`, `models/usenet.py`, `models/komga.py`
- `routes/opds.py`, `routes/api_v1.py`
- provider, download-client, route, unit, mocked, and integration test inventories

## Initial conclusion

CLU is a credible replacement candidate for the *operational surface* currently split
between Mylar, custom Cirrus scripts, and parts of Kavita/Komga support. It is not yet
safe to call it a Mylar replacement because the critical comparison is behavioral:
series monitoring, wanted-issue semantics, edition/annual handling, acquisition retries,
post-download import, duplicate policy, and recovery after interruption still require
an isolated pilot.

The strongest likely fit is a coexistence architecture in which CLU owns acquisition,
metadata review, and staging while Komga or Kavita remains the reader during migration.
CLU's own reader and OPDS service can then be tested without making reader migration a
prerequisite for replacing Mylar.

## Capability map

| Area | CLU evidence | Cirrus implication | Decision status |
|---|---|---|---|
| Library index | SQLite file index, metadata scanner, filesystem watcher | Can replace several indexing scripts; must define DB backup/rebuild policy | promising |
| Metadata | Metron, GCD, ComicVine, local DBs, ComicInfo writer, history/revert | Strong overlap with existing Cirrus work; reconcile schema and authority rules | pilot |
| Series metadata | Mylar-compatible `series.json`, Metron IDs, ComicVine backfill | Useful bridge, but compare against DieselTech v2 before adopting | verify |
| Wanted/pull list | Metron releases, monitored series, wanted reconciliation | Potential Mylar replacement core; test issue/edition edge cases | pilot |
| Acquisition | GetComics, Newznab + SABnzbd/NZBGet, AirDC++, MEGA/Pixeldrain | Broad coverage; isolate each provider and preserve provenance | pilot |
| Post-download | Folder monitor, unpack/convert/rename/move, metadata scan | Overlaps Stage-01; do not run two competing watchers on one tree | design gate |
| Reader | Built-in browser reader, progress/history, favorites, lists | May reduce need for separate UI, but Panels compatibility must be tested | verify |
| OPDS | `/opds`, browse, to-read; multi-user auth/scoping | Likely Panels integration path; test actual client behavior | verify |
| Komga | Reading-history/progress synchronization client | Supports phased coexistence and reader continuity | promising |
| Kavita | No equivalent first-class sync evidence found in inspected files | Keep Kavita as independent consumer; do not assume CLU sync parity | open |
| Administration | backups, restore, logs, health endpoint, roles, path permissions | Better operational surface than ad-hoc scripts; validate backup restore | verify |

## Risks requiring proof

1. The Docker example contains both a bind mount and a named volume for `/config`; the
   final deployment must use exactly one deliberate persistent mapping.
2. `MONITOR=yes` enables automatic filesystem behavior. It must not watch the live
   JDownloader root until claim, provenance, collision, and rollback semantics are proven.
3. CLU's Metron implementation has process-level throttling and SQLite response caching,
   but its own comments identify concurrency and cache-expiry subtleties. We must verify
   actual installed dependencies and response-header behavior without high-volume calls.
4. CLU writes a Mylar-compatible format today, but compatibility is not proof that it
   can consume every existing Mylar series or preserve all hand-edited fields.
5. Database state and archive metadata can diverge. Files remain authoritative for the
   comic payload; CLU's database must be rebuildable and never become the sole copy of
   identity or reading history without backup/export validation.

## Recommended pilot boundary

Use a disposable CLU database/configuration and a copied or explicitly selected small
CBZ corpus. Start with read-only indexing and metadata inspection, then enable one
mutation at a time: metadata proposal, XML write, rename, move, download client, and
reader/OPDS access. Keep Mylar, Kavita, and the production intake paths untouched until
the pilot acceptance report is complete.
