# Codex

> ID: `CB-EXT-007`
> Owner: ajslater / Codex maintainers
> Source: https://github.com/ajslater/codex
> Last Verified: 2026-11-05
> Scope: Web comic archive browser, reader, library scanner, OPDS, and metadata editing
> Status: Candidate
> Source Type: official project source

## Authority Statement

The repository is the primary source for Codex application behavior and deployment.
It identifies Comicbox as the metadata engine and documents the official container.

## Relevant Pages or Sections

- https://github.com/ajslater/codex — README, Docker, administration, OPDS, and tagging
- https://github.com/ajslater/codex/releases — release notes

## What This Source Governs

- Supported archive formats, filesystem watching, browser editing, online tagging, renaming, and OPDS behavior.
- Container image and configuration expectations.

## Limits and Caveats

- Writable library mounts make metadata and rename operations state-changing; use staging and approvals.
- It is a reader/catalog application, not an acquisition manager.

## Verification Record

| Date | Checked by | Pages checked | Result / change |
| --- | --- | --- | --- |
| 2026-11-05 | Codex | Repository README and releases | Official source confirmed; integration candidate recorded. |

## Review

- Review cycle: on release; quarterly
- Next review due: 2027-02-05
- Related local truth records: `docs/comics-expansion/`
