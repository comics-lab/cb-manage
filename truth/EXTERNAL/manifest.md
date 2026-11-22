# CB-MANAGE External Source Manifest

> Owner: Richard
> Source: CB-MANAGE external URL inventory
> Last Updated: 2026-11-03
> Scope: Public websites and documentation considered for comic archive and related software work
> Status: Active — reviewed sources identified below; remaining candidates retained

## Purpose

Track external documentation and web sources that may inform CB-MANAGE work.
This manifest is an intake and provenance record; listing a candidate does not
make it authoritative. The approval state is maintained in
[`../TRUTHS_INDEX.md`](../TRUTHS_INDEX.md).

## Source Inventory

| ID | Title | URL | Local Record | Owner | Checked | Review Cycle | Status | Intended Scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CB-EXT-001 | Mylar3 | <https://github.com/MylarComics/mylar3> | [record](mylar3.md) | Mylar3 maintainers | 2026-11-17 | Before use; annual | Active | Comic library management software; project source |
| CB-EXT-002 | Mylar3 documentation | <https://mylar.nerdfirehurricane.com/> | [record](mylar3-documentation.md) | Mylar3 maintainers | 2026-11-17 | Before use; annual | Active | Mylar3 usage and configuration documentation |
| CB-EXT-003 | Mylar3 Saltbox installation guide | <https://docs.saltbox.dev/sandbox/apps/mylar3/> | [record](mylar3-saltbox.md) | Saltbox maintainers | 2026-11-05 | Before use; annual | Active | Saltbox-specific Mylar3 installation and configuration |
| CB-EXT-004 | Kavita | <https://www.kavitareader.com/> | [record](kavita.md) | Kavita maintainers | 2026-11-05 | Before use; annual | Active | Kavita product and reader information |
| CB-EXT-005 | Kavita source repository | <https://github.com/Kareadita/Kavita> | [record](kavita-source.md) | Kareadita / Kavita maintainers | 2026-11-05 | Before use; annual | Active | Kavita software source and project documentation |
| CB-EXT-006 | Comicbox | <https://github.com/ajslater/comicbox> | [record](comicbox.md) | ajslater / Comicbox maintainers | 2026-11-05 | Before use; annual | Active | Comicbox project source and documentation |
| CB-EXT-007 | Codex | <https://github.com/ajslater/codex> | [record](codex.md) | ajslater / Codex maintainers | 2026-11-05 | Before use; annual | Active | Related comic cataloging/management project; relationship to Comicbox to verify |
| CB-EXT-008 | The Metron Project | <https://metron-project.github.io/> | [record](metron.md) | The Metron Project | 2026-11-05 | Before use; annual | Active | Comic metadata project and documentation |
| CB-EXT-009 | Metron Open Collective | <https://opencollective.com/metron> | [record](metron-open-collective.md) | The Metron Project / Open Collective | 2026-11-05 | Before use; annual | Active | Funding and project-support information; not a technical authority by itself |
| CB-EXT-010 | Grand Comics Database | <https://www.comics.org/> | [record](gcd.md) | Grand Comics Database community and maintainers | 2026-11-05 | Before use; annual | Active | Comic bibliographic database and reference data |
| CB-EXT-011 | CBL-ReadingLists | <https://github.com/DieselTech/CBL-ReadingLists> | [record](cbl-readinglists.md) | DieselTech | 2026-11-05 | Before use; annual | Active | Comic Book Library reading-list files and project documentation |
| CB-EXT-012 | CLU Comics | <https://clucomics.org/> | [record](clu-comics.md) | CLU Comics maintainers | 2026-11-05 | Before use; annual | Active | Comic library management, metadata, and archive workflow |
| CB-EXT-013 | Pullbox | <https://pullbox.app/docs/> | [record](pullbox.md) | Pullbox maintainers | 2026-11-05 | Before use; annual | Active | Comic collection management and related API/documentation |
| CB-EXT-014 | SQLite documentation | <https://www.sqlite.org/docs.html> | [record](sqlite.md) | SQLite project maintainers | 2026-11-17 | Before use; on change | Active | SQLite3 SQL behavior, data types, pragmas, CLI, and file-backed database operations |

## Intake Rules

- Prefer official documentation from the publisher, project maintainer, or
  platform owner.
- Capture the canonical URL and the specific pages or sections that matter.
- Record the source owner when known; use `Unknown` until verified.
- Record what the source governs and what it does not establish.
- Mark new entries `Candidate` until reviewed; do not silently treat bookmarks
  or search results as truth.
- The initial candidate list was transcribed from a user-provided intake stub,
  then migrated into this manifest; the stub was removed after migration.
  Titles and intended scopes are descriptive labels; owners, current
  availability, canonical status, and authority have not been verified.
- Review volatile platform and software documentation more often than stable
  reference material. Set the cadence per source.
- If a URL moves, redirects, or becomes unavailable, record the observation and
  update the status. Do not silently replace the source.
- Keep credentials, private URLs, personal data, and access tokens out of this
  public repository manifest.

## Record Template

Copy [`source_record_template.md`](source_record_template.md) for each source
that needs a durable scope and authority statement. The manifest row should
link to that record.

