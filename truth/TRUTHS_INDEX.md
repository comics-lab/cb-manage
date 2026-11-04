# CB-MANAGE Truth Index

> Owner: Richard
> Source: CB-MANAGE truth registry
> Last Updated: 2026-11-03
> Scope: URL-backed, local, and imported sources relevant to the comic archive and its related software repositories
> Status: Active — registry initialized; candidate URLs recorded, source review pending

## Purpose

This index is the authoritative list of sources CB-MANAGE has reviewed and
approved for use as truth. It points to source manifests and curated local
records. It does not imply that an unreviewed URL, reachable site, or copied
document is authoritative.

## Truth Inventory

| ID | Path | Type | Owner | Last Verified | Review Cycle | Status | Scope |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CB-EXT-INDEX | `truth/EXTERNAL/manifest.md` | URL/source manifest | Richard | 2026-11-03 | On change | Active | Registry for external documentation and web sources |
| CB-SOURCES-ARCH | `truth/sources_of_truth_architecture.md` | Operating model | Richard | 2026-11-03 | On change | Active | Intake, authority, provenance, and review rules for sources |
| CB-EXT-TEMPLATE | `truth/EXTERNAL/source_record_template.md` | Template | Richard | 2026-11-03 | On change | Active | Template for documenting one external source |

The manifest currently contains eleven Candidate URLs migrated from a
user-provided intake stub. None has been checked or promoted to authoritative
status. Review each source's owner, scope, canonical URL, and authority before
relying on it as truth.

## Rules

1. Treat a source as authoritative only after it has an entry here with a
   defined scope and status.
2. Keep source details and verification notes in the linked manifest or source
   record; this index is the compact navigation layer.
3. Distinguish `Candidate`, `Active`, `Draft`, `Unreviewed`, `Deprecated`, and
   `Archived` status accurately.
4. Record the exact URL and the date checked. Do not imply a page was verified
   merely because it is listed.
5. Prefer primary documentation from the project, platform, publisher, or
   maintainer. Note when a secondary source is only supporting evidence.
6. A URL-backed source may change. Recheck it at the stated review cycle and
   update both the manifest and this index when its status or scope changes.
7. Imported or generated local copies need provenance, owner, refresh method,
   and limitations before agents rely on them.
8. Truth sources do not override repository policy, access controls, or user
   approval requirements.

## Adding a Source

1. Create a record using [`EXTERNAL/source_record_template.md`](EXTERNAL/source_record_template.md).
2. Add the source to [`EXTERNAL/manifest.md`](EXTERNAL/manifest.md) as `Candidate`
   until its authority and scope have been reviewed.
3. Promote it to `Active` only after confirming the source owner, exact scope,
   relevant pages, and review cadence.
4. Add the record path and scope to this index.
5. Record material source decisions in the repository construction or relevant
   topic log.

