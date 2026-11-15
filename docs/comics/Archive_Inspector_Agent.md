# Archive Inspector Agent Contract

## Mission

Process one item at a time from the raw JDownloader intake and produce a complete,
closed, normalized series directory for the ComicInfo Resolver.

## Input

The only initial source is:

```text
/mnt/phoenix/media/incoming/jdownloader
```

Accepted payload types are `.cbr`, `.cbz`, and `.pdf`. Files still being downloaded,
locked, incomplete, zero-length, corrupt, or otherwise changing must not be processed.

## Required Processing

1. Atomically claim the file or containing download directory into
   `_Stage-01/archive-inspector/working/`.
2. Confirm the payload is closed and stable, then verify size and integrity.
3. Unpack a large archive containing other archives and reanalyze the extracted payloads.
4. Convert CBR archives to CBZ using the approved RAR-capable converter.
5. Convert PDF comic payloads to CBZ using the approved PDF conversion path.
6. Verify that every resulting CBZ is readable and contains comic pages.
7. Determine publisher and series identity using the source precedence below.
8. Create the publisher/series directory and create or update `series.json` and `cvinfo`
   sidecars when sufficient local identity exists.
9. Record source paths, original names, hashes, conversions, warnings, and timestamps.
10. Move the completed series directory to
   `_Stage-01/comicinfo-resolver/`.

## Failure Handling

Do not send a failed directory downstream. Create or use:

```text
_Stage-01/archive-inspector/error/
```

Move the complete failed work directory there and write an error record containing the
failure class, command/tool result, source path, hash if available, and retry guidance.

Use distinct failure classes such as `unstable_source`, `unsupported_type`,
`nested_archive_error`, `cbr_conversion_error`, `pdf_conversion_error`,
`corrupt_archive`, `no_comic_pages`, `identity_unresolved`, and `sidecar_write_error`.

## Series Metadata Precedence

Use the first consistent, sufficiently complete result. Preserve all contributing sources
in the result record; do not silently replace stronger evidence with weaker evidence.

1. Existing `media/comics` tree: sibling CBZ metadata, parent directory names, existing
   `series.json`, and `cvinfo`.
2. Local CBL reading-list cache: match publisher/series/year/issue where possible and
   require a unique result before accepting an identifier.
3. Local GCD dataset: use series and issue metadata to fill gaps and cross-check dates,
   publisher, and numbering.
4. Metron API: query only after local sources are exhausted; cache responses and obey its
   service limits.
5. ComicVine API: last resort, sequential and rate-limited; cache the response and record
   the query, result, and confidence.

The first two sources are preferred for creating a provisional series directory and
sidecars. A remote identifier must not be fabricated from a name-only match. If the
sources disagree, retain the work in `archive-inspector/error/` or a review disposition
with the conflict details.

## Mylar-Compatible Sidecars

The existing Mylar-compatible builder reads `series.json` fields under the nested
`metadata` object, including `publisher`, `name`, `year`, `volume`, `booktype`, and
`comicid`. It uses `comicid` as the ComicVine series identifier when generating `cvinfo`
and ComicVine URLs. Our Archive Inspector must preserve this shape, but must not label a
non-ComicVine identifier as `comicid` without recording its source and confidence.

The builder's current local fallback is not the complete precedence chain above. The
CBL/GCD/Metron/ComicVine resolution must therefore be a separate, reportable resolver
step rather than an assumption about Mylar's internal search behavior.

## Safety Rules

- Never overwrite an existing file; use a collision-safe name and record the collision.
- Preserve original payloads until conversion and validation succeed.
- Do not modify CBL source files or canonical cache rows.
- Do not query ComicVine concurrently or use it to guess a series at this stage.
- Do not move partial output to `comicinfo-resolver`.
- A directory is complete only when all accepted payloads have a disposition and the
  result record has been written.

## Acceptance Output

The output directory must contain validated CBZ payloads plus, where identity is known:

```text
series.json
cvinfo
archive-inspector-result.json
```

The next role is responsible for resolving and validating ComicInfo identity. The
Archive Inspector must not mark an archive `mylar_ready`.
