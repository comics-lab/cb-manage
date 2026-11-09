# Comicbox: Online Metadata and Archive Writes

**Status:** Source review handoff; no library archives changed.
**Reviewed:** 2026-11-09
**Checkout:** `../comicbox`, branch `main`, commit `9cacf3c` (`v5.6.1`, 2026-11-06), clean and tracking `origin/main` at inspection time.

## Summary

Comicbox contains the implementation that Codex delegates to for online
Comic Vine and Metron lookup, conversion into its canonical metadata model,
format-specific serialization, and archive writes. The local checkout is the
matching latest version used by Codex's lockfile (`comicbox~=5.6.1`). This
inspection identifies code paths; it does not test live API credentials or
write to a real comic library.

The overall flow is:

```text
Online source (Metron / Comic Vine)
        -> source-specific API schema and fetch/search
        -> canonical Comicbox metadata dict
        -> merge with archive metadata / explicit patch
        -> MetronInfo and/or ComicInfo transform + schema validation
        -> archive replacement or conversion to CBZ
        -> Codex re-imports the resulting archive
```

## Source locations

| Concern | Code to inspect | Role |
|---|---|---|
| Metron API | `comicbox/formats/metron_api/online_source.py` | Metron source fetch/search, session and cache/rate-limit behavior; inspect `get()` and `search()` implementations. |
| Metron payload mapping | `comicbox/formats/metron_api/transform.py` | Converts Metron API issue/series data to Comicbox's canonical dictionary. It maps Metron, Comic Vine, and GCD cross-identifiers when present. |
| Metron API payload model | `comicbox/formats/metron_api/schema.py` | Validates and documents normalized API payload structure. |
| Comic Vine API | `comicbox/formats/comicvine_api/online_source.py` | Comic Vine fetch/search, API request behavior, candidate construction, and throttling. |
| Comic Vine payload mapping | `comicbox/formats/comicvine_api/transform.py` | Converts Comic Vine issue/volume results into canonical Comicbox metadata. |
| Shared source orchestration | `comicbox/online_session.py`, `comicbox/box/online_lookup.py`, `comicbox/formats/base/online/` | Configures sources, looks up candidates or explicit IDs, matches/merges candidates, and manages shared online-source behavior. |
| Canonical merge | `comicbox/box/merge.py` | Combines existing metadata, online source results, and caller patches according to merge policy. |
| MetronInfo output | `comicbox/formats/metron_info/transform/`, `comicbox/formats/metron_info/schema/` | Maps canonical metadata to MetronInfo XML and its schema. |
| ComicInfo output | `comicbox/formats/comic_info/transform/`, `comicbox/formats/comic_info/schema.py` | Maps canonical metadata to ComicInfo XML and its schema. |
| Public write API | `comicbox/write.py` | `write_metadata()` and `bulk_write()` APIs; accepts a canonical patch, merge mode, target formats, deletion paths, and dry-run option. |
| Archive I/O | `comicbox/box/archive/read.py`, `comicbox/box/archive/write.py` | Reads archive contents, removes/replaces metadata members, writes a temporary archive, and handles write destination or format conversion. |
| Format registry | `comicbox/formats/metron_info/__init__.py`, `comicbox/formats/comic_info/__init__.py`, `comicbox/formats/sources.py` | Registers format labels, embedded filenames, transforms, schemas, and supported metadata sources. |

## API/write semantics to account for

- The write patch is in Comicbox's canonical schema, not arbitrary XML. Use
  the format transforms to produce XML; do not construct both XML formats by
  hand unless there is a concrete reason.
- `formats` selects `METRON_INFO`, `COMIC_INFO`, or both. Inspect the selected
  formats and their field support before applying a proposed GCD mapping.
- `merge_mode` has `additive`, `replace`, and `update` behavior. Their list and
  nested-dictionary semantics differ. Choose deliberately and test on copies.
- Empty values do not necessarily clear an existing field. `delete_keys`
  accepts canonical glom paths for explicit deletion.
- `dry_run=True` returns serialized would-be output by format and does not
  write the archive. This should be the initial mode for any GCD enrichment
  integration.
- `WriteResult` reports errors and the final path. Some archive types cannot
  be updated in place and may be repacked to CBZ; configured behavior can
  preserve or delete the original. A caller must track `final_path`.
- Archive write replaces metadata files known to the format registry and
  repacks archive contents. It is not equivalent to a surgical byte-level
  edit of one existing XML member. Review archive conversion and original-file
  retention settings before using it on a library.

## Codex connection

Codex's local source code delegates to these APIs:

- `codex/librarian/onlinetag/` coordinates online searches and explicit-ID
  retrieval through Comicbox.
- `codex/choices/tagging.py` maps its format identifiers to Comicbox's
  `MetronInfoTransform` and `ComicInfoTransform`.
- `codex/librarian/scribe/tag_writer.py` invokes `comicbox.write.bulk_write`,
  handles final paths and failures, and queues metadata re-import.

For a standalone GCD workflow, either use Comicbox's supported public write
API directly or extend Codex's orchestration. The latter entails integrating
with Codex's task scheduling, path/rename bookkeeping, filesystem watcher,
re-import lifecycle, and user-facing approval flow. Avoid calling private
Codex internals from a separate utility.

## GCD mapping implications

The Metron API transformer already knows how to preserve a GCD issue identifier
when Metron supplies `gcd_id`. That is evidence of an identifier path, not
proof that Comicbox queries GCD directly or that a local GCD snapshot is
supported. The inspected source registry and online source modules include
Metron and Comic Vine; no GCD online source implementation was identified in
this review.

A local-GCD integration should therefore define its own adapter from the GCD
snapshot to Comicbox's canonical metadata dictionary. It should establish:

1. how the GCD issue/series record is matched and how ambiguity is reviewed;
2. how GCD identifiers are represented in canonical `identifiers`;
3. which GCD fields map to canonical fields and then to each target XML format;
4. conflict precedence among archive values, GCD values, and any Metron/Comic
   Vine values;
5. provenance/version/date for the local GCD dataset and rights/attribution
   requirements before use or redistribution.

CB-MANAGE's GCD and Metron URLs remain candidate sources in
`truth/EXTERNAL/manifest.md`; they have not yet been authority-reviewed.

## Suggested safe implementation order

1. Review the exact source and schema code above, plus the relevant tests under
   `tests/schemas/`, `tests/unit/test_write_api.py`, and online-source tests.
2. Build a local GCD-to-canonical-dictionary adapter with provenance and
   deterministic, reviewable match evidence.
3. Generate dry-run `write_metadata()` output for fixture archives in both
   formats, including a dual-format archive and conflicting existing fields.
4. Validate serialized XML with the registered schema and re-read it through
   Comicbox; compare intended changes against actual changes.
5. Exercise write failures, unsupported archives, duplicate metadata members,
   final-path conversion, and rollback using disposable copies.
6. Only then integrate with Codex's tag-write lifecycle or approve a narrowly
   scoped real-library batch.

## Scope and limitations

This is a source-level review of the local `v5.6.1` checkout. It did not
contact Comic Vine or Metron, fetch a GCD snapshot, validate current external
terms, run the test suite, or modify Codex or library archives. Upstream may
have advanced after this checkout was inspected; compare local Git status and
the pinned dependency before future implementation work.
