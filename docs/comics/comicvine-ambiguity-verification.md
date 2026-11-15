# ComicVine Ambiguity Verification (v1.1)

Use this utility to review ambiguous ComicVine issue ids without changing the
local cache.

Script:

- `utilities/verify_comicvine_ambiguity.py`
- `scripts/verify_comicvine_ambiguity.sh`

What it does:

- reads ambiguous ComicVine issue ids from `data/cbl_lookup.sqlite3`
- queries ComicVine one id at a time
- compares the live issue metadata against the most common cache row
- reports conflicts in ComicVine series ID, series name, issue number, volume,
  and year
- reports a normalized series-name count to distinguish punctuation/case variants
  from likely substantive name conflicts
- writes a CSV report for manual review

Why it exists:

- the cache contains legitimate ambiguities caused by relaunches, renamed
  series, and reading-list overlaps
- the verifier helps confirm which rows deserve a human review pass before any
  cache correction is made

Version 1.1 changes:

- includes `comicvine_series_id` and `volume` in ambiguity detection
- adds `series_id_count`, `volume_count`, and `normalized_name_count` to the CSV
- treats Unicode punctuation and case-only label differences as normalized-name
  variants, without hiding the original values
- remains review-only; it does not modify CBL source files or the SQLite cache

Safe usage:

```bash
./scripts/verify_comicvine_ambiguity.sh
```

With an explicit report path and slower pacing:

```bash
./scripts/verify_comicvine_ambiguity.sh \
  /home/rmleonard/Projects/cirrus/data/cbl_lookup.sqlite3 \
  report \
  /home/rmleonard/Projects/cirrus/data/reports/comicvine_ambiguity_review.csv \
  0 \
  3.0
```

Recommended workflow:

1. run the verifier against a small limit first
2. inspect the report for mismatched series, issue numbers, or years
3. review the highest-severity ids from the appendix
4. only then consider cache corrections or source-file corrections

Interpretation:

- Multiple raw series names with one normalized name are usually presentation
  differences, but still retain the original labels for review.
- Multiple series IDs, volumes, years, or issue numbers are substantive identity
  conflicts and should not be auto-corrected from the cache alone.
- The local scan is broad; live ComicVine verification remains sequential and
  rate-limited. Use `--limit` before a full remote run.
