# Pinky Exclusive Media Management Pre-Action Plan

## Purpose

This plan defines the preparation required before Pinky becomes the exclusive
manager for comics and other supported media. Pinky should begin as an assisted,
report-driven operator and move toward exclusive management only after the
controls below are verified.

## 1. Parameterize the transferred tools

Replace or override Cirrus-specific defaults for:

- intake roots
- comic and media library roots
- GCD and CBL cache paths
- report and log paths
- Mylar, Codex, Kavita, Komga, and Calibre locations
- staging, quarantine, archive, and backup directories

Until this is complete, every command must use explicit Pinky paths.

## 2. Establish ownership and source-of-truth rules

Document which system owns:

- raw downloads
- canonical metadata
- filenames and directory structure
- Comicbox JSON/YAML records
- archive contents
- application indexes
- corrections and approval decisions

Endpoint applications should consume approved archives and metadata rather than
compete as independent authorities.

## 3. Implement the metadata staging ledger

Create the planned records for:

- raw source data
- source records
- candidate matches
- canonical records
- field provenance
- conflicts
- materialization plans
- materialization events

The ledger must preserve competing values and explain why a final value was
selected.

## 4. Configure credentials securely

Configure Pinky's secret store or protected environment for:

- ComicVine
- Metron
- GCD, where required
- Amazon or other metadata providers
- Codex, Mylar, Kavita, and Komga APIs
- download clients

Do not copy passwords, API keys, or `.env` files into Git.

## 5. Install and validate dependencies

Verify:

- Python and virtual-environment versions
- Comicbox and Comicbox Doctor
- ComicTagger, if still required
- `unrar`, `7z`, ZIP, and PDF support
- database drivers
- filesystem permissions
- network access
- API rate-limit and cache behavior

Record versions and test results in Pinky's documentation.

## 6. Build a disposable test library

Include representative cases:

- clean CBZ
- archive with missing metadata
- conflicting ComicInfo and MetronInfo
- trade paperback
- annual
- manga volume
- malformed archive
- duplicate or ambiguous ComicVine IDs
- EPUB and PDF, if those formats are in scope

Run the complete cycle:

```text
inventory → dry run → review → apply → audit → consumer scan
```

## 7. Define operational permissions

Pinky should have access only to explicitly configured:

- intake directories
- staging and quarantine
- approved library roots
- reports and logs
- required application APIs or sockets

It should not receive unrestricted access to unrelated host or personal data.

## 8. Establish backup and rollback

Before exclusive operation:

- back up application databases
- snapshot current library metadata
- preserve original downloads
- retain pre-change reports
- restore one archive successfully
- restore one application database successfully
- document reversal of metadata writes and promotions

## 9. Validate application integration

Test each integration independently and together:

- Comicbox materialization
- Codex scanning
- Mylar import/handoff
- Kavita scan
- Komga scan
- Panels/OPDS access
- Calibre import, if books remain in scope

Keep each application's database private. Share media and deliberate metadata
files only.

## 10. Complete Pinky runbooks and guardrails

Pinky documentation must explain:

- when to suggest each tool
- which tools are read-only
- which tools write archives
- which tools move or promote files
- when human review is mandatory
- how to handle ambiguous identity
- how to handle API or network failure
- how to report partial completion
- how to prevent duplicate imports
- which actions require an approved materialization plan

## 11. Migrate gradually

Use this progression:

```text
observe-only
  → dry-run reports
  → small approved batch
  → scheduled limited batch
  → full comic intake
  → additional media types
```

Do not begin with unattended exclusive management of the complete collection.

## Readiness gates

Pinky is ready for assisted comic intake when:

- transferred tools are discoverable and documented;
- paths and dependencies are configured;
- dry-run reports work on the disposable library;
- credentials are secured;
- backups exist;
- archive writes and rollback have been tested.

Pinky is ready for exclusive comic management only when:

- the metadata staging ledger is operating;
- the saved materialization-plan workflow is operating;
- all required consumer integrations have passed tests;
- permissions are restricted and verified;
- recovery has been demonstrated;
- Pinky's runbooks and guardrails are complete.

## Immediate priorities

1. Parameterize paths and configuration.
2. Secure credentials and permissions.
3. Create the disposable end-to-end test library.
4. Implement the saved metadata/materialization plan.
5. Verify backup and rollback.
6. Complete Pinky's tool-selection runbooks and guardrails.

Until these priorities are complete, Pinky should operate as an assisted,
report-driven comic-intake tool rather than the sole manager of all media.
