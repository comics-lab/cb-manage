# ComicInfo Materializer Agent Contract

## Mission

Create a reviewable external `ComicInfo.xml` proposal beside each CBZ, then upsert it
into the archive only after the proposal passes identity and provenance gates.

## External Filename

```text
CV-[series]-#000-(year)-CVID.xml
```

`series` is sanitized for the filesystem, `000` is the normalized issue number, `year`
is the initial publication year, and `CVID` is the ComicVine issue ID. Missing or
ambiguous values must not be guessed; the item goes to review instead.

## Required Sequence

1. Extract an existing embedded `ComicInfo.xml` from the archive when present and use it
   as the initial proposal.
2. If no XML exists, construct the initial document from the nearest `series.json`.
3. Resolve and cross-check missing fields using the local CBL cache, then GCD data, then
   Metron API, and ComicVine API last for the issue ID.
4. Build the complete ComicInfo XML document in memory.
5. After the ComicVine issue ID is known, write the external proposal beside the CBZ using
   an exclusive create operation.
6. Record source fields, confidence, original archive hash, and proposal timestamp.
7. Validate XML syntax and required identity fields.
6. Await approval or an explicit apply command.
7. Upsert `ComicInfo.xml` into a temporary CBZ, validate the replacement, then atomically
   replace the original.
8. Record pre-write and post-write hashes in the provenance manifest.

## Safety Rules

- External XML creation is safe in dry-run only when no file is written.
- Never overwrite an existing external proposal; create a collision report instead.
- Never use a series ID as an issue ID.
- A CVID is required for the `CV-` filename; non-ComicVine editions use a separate
  materialization profile.
- Do not edit CBL sources or canonical cache rows.
- Preserve the original XML and archive provenance.

## Acceptance

The external proposal must parse as XML and contain, when applicable, `Series`, `Number`,
`Year`, `Publisher`, `ComicVineSeriesId`, and `ComicVineIssueId`. The proposal is not
considered applied until the CBZ is reopened and the embedded XML is validated.
