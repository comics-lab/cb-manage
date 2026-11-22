# SQLite Documentation

> ID: `CB-EXT-014`
> Owner: SQLite project maintainers
> Source: <https://www.sqlite.org/docs.html>
> Last Verified: 2026-11-17
> Scope: SQLite3 SQL behavior, data types, pragmas, CLI, and file-backed database operations
> Status: Active
> Source Type: official documentation

## Authority Statement

The SQLite project documentation is the primary external reference for the
SQLite engine and its command-line interface. Richard reviewed and approved
this source for CB-MANAGE's SQLite3 boundary. It is authoritative for the
documented upstream behavior within the scoped pages below, but not for local
comic schemas or write approvals.

## Relevant Pages or Sections

- <https://www.sqlite.org/docs.html> — official documentation index.
- <https://www.sqlite.org/lang.html> — SQL syntax and SQLite-specific SQL behavior.
- <https://www.sqlite.org/datatype3.html> — storage classes, type affinity, and STRICT tables.
- <https://www.sqlite.org/pragma.html> — PRAGMA statements and compatibility limits.
- <https://www.sqlite.org/cli.html> — `sqlite3` command-line shell and safe-operation guidance.

## What This Source Governs

- SQLite3 SQL syntax and supported language features.
- Dynamic typing, storage classes, type affinity, and STRICT-table behavior.
- PRAGMA semantics and their version-sensitive compatibility limits.
- SQLite CLI distinction from the underlying library and database-file operations.

## Limits and Caveats

- The documentation is version-sensitive; record the relevant SQLite version
  when a workflow depends on a feature or PRAGMA.
- It does not establish CB-MANAGE schema design, comic metadata meaning, or
  local archive paths.
- It does not authorize writes to any database or comic archive.

## Verification Record

| Date | Checked by | Pages checked | Result / change |
| --- | --- | --- | --- |
| 2026-11-17 | Codex | Documentation index, SQL syntax, datatypes, pragmas, CLI | Official pages reachable and relevant; Richard approved CB-EXT-014 for Active use. |

## Review

- Review cycle: on change
- Next review due: Unknown
- Related local truth records: `truth/sources_of_truth_architecture.md`, `truth/TRUTHS_INDEX.md`
