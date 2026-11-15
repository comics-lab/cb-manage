#!/usr/bin/env python3
"""Audit and optionally enrich CBZ ComicInfo.xml and MetronInfo.xml files.

Default mode is read-only. GCD enrichment and XML rewriting require --write-xml.
Application databases are never edited directly; service rescans are separate, explicit
operations and are intentionally not implemented until their API endpoints are configured.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sqlite3
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

CV_RE = re.compile(r"(?:4000-|CVDB[:\s#-]*|COMICID[:\s#-]*)(\d+)", re.I)
DEFAULT_GCD = Path("/home/rmleonard/Projects/mylar-library/utilities/2025-10-15.db")


def args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", required=True, help="Root directory to scan for CBZ files")
    p.add_argument("--gcd-db", default=str(DEFAULT_GCD), help="Local GCD SQLite database")
    p.add_argument("--report", default="", help="CSV report path")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--write-xml", action="store_true", help="Write enriched XML into CBZ archives")
    p.add_argument("--dry-run", action="store_true", help="Explicit read-only mode")
    p.add_argument("--no-comicinfo", action="store_true", help="Do not create or update ComicInfo.xml")
    p.add_argument("--no-metroninfo", action="store_true", help="Do not create or update MetronInfo.xml")
    p.add_argument("--mylar-rescan", action="store_true", help="Reserved: fail until a configured Mylar API is supplied")
    p.add_argument("--kavita-rescan", action="store_true", help="Reserved: fail until a configured Kavita API is supplied")
    return p.parse_args()


def field(root: ET.Element | None, name: str) -> str:
    if root is None:
        return ""
    node = root.find(name)
    return (node.text or "").strip() if node is not None and node.text else ""


def root_xml(zf: zipfile.ZipFile, filename: str) -> tuple[str, ET.Element | None]:
    target = next((n for n in zf.namelist() if n.lower() == filename.lower()), "")
    if not target:
        return "", None
    return target, ET.fromstring(zf.read(target))


def cv_ids(root: ET.Element | None) -> tuple[str, str]:
    if root is None:
        return "", ""
    values = " ".join((node.text or "") for node in root.iter())
    ids = CV_RE.findall(values)
    explicit = field(root, "ComicVineIssueId")
    if explicit.isdigit():
        ids.insert(0, explicit)
    issue = field(root, "Number")
    return (ids[0] if ids else "", issue)


def gcd_lookup(db: Path, series: str, year: str) -> dict[str, str]:
    if not db.exists() or not series:
        return {}
    try:
        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        row = con.execute(
            "SELECT name, year_began, publisher_id FROM gcd_series WHERE lower(name)=lower(?) AND (?='' OR year_began=?) LIMIT 1",
            (series, year, int(year) if year.isdigit() else 0),
        ).fetchone()
        con.close()
    except (sqlite3.Error, ValueError):
        return {}
    return {"Series": str(row["name"]), "Year": str(row["year_began"])} if row else {}


def sidecar_context(path: Path) -> dict[str, str]:
    """Read only simple scalar identity fields from the nearest series.json."""
    for parent in (path.parent, *path.parents):
        candidate = parent / "series.json"
        if not candidate.is_file():
            continue
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict):
            values = data.get("metadata", data)
            if not isinstance(values, dict):
                continue
            result = {str(k).lower(): str(v).strip() for k, v in values.items()
                      if isinstance(v, (str, int))}
            # ComicTagger/Mylar sidecars commonly call the ComicVine volume id comicid.
            if result.get("comicid", "").isdigit():
                result["comicvineseriesid"] = result["comicid"]
            return result
    return {}


def cache_lookup(db: Path, series: str, number: str, year: str) -> dict[str, str]:
    if not db.exists() or not series or not number:
        return {}
    try:
        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT series, number, year, comicvine_series_id, comicvine_issue_id "
            "FROM cbl_issue_lookup WHERE lower(series)=lower(?) AND number=?",
            (series, number),
        ).fetchall()
        con.close()
    except sqlite3.Error:
        return {}
    if year:
        same_year = [r for r in rows if str(r["year"]) == year]
        if same_year:
            rows = same_year
    pairs = {(str(r["comicvine_series_id"]), str(r["comicvine_issue_id"])) for r in rows
             if r["comicvine_series_id"] and r["comicvine_issue_id"]}
    if len(pairs) != 1:
        return {}
    series_id, issue_id = next(iter(pairs))
    r = rows[0]
    return {"Series": str(r["series"]), "ComicVineSeriesId": series_id,
            "ComicVineIssueId": issue_id}


def cache_lookup_issue(db: Path, issue_id: str) -> dict[str, str]:
    """Resolve the unique series for an existing ComicVine issue id."""
    if not db.exists() or not issue_id:
        return {}
    try:
        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT series, number, year, comicvine_series_id, comicvine_issue_id "
            "FROM cbl_issue_lookup WHERE comicvine_issue_id=?",
            (issue_id,),
        ).fetchall()
        con.close()
    except sqlite3.Error:
        return {}
    pairs = {(str(r["comicvine_series_id"]), str(r["comicvine_issue_id"])) for r in rows
             if r["comicvine_series_id"] and r["comicvine_issue_id"]}
    if len(pairs) != 1:
        return {}
    series_id, resolved_issue = next(iter(pairs))
    r = rows[0]
    return {"Series": str(r["series"]), "Number": str(r["number"]),
            "Year": str(r["year"]), "ComicVineSeriesId": series_id,
            "ComicVineIssueId": resolved_issue}


def set_field(root: ET.Element, name: str, value: str) -> bool:
    if not value:
        return False
    node = root.find(name)
    if node is None:
        node = ET.SubElement(root, name)
    if node.text == value:
        return False
    node.text = value
    return True


def rewrite(path: Path, comic: ET.Element, metron: ET.Element) -> None:
    fd, name = tempfile.mkstemp(suffix=".cbz", dir=path.parent)
    os.close(fd)
    Path(name).unlink(missing_ok=True)
    tmp = Path(name)
    try:
        with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename.lower() in {"comicinfo.xml", "metroninfo.xml"}:
                    continue
                zout.writestr(item, zin.read(item.filename))
            zout.writestr("ComicInfo.xml", ET.tostring(comic, encoding="utf-8", xml_declaration=True))
            zout.writestr("MetronInfo.xml", ET.tostring(metron, encoding="utf-8", xml_declaration=True))
        tmp.replace(path)
    finally:
        tmp.unlink(missing_ok=True)


def inspect(path: Path, gcd: Path, write: bool, repair_comicinfo: bool, repair_metroninfo: bool) -> dict[str, str]:
    row = {"cbz_path": str(path), "status": "ok", "reason": "", "comicvine_issue_id": "", "comicvine_series_id": "", "series": "", "number": "", "year": "", "publisher": "", "comicinfo_valid": "0", "metroninfo_valid": "0", "fields_added": "0", "xml_written": "0"}
    try:
        with zipfile.ZipFile(path) as zf:
            _, comic = root_xml(zf, "ComicInfo.xml")
            _, metron = root_xml(zf, "MetronInfo.xml")
            context = sidecar_context(path)
            if comic is None and repair_comicinfo:
                comic = ET.Element("ComicInfo")
                set_field(comic, "Series", context.get("series", path.parent.name))
                set_field(comic, "Publisher", context.get("publisher", path.parent.parent.name))
                set_field(comic, "Year", context.get("year", ""))
            if comic is None:
                row.update(status="review", reason="missing_or_invalid_root_comicinfo")
                return row
            row["comicinfo_valid"] = "1"
            if metron is not None:
                row["metroninfo_valid"] = "1"
            if repair_comicinfo and not field(comic, "ComicVineSeriesId"):
                set_field(comic, "ComicVineSeriesId", context.get("comicvineseriesid", ""))
            row.update(series=field(comic, "Series"), number=field(comic, "Number"), year=field(comic, "Year"), publisher=field(comic, "Publisher"))
            issue_id, _ = cv_ids(comic)
            mi_issue, mi_number = cv_ids(metron)
            row["comicvine_issue_id"] = issue_id or mi_issue
            row["comicvine_series_id"] = (field(comic, "ComicVineSeriesId") or
                                           field(metron, "ComicVineSeriesId") or
                                           context.get("comicvineseriesid", ""))
            # A disabled write phase must not hide evidence used by validation.
            if not row["comicvine_series_id"]:
                row["comicvine_series_id"] = context.get("comicvineseriesid", "")
            if bool(issue_id) != bool(row["comicvine_series_id"]):
                row.update(status="review", reason="ComicVine issue and series identifiers must appear together")
            if metron is None and repair_metroninfo:
                metron = ET.Element("MetronInfo")
            if metron is None:
                metron = ET.Element("MetronInfo")
            before = ET.tostring(comic) + ET.tostring(metron)
            cached = cache_lookup_issue(gcd, row["comicvine_issue_id"])
            if not cached:
                cached = cache_lookup(gcd, row["series"], row["number"], row["year"])
            for key, value in cached.items():
                if repair_comicinfo and not field(comic, key):
                    set_field(comic, key, value)
                if repair_metroninfo and not field(metron, key):
                    set_field(metron, key, value)
            gcd = gcd_lookup(gcd, row["series"], row["year"])
            for key, value in gcd.items():
                if repair_comicinfo and not field(comic, key):
                    set_field(comic, key, value)
                if repair_metroninfo and not field(metron, key):
                    set_field(metron, key, value)
            for key in ("Series", "Number", "Year", "Publisher"):
                value = field(comic, key)
                if value and repair_metroninfo:
                    set_field(metron, key, value)
            row["comicvine_issue_id"], _ = cv_ids(comic)
            row["comicvine_series_id"] = (field(comic, "ComicVineSeriesId") or
                                           field(metron, "ComicVineSeriesId") or
                                           context.get("comicvineseriesid", ""))
            if not row["comicvine_issue_id"] or not row["comicvine_series_id"]:
                row.update(status="review", reason="ComicVine issue and series identifiers must appear together")
            elif row["reason"] == "ComicVine issue and series identifiers must appear together":
                row.update(status="ok", reason="")
            changed = before != ET.tostring(comic) + ET.tostring(metron)
            row["fields_added"] = "1" if changed else "0"
            if write and changed and (repair_comicinfo or repair_metroninfo):
                rewrite(path, comic, metron)
                row["xml_written"] = "1"
    except zipfile.BadZipFile:
        row.update(status="invalid", reason="bad_zip")
    except ET.ParseError as exc:
        row.update(status="invalid", reason=f"xml_parse_error:{exc}")
    except Exception as exc:
        row.update(status="review", reason=f"error:{exc}")
    return row


def main() -> int:
    a = args()
    if a.mylar_rescan or a.kavita_rescan:
        raise SystemExit("Rescan hooks are not configured; use the report first and configure service APIs separately.")
    report = Path(a.report) if a.report else Path("/mnt/phoenix/staging/metadata_consistency/reports") / f"metadata_consistency_{datetime.now():%Y-%m-%d_%H%M%S}.csv"
    report.parent.mkdir(parents=True, exist_ok=True)
    paths = sorted(Path(a.root).resolve().rglob("*.cbz"))
    if a.limit:
        paths = paths[:a.limit]
    rows = [inspect(p, Path(a.gcd_db), a.write_xml and not a.dry_run,
                    not a.no_comicinfo, not a.no_metroninfo) for p in paths]
    with report.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ["cbz_path", "status", "reason"])
        writer.writeheader(); writer.writerows(rows)
    print(f"processed={len(rows)} report={report} write_xml={int(a.write_xml and not a.dry_run)}")
    print(f"ok={sum(r['status']=='ok' for r in rows)} review={sum(r['status']=='review' for r in rows)} invalid={sum(r['status']=='invalid' for r in rows)} xml_written={sum(r['xml_written']=='1' for r in rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
