#!/usr/bin/env python3
"""Refresh the local CBL cache only when it is older than the freshness window."""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CBL_ROOT = Path("/home/rmleonard/Projects/CBL-ReadingLists")
DEFAULT_DB = REPO_ROOT / "data/cbl_lookup.sqlite3"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(DEFAULT_CBL_ROOT), help="CBL Git checkout")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="SQLite cache path")
    ap.add_argument("--max-age-days", type=float, default=7.0)
    ap.add_argument("--no-pull", action="store_true", help="Do not pull; rebuild from the current checkout")
    args = ap.parse_args()
    root, db = Path(args.root).resolve(), Path(args.db).resolve()
    if not root.is_dir():
        raise SystemExit(f"CBL root not found: {root}")
    age_days = float("inf") if not db.exists() else (time.time() - db.stat().st_mtime) / 86400
    print(f"cache={db} age_days={age_days:.2f} max_age_days={args.max_age_days:g}")
    if age_days <= args.max_age_days:
        print("action=reuse (cache is fresh)")
        return 0
    if not args.no_pull:
        print(f"action=refresh (pulling {root})")
        subprocess.run(["git", "-C", str(root), "pull", "--ff-only"], check=True)
    else:
        print("action=refresh (using current checkout; pull disabled)")
    cmd = [sys.executable, str(REPO_ROOT / "utilities/build_cbl_cache.py"), "--root", str(root), "--db", str(db)]
    subprocess.run(cmd, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
