# Comics Expansion Investigation Log

## 2026-09-09 — Discovery started

- Scope: assess `/home/rmleonard/Projects/clu-comics` as a possible Mylar replacement and design a broader comics acquisition, metadata, library, and reading-service plan.
- Cirrus source material: `/home/rmleonard/Projects/cirrus`.
- Related project inventory: `/home/rmleonard/Projects/comicinfo-creator`, `/home/rmleonard/Projects/clu-comics`, and other Markdown-bearing projects under `/home/rmleonard/Projects`.
- External topics queued for primary-source verification: Metron API and dataset/version changes, ComicInfo and `series.json` conventions, COPS/Calibre OPDS, AirDC++ Web, and a compatible Usenet client.
- Safety boundary: discovery and documentation only. No production archives, application databases, remote APIs at scale, credentials, downloads, deployments, or service configuration were changed.
- Temporary execution area reserved: `/tmp/CE` (not yet populated).

## Initial observations

`clu-comics` contains application code, database models, metadata providers, acquisition clients, library/file operations, OPDS routes, a web UI, Docker packaging, and a substantial test suite. Its architecture and operational behavior must be evaluated from source rather than inferred from its README.

The investigation must separate three questions:

1. Can it replace Mylar's series/issue acquisition and post-processing behavior?
2. Can it become the authoritative metadata and library workflow for Cirrus?
3. Which adjacent services belong in the expansion (Calibre/OPDS, AirDC++, Usenet, Metron integration), and which should remain optional?

Web research is limited to documentation and compatibility verification. Rate limits and terms of service will be respected; no load testing is part of this plan.

## Blocked actions

- `ssh reality.local ...` stopped locally with exit `255`: `Bad owner or permissions on /etc/ssh/ssh_config.d/20-systemd-ssh-proxy.conf`. No remote command ran. Continue using local project material; revisit only after the host SSH configuration is corrected.
- `python3 -m compileall` in `/home/rmleonard/Projects/clu-comics` could not create `__pycache__` files because that checkout is read-only. No source files were changed. Test execution may also be affected if pytest attempts to write caches; static inspection remains available.

## 2026-09-12 — Service configurations staged, not started

- Created `/srv/compose/komga/docker-compose.yml` using pinned image `gotson/komga:1.23.4`, state `/mnt/phoenix/services/komga`, and read-only library `/mnt/phoenix/media/comics:/data:ro`.
- Created `/srv/compose/transmission/docker-compose.yml` using pinned image `lscr.io/linuxserver/transmission:4.0.6`; staged incomplete downloads on `/home/transmission/incomplete` (NVMe volume) and completed weekly payloads on Phoenix. Credentials remain external via `/srv/compose/transmission/.env` (only `.env.example` was created).
- Created `/srv/compose/calibre/docker-compose.yml` and `/srv/compose/calibre/build/`. The build uses Calibre `9.11.0` and the reviewed/corrected Dockerfile; adapted scripts were copied from `/home/rmleonard/Projects/calibre/cirrus-adapted/` without modifying the source project.
- Created required empty service/download directories. No images were pulled and no new containers were started.
- Validated all three Compose files with `docker compose config`; Transmission validation used `.env.example` placeholders.
- Review item: confirm Komga and Calibre image/version choices, Transmission credentials and bandwidth policy, and Calibre's intended `/mnt/phoenix/media/books` library before first startup.

## 2026-09-15 — 2000 AD stabilization dry run

- Scanned `/mnt/phoenix/media/comics/Rebellion/2000 AD (1977)/` read-only: 2,499 valid CBZ files.
- Found 1,971 files with ComicInfo `Volume=1`, 527 with `Volume=1977`, and 1 blank.
- Confirmed directory `series.json` identifies ComicVine volume `19752` and year `1977`.
- Confirmed local GCD has matching `2000 AD` 1977 series ID `11289`.
- No live Metron API request was made during this pass. Full metadata rewrite remains gated on live Metron identity verification and operator approval.
- Report: `docs/comics-expansion/2000ad-metadata-dry-run-2026-09-15.md`; raw CSV remains in `/tmp/CE/2000ad-metadata-dry-run.csv`.
- Format check: ComicInfo v2.0 is the current stable compatibility target; v2.1 is a draft. MetronInfo v1.1 is available and requires XSD 1.1 validation. The old minimal writer is not accepted as the proposal generator until mappings are validated.
- Began proposal phase with `Volume=1977`: generated 2,499 external ComicInfo and 2,499 external MetronInfo proposals under `/mnt/phoenix/media/comics/Rebellion/2000 AD (1977)-metadata-proposals-20260915-v2/`; no CBZ archives were modified.
- Proposals preserve existing ComicInfo fields and add the canonical series/publisher/volume. MetronInfo proposals include the local Comic Vine series ID and are explicitly marked pending issue-level Metron verification; they are not approved for insertion yet.
- The first proposal directory without `-v2` used an incomplete ID element and must be treated as superseded/invalid; the `-v2` directory is the review target.
- Materialization attempt: first 24 archives now contain the reviewed proposal XML with `Volume=1977`; rollback XML copies exist under `/mnt/phoenix/media/comics/Rebellion/2000 AD (1977)-metadata-rollback-20260915/`. The report was not finalized because NFS archive replacement stalled. A detached continuation was not preserved by the execution environment and exited; no process remains. Remaining files are untouched and the resumable script skips entries with rollback copies.
- Resumed materialization on 2026-09-15: progress reached 100 rollback entries/updated archives before the execution environment ended the long-running command. No process remains; the resumable script skips completed entries.
