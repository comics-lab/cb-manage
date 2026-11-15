# Cirrus-developed comic metadata scripts

This catalog separates the tools developed in the Cirrus work from external projects.

## Ownership and scope

The following are external projects or upstream data/services, not Cirrus-developed
scripts: Codex, CLU-comics, Mylar3, Calibre, CBL-ReadingLists, the GCD database,
ComicVine, Metron, ComicTagger, Kavita, Komga, Transmission, and similarly named
upstream applications or datasets.

The scripts below are the local operational tools developed for the Cirrus comic
intake and metadata workflow. They live in `/home/rmleonard/Projects/cirrus`.

## General metadata and archive workflow

### `utilities/metadata_consistency_enrich.py`

Audits CBZ archives and optionally writes both root `ComicInfo.xml` and
`MetronInfo.xml`. It reads existing embedded XML, nearby `series.json`, the local
CBL lookup cache, and the local GCD SQLite database. It writes a CSV report and
replaces the CBZ atomically when writing is enabled. It does not directly modify
Mylar or Kavita databases.

Read-only dry run:

```bash
cd /home/rmleonard/Projects/cirrus
python3 utilities/metadata_consistency_enrich.py \
  --root /mnt/phoenix/media/incoming/jdownloader \
  --gcd-db /home/rmleonard/Projects/mylar-library/utilities/2025-10-15.db \
  --report data/reports/metadata-consistency.csv \
  --dry-run
```

Write both XML files:

```bash
python3 utilities/metadata_consistency_enrich.py \
  --root /mnt/phoenix/media/incoming/jdownloader \
  --report data/reports/metadata-consistency-apply.csv \
  --write-xml
```

Useful switches: `--limit N`, `--no-comicinfo`, `--no-metroninfo`, and
`--dry-run`. The reserved `--mylar-rescan` and `--kavita-rescan` switches currently
fail because service API hooks are not configured.

Wrapper: `scripts/metadata_consistency_batch.sh`. It defaults to the Phoenix comic
tree and normally enables XML writing; pass `--dry-run` for inspection. It also
supports `--phase all|comicinfo|metron`, `--root`, `--gcd-db`, `--report`, and
`--limit`.

### `utilities/prepass_normalize.py`

Performs an earlier local-only prepass. It reads embedded ComicInfo, nearby
`series.json`, and the CBL cache; it identifies strong or ambiguous matches,
creates/refreshes both XML files for normalizable records, and moves normalized
archives into a publisher/series/volume tree. Weak or ambiguous records remain for
manual review. The default root is the JDownloader intake directory.

Dry run:

```bash
python3 utilities/prepass_normalize.py \
  --root /mnt/phoenix/media/incoming/jdownloader \
  --cache-db /home/rmleonard/Projects/cirrus/data/cbl_lookup.sqlite3 \
  --report data/reports/prepass-review.csv \
  --dry-run
```

Apply normalization:

```bash
python3 utilities/prepass_normalize.py \
  --root /mnt/phoenix/media/incoming/jdownloader \
  --cache-db /home/rmleonard/Projects/cirrus/data/cbl_lookup.sqlite3
```

### `utilities/pass1_write_comicinfo.py`

Resolves high-confidence ComicVine issue matches and writes `ComicInfo.xml`
through ComicTagger. It is intentionally conservative: resolved matches may be
written, while candidates and unresolved files are reported for review. It does
not generate MetronInfo.

```bash
python3 utilities/pass1_write_comicinfo.py \
  --root /mnt/phoenix/media/incoming/jdownloader \
  --limit 20 \
  --report data/reports/pass1.csv \
  --dry-run
```

Remove `--dry-run` to write. Other options include `--config CONFIG`, `--limit N`,
and `--report PATH`. The companion wrapper is `scripts/pass1_batch.sh`.

### `utilities/mylar_v3_buildout.py`

Normalizes staged v3 Mylar branches. It reads ComicInfo, MetronInfo, and sidecars,
generates both XML files, writes `series.json` and `cvinfo`, renames archives using
the configured Mylar naming rules, and can copy or move a normalized branch into
the import tree.

Dry run:

```bash
python3 utilities/mylar_v3_buildout.py \
  --source-root /mnt/phoenix/media/incoming/mylar-DUMMY-ROOT \
  --import-root /mnt/phoenix/media/incoming/mylar-imports \
  --dry-run
```

Apply and copy into the import tree:

```bash
python3 utilities/mylar_v3_buildout.py \
  --source-root /mnt/phoenix/media/incoming/mylar-DUMMY-ROOT \
  --import-root /mnt/phoenix/media/incoming/mylar-imports \
  --promote
```

Important switches: `--report PATH`, `--mylar-config PATH`, `--promote`, `--move`,
`--dry-run`, and `--all`. By default it only processes paths tagged as v3.

## Specialized metadata seeders

### `utilities/isbn_library_metadata.py`

Writes ISBN/library-oriented ComicInfo and MetronInfo data into CBZ files from a
JSON manifest. It is intended for curated books rather than unattended discovery.

```bash
python3 utilities/isbn_library_metadata.py \
  --manifest /path/to/manifest.json \
  --dry-run
```

Remove `--dry-run` to apply the manifest.

### `utilities/dc_finest_metadata.py`

Special-purpose metadata generation for the DC Finest set. Its command-line
interface should be checked with the installed source before use:

```bash
python3 utilities/dc_finest_metadata.py --help
```

### `utilities/seed_legacy_series_metadata.py`

Seeds legacy series metadata using a mapping CSV and the local GCD database,
producing a required report. Use dry-run first:

```bash
python3 utilities/seed_legacy_series_metadata.py \
  --mapping-csv /path/to/mapping.csv \
  --gcd-db /home/rmleonard/Projects/mylar-library/utilities/2025-10-15.db \
  --report data/reports/legacy-seed.csv \
  --dry-run
```

### `utilities/seed_series_from_cache.py`

Seeds loose CBZ files from the local series cache. It requires a root and report
path and supports an alternate cache database.

```bash
python3 utilities/seed_series_from_cache.py \
  --root /mnt/phoenix/media/incoming/jdownloader \
  --cache-db /home/rmleonard/Projects/cirrus/data/series_cache.sqlite3 \
  --report data/reports/series-seed.csv \
  --dry-run
```

## Audit or proposal-only tools

### `utilities/write_external_comicinfo.py`

Creates an external ComicInfo proposal beside a CBZ. It deliberately does not
alter the archive.

```bash
python3 utilities/write_external_comicinfo.py \
  --cbz /path/to/book.cbz \
  --output /path/to/proposal \
  --dry-run
```

Remove `--dry-run` to write the proposal.

### `utilities/cbz_audit.py`

Audits CBZ placement, XML presence, and Mylar-readiness. It is report-only and
does not modify archives.

```bash
python3 utilities/cbz_audit.py --help
python3 utilities/cbz_audit.py \
  --root /mnt/phoenix/media/incoming/jdownloader \
  --report /mnt/phoenix/staging/cbz_audit/reports/manual.csv
```

## Recommended order

For a new intake tree, use:

1. `cbz_audit.py` for an inventory.
2. `prepass_normalize.py --dry-run` to identify local matches and ambiguities.
3. `metadata_consistency_enrich.py --dry-run` to validate the proposed XML state.
4. Apply the selected normalization/enrichment step after reviewing reports.
5. Use `mylar_v3_buildout.py` only when a Mylar-compatible staging tree and naming
   convention are required.
6. Run a final audit before handing the tree to Mylar, Kavita, Codex, or another
   consumer.

These local scripts are workflow components; Codex, CLU-comics, Mylar3, Calibre,
and the other named applications remain external consumers or upstream systems.

## Appendix A — ComicInfo.xml schema record

The current practical ComicInfo target is the ComicRack-compatible **ComicInfo
v2.1 draft** schema. It is commonly called “ComicInfo v2”; the `v2.1` label is
important because current readers generally treat it as a backward-compatible
extension rather than a separate archive format.

The document root is `ComicInfo`. Fields are generally scalar child elements;
multi-valued fields are conventionally represented as comma-separated text.
Implementations vary in which fields they preserve.

| Group | Elements | Notes |
|---|---|---|
| Identity | `Series`, `Title`, `Number`, `Count`, `Volume`, `AlternateSeries`, `AlternateNumber`, `AlternateCount`, `StoryArc`, `StoryArcNumber`, `SeriesGroup` | Series and issue identity; `Volume` is frequently interpreted differently by Mylar, Kavita, and other readers. |
| Dates and publication | `Year`, `Month`, `Day`, `Publisher`, `Imprint`, `Format`, `BlackAndWhite`, `Manga` | `Year`/`Month`/`Day` are issue dates; `Format` describes the publication. |
| Credits | `Writer`, `Penciller`, `Inker`, `Colorist`, `Letterer`, `CoverArtist`, `Editor`, `Translator`, `Teams`, `Characters`, `Locations` | Usually comma-separated strings. |
| Description | `Summary`, `Notes`, `Genre`, `Tags`, `Web` | `Notes` is often used for compatibility identifiers such as `[CVDB:...]`; this is convention, not a strong schema type. |
| Ratings and flags | `AgeRating`, `CommunityRating`, `Review`, `GTIN`, `IsVersion`, `Manga`, `BlackAndWhite`, `StoryArc` | Reader support is uneven, especially for ratings and flags. |
| Archive/display | `PageCount`, `LanguageISO`, `ScanInformation`, `Characters`, `Teams`, `Locations` | `PageCount` may be recalculated by the consumer. |
| Identifiers | `ComicVineIssueId`, `ComicVineSeriesId`, `GTIN`, `Web` | ComicVine fields are widely used in the Mylar ecosystem but are not universal identifiers. |

Minimal representative record:

```xml
<?xml version="1.0" encoding="utf-8"?>
<ComicInfo>
  <Series>Example Series</Series>
  <Number>1</Number>
  <Volume>1977</Volume>
  <Year>1977</Year>
  <Publisher>Example Publisher</Publisher>
  <Title>Example Issue</Title>
  <Summary>Issue synopsis.</Summary>
  <Writer>Example Writer</Writer>
  <ComicVineSeriesId>12345</ComicVineSeriesId>
  <ComicVineIssueId>67890</ComicVineIssueId>
</ComicInfo>
```

This is a crosswalk record, not a claim that every consumer supports every field.
ComicInfo has no universally enforced XML namespace in normal CBZ use.

## Appendix B — MetronInfo.xml schema record

The current Metron schema is **MetronInfo v1.2**. Its namespace is
`https://metron-project.github.io/docs/metroninfo/schemas/v1.2`; the schema is
more structured than ComicInfo and supports typed collections and nested records.

| Group | Elements | Notes |
|---|---|---|
| Identifiers | `IDS` | Structured identifier collection for source systems and issue/series identity. |
| Publication identity | `Publisher`, `Series`, `MangaVolume`, `CollectionTitle`, `Number`, `AlternativeNumber` | `Series` is required by the v1.2 schema; manga and alternate numbering are explicit. |
| Content | `Stories`, `Summary`, `Genres`, `Tags` | `Stories` is a structured list; genres and tags are repeated elements. |
| Dates and physical data | `CoverDate`, `StoreDate`, `PageCount`, `Prices`, `GTIN` | Dates are typed dates; page count is a non-negative integer. |
| Classification | `AgeRating`, `CommunityRating` | Community rating can include average rating and rating count. |
| Relationships | `Arcs`, `Characters`, `Teams`, `Universes`, `Locations`, `Reprints` | These are structured lists and can carry identifiers or attributes. |
| Credits and links | `Credits`, `URLs` | Credits and URLs are structured repeated records. |
| Administrative | `Notes`, `LastModified` | `LastModified` is a typed date-time. |

Representative record:

```xml
<?xml version="1.0" encoding="utf-8"?>
<MetronInfo xmlns="https://metron-project.github.io/docs/metroninfo/schemas/v1.2"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Series id="12345">Example Series</Series>
  <Number>1</Number>
  <CoverDate>1977-01-01</CoverDate>
  <Publisher>Example Publisher</Publisher>
  <Summary>Issue synopsis.</Summary>
  <PageCount>32</PageCount>
  <Notes>Imported from local authority data.</Notes>
</MetronInfo>
```

MetronInfo v1.2 is the current target for new generated records. Existing Cirrus
scripts and older Comicbox documentation may still emit or describe v1.1, so XML
generation should be checked before bulk rewriting.

## Appendix C — Combined Comicbox/Codex normalized record

Comicbox and Codex do not define a third shared XML file called
`CombinedInfo.xml`. Comicbox normalizes filename data, ComicInfo, MetronInfo,
ComicBookInfo, CoMet, PDF metadata, and its own JSON/YAML into a superset internal
record. Codex uses Comicbox as its metadata engine and stores the resulting library
metadata in its application database while retaining the archive files as the
source media.

The effective crosswalk record is therefore a normalized object like this:

```yaml
identity:
  series: Example Series
  title: Example Issue
  number: "1"
  volume: "1977"
  alternate_number: ""
  collection_title: ""
publication:
  publisher: Example Publisher
  imprint: ""
  year: 1977
  cover_date: 1977-01-01
  store_date: ""
  format: Single Issue
identifiers:
  comicvine_series_id: "12345"
  comicvine_issue_id: "67890"
  metron_series_id: ""
  metron_issue_id: ""
  gcd_series_id: ""
  gcd_issue_id: ""
  gtin: ""
content:
  summary: Issue synopsis.
  stories: []
  genres: []
  tags: []
  arcs: []
  characters: []
  teams: []
  universes: []
  locations: []
credits: []
relationships:
  reprints: []
  alternative_names: []
technical:
  page_count: 32
  language: en
  age_rating: Unknown
  community_rating: null
provenance:
  source_files: [ComicInfo.xml, MetronInfo.xml]
  source_systems: [local-cache, gcd, comicvine, metron]
  last_modified: ""
```

The practical mapping is:

| Normalized field | ComicInfo | MetronInfo | Typical Codex/Comicbox use |
|---|---|---|---|
| Series/title/number | `Series`, `Title`, `Number` | `Series`, `Number`, `Stories` | Primary display and grouping identity. |
| Volume | `Volume` | `MangaVolume` or series/issue context | Must be policy-controlled; do not assume ComicInfo volume equals Metron volume. |
| IDs | `ComicVine*`, `GTIN`, `Web`/`Notes` | `IDS`, `GTIN`, `URLs` | Preserve source-specific IDs rather than collapsing them into one ID. |
| Dates | `Year`, `Month`, `Day` | `CoverDate`, `StoreDate` | Metron retains more date precision and semantics. |
| Credits | scalar comma-separated fields | repeated `Credits` records | Normalize to a list, then downgrade carefully to ComicInfo strings. |
| Tags/relationships | `Genre`, `Tags`, `StoryArc`, `Characters`, `Teams`, `Locations` | structured repeated lists | Metron retains richer structure. |
| Summary/notes | `Summary`, `Notes` | `Summary`, `Notes` | Keep provenance and identifiers in notes only as compatibility fallback. |

The normalized record is lossy when exported to ComicInfo. Therefore the safe
direction is to preserve MetronInfo and/or Comicbox JSON/YAML as the richer record,
then generate ComicInfo as a compatibility projection for Mylar, Kavita, Komga,
and other readers.

## Appendix D — Database storage clarification

No: the endpoint applications do not all use SQLite, and “latest SQLite” is not a
shared compatibility guarantee.

| Application/system | Storage model |
|---|---|
| Codex | Supports SQLite for simple deployments and PostgreSQL for production. |
| Comicbox | Primarily a metadata library/CLI; its native JSON/YAML records are not an application database requirement. |
| Mylar3 | Uses SQLite in the typical deployment. |
| Kavita | Uses SQLite in normal deployments. |
| Komga | Uses an embedded database in standard deployments; verify the deployed version and configuration rather than assuming every release/backend is identical. |
| Calibre | Uses its own library metadata database format, normally SQLite-backed, plus filesystem content and configuration. It is not interchangeable with Codex/Mylar/Kavita databases. |
| CBL-ReadingLists | Uses the repository's configured files/database; it is not a universal endpoint database standard. |

SQLite is therefore common in this ecosystem, but each application's schema,
migrations, locking behavior, and ownership rules are application-specific. Do not
point two applications at the same SQLite database. Share media archives and
metadata files deliberately, while keeping each application's database private.
