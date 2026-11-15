# Script Library and Documentation Plan

## Purpose

Cirrus has accumulated a useful but heterogeneous shell/Python toolkit. Before adding
CLU, every tool must be cataloged so the team knows what is authoritative, what is a
wrapper, what mutates files or databases, and what can be safely rerun.

## Inventory baseline

- Cirrus repository: 57 `.py`/`.sh` files, including imports and integrations.
- CLU repository: 298 `.py`/`.sh` files, including application modules and tests.
- Raw inventories: `/tmp/CE-cirrus-tools.txt` and `/tmp/CE-clu-tools.txt`.

## Required record for each tool

- repository and relative path
- language and executable status
- one-sentence purpose
- authoritative or compatibility-wrapper status
- required binaries, Python packages, environment variables, credentials, and mounts
- inputs and outputs
- read-only, report-only, reversible mutation, or destructive mutation classification
- default paths and override flags
- dry-run support
- idempotency and collision behavior
- database/filesystem/network side effects
- safe example command
- expected report/log location
- failure and rollback procedure
- replacement or consolidation candidate

## Documentation standard

Each retained operator-facing tool gets either a section in a grouped runbook or its own
short page under this directory. Every example must use a harmless path or `--dry-run`
where available. Production paths must be labeled explicitly. Tools without safe behavior
must be marked review-only until wrapped or corrected.

## Planned catalog groups

1. archive conversion and extraction
2. inspection and audit
3. metadata resolution and XML materialization
4. cleanup, normalization, rename, and rebuild
5. promotion and Mylar handoff
6. library/database reports and cache maintenance
7. service integrations (Calibre, Mylar, Kavita, Komga)
8. host diagnostics and pressure tests
9. legacy/imported utilities

This catalog is a prerequisite to selecting which Cirrus tools CLU supersedes and which
remain as independent recovery utilities.
