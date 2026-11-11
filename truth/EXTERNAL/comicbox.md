# Comicbox

> ID: `CB-EXT-006`
> Owner: ajslater / Comicbox maintainers
> Source: https://github.com/ajslater/comicbox
> Last Verified: 2026-11-05
> Scope: Comic archive metadata reading, synthesis, online tagging, and conversion
> Status: Candidate
> Source Type: official project source

## Authority Statement

The repository is the primary source for Comicbox formats, transformations, CLI,
and supported online metadata behavior.

## Relevant Pages or Sections

- https://github.com/ajslater/comicbox — README, CLI, metadata, and release information

## What This Source Governs

- Reading and writing ComicInfo.xml, MetronInfo.xml, ComicBookInfo, CoMet, PDF metadata, YAML, and JSON.
- Online tagging against Metron and ComicVine, archive conversion, extraction, and renaming.

## Limits and Caveats

- Online tagging is version- and credential-dependent; rate limits and match confidence must be controlled.
- It does not replace local source precedence or review gates.

## Verification Record

| Date | Checked by | Pages checked | Result / change |
| --- | --- | --- | --- |
| 2026-11-05 | Codex | Repository README and CLI sections | Capabilities confirmed; strong candidate for CB-MANAGE integration. |

## Review

- Review cycle: on release; quarterly
- Next review due: 2027-02-05
- Related local truth records: `docs/comics-expansion/`, `docs/comic-metadata-intake-contract.md`
