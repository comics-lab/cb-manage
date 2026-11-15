#!/usr/bin/env bash
set -euo pipefail

# Recursive audit and optional XML repair for the curated comics library.

ROOT="/mnt/phoenix/media/comics"
GCD_DB="/home/rmleonard/Projects/mylar-library/utilities/2025-10-15.db"
REPORT=""
LIMIT="0"
DRY_RUN=0
COMICINFO=1
METRONINFO=1
PHASE="all"

usage() {
  cat <<'USAGE'
Usage: metadata_consistency_batch.sh [--root PATH] [--gcd-db PATH] [--report PATH] [--limit N] [--dry-run]
       [--phase all|comicinfo|metron] [--no-comicinfo] [--no-metroninfo]

Recursively audits CBZ files under /mnt/phoenix/media/comics and repairs XML metadata.
Use --dry-run to exercise the same checks and planned repairs without modifying CBZ files.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root) [[ $# -ge 2 ]] || exit 2; ROOT="$2"; shift 2 ;;
    --gcd-db) [[ $# -ge 2 ]] || exit 2; GCD_DB="$2"; shift 2 ;;
    --report) [[ $# -ge 2 ]] || exit 2; REPORT="$2"; shift 2 ;;
    --limit) [[ $# -ge 2 ]] || exit 2; LIMIT="$2"; shift 2 ;;
    --phase) [[ $# -ge 2 ]] || exit 2; PHASE="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --no-comicinfo) COMICINFO=0; shift ;;
    --no-metroninfo) METRONINFO=0; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "$PHASE" in
  all) ;;
  comicinfo) METRONINFO=0 ;;
  metron) COMICINFO=0 ;;
  *) echo "phase must be all, comicinfo, or metron" >&2; exit 2 ;;
esac

[[ -d "$ROOT" ]] || { echo "root directory not found: $ROOT" >&2; exit 1; }
[[ "$LIMIT" =~ ^[0-9]+$ ]] || { echo "limit must be a non-negative integer" >&2; exit 2; }
if [[ -z "$REPORT" ]]; then
  REPORT="data/reports/metadata_consistency_comics_$(date +%Y-%m-%d_%H%M%S).csv"
fi

COUNT="$(find "$ROOT" -type f -iname '*.cbz' -printf '.' | wc -c)"
echo "root=$ROOT"
echo "cbz_count=$COUNT"
echo "gcd_db=$GCD_DB"
echo "report=$REPORT"
echo "phase=$PHASE"
if [[ "$DRY_RUN" == "1" ]]; then
  echo "mode=dry-run (no CBZ/XML writes)"
else
  echo "mode=apply (XML repairs will be written into CBZ archives)"
fi

cmd=(python3 utilities/metadata_consistency_enrich.py --root "$ROOT" --gcd-db "$GCD_DB" --report "$REPORT")
if [[ "$DRY_RUN" == "1" ]]; then
  cmd+=(--dry-run)
else
  cmd+=(--write-xml)
fi
if [[ "$COMICINFO" == "0" ]]; then cmd+=(--no-comicinfo); fi
if [[ "$METRONINFO" == "0" ]]; then cmd+=(--no-metroninfo); fi
if [[ "$LIMIT" != "0" ]]; then
  cmd+=(--limit "$LIMIT")
fi
"${cmd[@]}"
