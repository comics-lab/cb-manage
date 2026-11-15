# Comic Tools Transfer Summary

Date: 2026-11-15

Source: `/home/rmleonard/Projects/cirrus`

Destination: `/home/rmleonard/Projects/cb-manage`

## Purpose

The comic-specific scripts, documentation, contracts, and skills developed in
Cirrus were copied into Pinky's repository. The transfer keeps comic-library
operations separate from Calibre, host administration, Docker, networking, and
other system tooling.

## Destination layout

```text
tools/comics/
  README.md
  MANIFEST.md
  utilities/
  scripts/

docs/comics/
  README.md
  agent contracts
  intake and metadata runbooks
  CBL and ComicVine reports
  comics-expansion material

skills/comics/
  README.md
  comic archive inspection skill
  comic metadata intake skill
  ComicInfo materialization skill
```

## Transferred contents

- 31 comic-related Python utilities
- 11 comic shell wrappers
- CBZ audit and archive-inspection tools
- CBL cache construction and reporting tools
- local metadata and ComicVine resolution tools
- ComicInfo and MetronInfo enrichment tools
- prepass normalization tools
- Mylar naming, staging, and promotion tools
- Comic metadata intake and materialization contracts
- comic archive, metadata-intake, and materialization skills
- intake, Mylar, CBL, ComicVine, and metadata runbooks
- comic expansion and application-evaluation documentation
- tool manifest and guidance for when agents should suggest each tool

## Safety organization

The manifest classifies tools as:

- audit
- plan/report
- metadata-write
- organize
- promote
- remote/API-enabled

The default operating sequence is:

1. inventory or audit;
2. run a dry run;
3. review the report and provenance;
4. apply the approved operation;
5. re-audit the result.

Agents must stop for review when identifiers, series names, editions, or source
records conflict. They must not silently correct authoritative CBL or cache data.

## Explicitly excluded

The transfer did not include:

- Calibre scripts or deployment files
- Docker, SSH, firewall, networking, or general host-management scripts
- generated reports
- caches or SQLite databases
- logs
- secrets or credentials
- Python bytecode
- external application source code for Codex, Comicbox, Mylar3, CLU-comics,
  Kavita, Komga, or Calibre

Those systems remain separate dependencies or tool families.

## Validation

All 31 transferred Python files were parsed with Python's AST parser. Result:

```text
python_files=31 syntax_errors=0
```

No runtime or destructive tests were performed against a comic library.

## Follow-up work

The copied scripts retain some Cirrus-era default paths. Before unattended use on
Pinky, parameterize or override paths for:

- intake roots
- cache databases
- GCD databases
- report directories
- Mylar import roots
- service configuration files

Use explicit command-line paths until that work is complete. The primary entry
points are:

- `tools/comics/README.md`
- `tools/comics/MANIFEST.md`
- `docs/comics/README.md`

