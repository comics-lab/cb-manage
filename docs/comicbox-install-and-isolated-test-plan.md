# Comicbox installation and isolated-library test plan

Date: 2026-11-05
Status: Proposed — Comicbox CLI baseline installed; Codex/test-library deployment still awaiting approval

## Executive finding

Comicbox is both a standalone Python library/CLI and the metadata engine used by
Codex. It is not itself Codex’s web server or database. Installing Codex normally
provides Comicbox inside the Codex runtime; installing Comicbox separately is
useful for controlled command-line metadata and archive tests.

Sources checked:

- https://github.com/ajslater/comicbox
- https://github.com/ajslater/codex

Comicbox reads, merges, writes, and converts comic metadata formats including
ComicInfo.xml and MetronInfo.xml. It can perform online tagging against Metron and
ComicVine, but those operations must remain disabled or tightly rate-limited during
the first test phase.

## Installed baseline

- Virtual environment: `/mnt/phoenix/services/comicbox/.venv`
- CLI: `/mnt/phoenix/services/comicbox/.venv/bin/comicbox`
- Installed version: `5.6.1`
- Python: `3.13.5`
- Doctor result: 0 problems
- Passing checks: CBZ, CBR via `unrar`, CB7, image codecs, configuration, cache parent, and Python requirements
- PDF support: not installed; requires `python -m pip install 'comicbox[pdf]'`
- Online services: intentionally unconfigured; no Metron or ComicVine credentials added

Activation:

```bash
cd /mnt/phoenix/services/comicbox
. .venv/bin/activate
comicbox doctor
```

## Installation requirements

### Standalone Comicbox

- Python environment suitable for the current pinned Comicbox release.
- `pip install comicbox` for CBZ/CBR/CBT/CB7 support.
- `pip install 'comicbox[pdf]'` only if PDF input is intentionally tested; this
  adds PyMuPDF and increases the dependency surface.
- `unrar` is required for CBR handling on Linux.
- No database or permanent library is required by Comicbox itself.

Comicbox configuration precedence is command line, environment, then config file.
The documented default config file is:

```text
~/.config/comicbox/config.yaml
```

Environment variables use the `COMICBOX_` prefix and nested `__` names, for example
`COMICBOX_GENERAL__RECURSE=true`. Credentials must not be written into the repo,
compose file, or shell history.

### Codex

The official Docker image is:

```text
ghcr.io/ajslater/codex
```

Codex is a separate web application that embeds/uses Comicbox. Its documented
container configuration should provide a persistent host directory mounted at
`/config`. Codex’s default internal service port is `9810`.

Codex state/configuration requirements:

- `CODEX_CONFIG_DIR`: defaults to `config/` under the working directory; in Docker,
  use the persistent `/config` mount.
- `codex.toml`: created in the config directory if absent.
- `codex.sqlite3`: main database, rebuildable for comic metadata but not user data.
- `user_data.sqlite`: user accounts, bookmarks, favorites, library definitions, and
  settings; must be backed up.
- `logs/`: application logs when file logging is enabled.
- `cache/`: Django cache and cover thumbnails by default; may be moved with
  `CODEX_CACHE_DIR`.

Codex does not require or justify a second copy of the comic library. Libraries are
configured in the application and should point to an existing mounted path.

## Proposed Cirrus layout

Application state only:

```text
/mnt/phoenix/services/comicbox-test/   # standalone config/cache if needed
/mnt/phoenix/services/codex-test/      # Codex /config, database, logs, cache
```

Shared content, never created or reorganized by these services:

```text
/mnt/phoenix/media/comics/              # existing Kavita/Mylar comic library
```

Isolated test content, explicitly separate from Mylar:

```text
/mnt/phoenix/staging/the_bins/           # 50–100 fresh test comics

/mnt/phoenix/media/codex/                # parallel Codex test library
```

JDownloader must feed the test only through a deliberate copy or bind mount into
`incoming/`; it must not be granted ownership of the authoritative comics library.
The first Codex mount should be read-only against `incoming/` or `library/`.

## Proposed first Docker test mounts

Illustrative only; do not run until approved:

```yaml
services:
  codex-test:
    image: ghcr.io/ajslater/codex:<pinned-version>
    container_name: codex-test
    ports:
      - "127.0.0.1:9810:9810"
    environment:
      TZ: America/Los_Angeles
      CODEX_CONFIG_DIR: /config
      CODEX_LOG_TO_FILE: "1"
    volumes:
      - /mnt/phoenix/services/codex-test:/config
      - /mnt/phoenix/staging/the_bins:/test-incoming:ro
      - /mnt/phoenix/media/codex:/test-library:ro
```

The final image tag, UID/GID, health check, command, and exact environment names
must be verified against the current Codex documentation before deployment. The
service must bind to loopback only during evaluation; no nginx route is proposed.

## Test sequence

1. Record host load, Docker state, current Mylar/Kavita mappings, and staging hashes.
2. Pin Comicbox and Codex versions.
3. Create only the application-state and isolated-test directories listed above.
4. Run Comicbox read-only inspection on a small sample of clean CBZ, malformed CBZ,
   CBR, PDF, and metadata-conflict archives.
5. Capture normalized metadata without writing archives.
6. Run `comicbox doctor` and record dependencies and failures.
7. Start Codex with the test content mounted read-only.
8. Verify initial scan, series/volume/issue grouping, search, covers, logs, and
   OPDS endpoints.
9. Test Panels only against the isolated Codex OPDS endpoint.
10. Compare Codex’s view with Kavita and Mylar without letting any application
    rename or move shared content.
11. If approved separately, copy a small sample into `library/`, mount it writable,
    and test metadata tagging/rename previews with rollback hashes.
12. Produce a pass/fail report and recommendation; do not promote test output
    automatically.

## Guardrails

- No mount of `/mnt/phoenix/media/comics` writable during the initial test.
- No Mylar download directory, database, or configuration is modified.
- No public proxy exposure during evaluation.
- No online tagging until credentials, throttling, cache behavior, and match review
  are documented.
- No automatic rename, move, overwrite, or deletion.
- Preserve original files and SHA-256 hashes for every write-test sample.
- Treat Codex’s database as rebuildable metadata state, but protect `user_data.sqlite`.

## Approval required

Please approve or revise:

- `/mnt/phoenix/staging/the_bins` as the source intake root;
- `/mnt/phoenix/media/codex` as the parallel Codex test library root;
- the proposed `/mnt/phoenix/services/comicbox-test` and `codex-test` state paths;
- Docker-only Codex deployment for the first test;
- loopback-only port `9810`;
- read-only first phase;
- whether JDownloader may copy selected fresh downloads into the isolated `incoming/`
  directory.
