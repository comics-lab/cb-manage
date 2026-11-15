# Metadata Consistency And Enrichment

`utilities/metadata_consistency_enrich.py` is the first consolidated validator for CBZ
metadata. It is deliberately report-first.

## What It Checks

- root `ComicInfo.xml` presence and XML validity
- root `MetronInfo.xml` presence and XML validity
- ComicVine identifier consistency
- series, number, year, and publisher fields
- local GCD enrichment opportunities
- post-write archive preservation through a temporary CBZ replacement

## Batch Audit And Repair

The batch wrapper defaults to applying XML repairs to CBZ archives under
`/mnt/phoenix/media/comics`:

```bash
scripts/metadata_consistency_batch.sh
```

It counts CBZ files first and writes a dated CSV report under `data/reports/`. Always use a
dry-run first when testing a new library or correction rule. Dry-run performs the same audit,
matching, and repair planning but does not write or replace any CBZ archive:

```bash
scripts/metadata_consistency_batch.sh --dry-run
```

Use `--limit N` for a bounded test run. The same `--root`, `--gcd-db`, `--report`, and
`--limit` options work in both modes. Use `--phase comicinfo` or `--phase metron` to run one
repair phase; `--phase all` is the default. The equivalent `--no-comicinfo` and
`--no-metroninfo` switches remain available. The ComicInfo phase uses the nearest
`series.json`, directory context, and unique local CBL-cache matches before considering a
record unresolved. It does not silently alter the CBL source or cache.

```bash
python3 utilities/metadata_consistency_enrich.py \
  --root /mnt/phoenix/media/incoming/jdownloader \
  --gcd-db /home/rmleonard/Projects/mylar-library/utilities/2025-10-15.db \
  --report data/reports/metadata-consistency.csv \
  --dry-run
```

The current wrapper phases stop after XML repair and validation. Mylar promotion and service
rescans remain separate operations; `validate` and `promote` are not batch-wrapper phases yet.

## Direct Utility Usage

The underlying utility remains available when a custom invocation is needed. For an explicit
apply, it requires `--write-xml`; `--dry-run` takes precedence and suppresses writes:

```bash
python3 utilities/metadata_consistency_enrich.py \
  --root /mnt/phoenix/media/incoming/jdownloader \
  --gcd-db /home/rmleonard/Projects/mylar-library/utilities/2025-10-15.db \
  --report data/reports/metadata-consistency-apply.csv \
  --write-xml
```

This utility does not edit Mylar or Kavita databases. Those databases are application-owned.
After XML materialization, use the respective application/API scan and verify the result from
logs and application state. The `--mylar-rescan` and `--kavita-rescan` options intentionally
fail until service-specific API configuration is added.

## Current Limitation

ComicVine series-name verification against the live API is not yet part of this utility. It
should be added as a cached, sequential resolver stage rather than making every archive audit
an independent remote request.
