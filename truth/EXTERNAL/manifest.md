# CB-MANAGE External Source Manifest

> Owner: Richard
> Source: CB-MANAGE external URL inventory
> Last Updated: 2026-11-03
> Scope: Public websites and documentation considered for comic archive and related software work
> Status: Active — candidate URLs transcribed; authority review pending

## Purpose

Track external documentation and web sources that may inform CB-MANAGE work.
This manifest is an intake and provenance record; listing a candidate does not
make it authoritative. The approval state is maintained in
[`../TRUTHS_INDEX.md`](../TRUTHS_INDEX.md).

## Source Inventory

| ID | Title | URL | Local Record | Owner | Checked | Review Cycle | Status | Intended Scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CB-EXT-001 | Mylar3 | <https://github.com/mylar3/mylar3> | — | Unknown | Not verified | Before use; annual | Candidate | Comic library management software; project source |
| CB-EXT-002 | Mylar3 documentation | <https://mylarcomics.com/> | — | Unknown | Not verified | Before use; annual | Candidate | Mylar3 usage and configuration documentation |
| CB-EXT-003 | Mylar3 Saltbox installation guide | <https://docs.saltbox.dev/sandbox/apps/mylar3/> | — | Unknown | Not verified | Before use; annual | Candidate | Saltbox-specific Mylar3 installation and configuration |
| CB-EXT-004 | Kavita | <https://www.kavitareader.com/> | — | Unknown | Not verified | Before use; annual | Candidate | Kavita product and reader information |
| CB-EXT-005 | Kavita source repository | <https://github.com/Kareadita/Kavita> | — | Unknown | Not verified | Before use; annual | Candidate | Kavita software source and project documentation |
| CB-EXT-006 | Comicbox | <https://github.com/ajslater/comicbox> | — | Unknown | Not verified | Before use; annual | Candidate | Comicbox project source and documentation |
| CB-EXT-007 | Codex | <https://github.com/ajslater/codex> | — | Unknown | Not verified | Before use; annual | Candidate | Related comic cataloging/management project; relationship to Comicbox to verify |
| CB-EXT-008 | The Metron Project | <https://metron-project.github.io/> | — | Unknown | Not verified | Before use; annual | Candidate | Comic metadata project and documentation |
| CB-EXT-009 | Metron Open Collective | <https://opencollective.com/metron> | — | Unknown | Not verified | Before use; annual | Candidate | Funding and project-support information; not a technical authority by itself |
| CB-EXT-010 | Grand Comics Database | <https://www.comics.org/> | — | Unknown | Not verified | Before use; annual | Candidate | Comic bibliographic database and reference data |
| CB-EXT-011 | CBL-ReadingLists | <https://github.com/DieselTech/CBL-ReadingLists> | — | Unknown | Not verified | Before use; annual | Candidate | Comic Book Library reading-list files and project documentation |

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

