# Comic tools

This directory contains the comic-specific tools transferred from
`Projects/cirrus`. It is intentionally separate from Calibre, Docker, host,
network, and general agent-management tooling.

## Layout

- `utilities/`: Python tools. Run them from this directory so local imports such
  as `utilities.cv_issue_resolver` resolve correctly.
- `scripts/`: shell wrappers for common multi-step operations.
- `MANIFEST.md`: ownership, source, safety, and dependency inventory.

## Operating rule

Use the sequence below unless a task-specific runbook says otherwise:

1. Audit or inventory.
2. Run a dry run and save its report.
3. Review ambiguity, provenance, and proposed paths.
4. Apply only the approved operation.
5. Re-audit the result.

Do not run archive-writing, moving, or promotion tools against a production
library without a saved report and rollback plan.

## Quick examples

```bash
cd /path/to/cb-manage/tools/comics
python3 utilities/cbz_audit.py --help
python3 utilities/prepass_normalize.py --root /path/to/intake --dry-run
python3 utilities/metadata_consistency_enrich.py \
  --root /path/to/intake \
  --report /path/to/report.csv \
  --dry-run
```

The scripts retain Cirrus-era defaults and may contain Cirrus-specific paths.
Use explicit arguments on Pinky or another host until those defaults are
parameterized.
