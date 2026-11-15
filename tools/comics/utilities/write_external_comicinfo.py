#!/usr/bin/env python3
"""Create an external ComicInfo.xml proposal beside a CBZ without altering the archive."""
from __future__ import annotations
import argparse, re, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

def text(root: ET.Element, name: str) -> str:
    return (root.findtext(name) or '').strip()

def safe(value: str) -> str:
    value = re.sub(r'[\\/:*?"<>|]+', '-', value)
    return re.sub(r'\s+', ' ', value).strip(' .') or 'Unknown'

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cbz', required=True)
    ap.add_argument('--output', help='External XML path; default is the CBZ directory')
    ap.add_argument('--dry-run', action='store_true', help='Show the proposal path without writing')
    a=ap.parse_args(); cbz=Path(a.cbz).resolve()
    with zipfile.ZipFile(cbz) as zf:
        name=next((n for n in zf.namelist() if n.lower()=='comicinfo.xml'),None)
        if not name: raise SystemExit('ComicInfo.xml not found in CBZ')
        root=ET.fromstring(zf.read(name))
    series=text(root,'Series'); number=text(root,'Number'); year=text(root,'Year')
    issue=text(root,'ComicVineIssueId')
    if not issue:
        notes=text(root,'Notes'); m=re.search(r'(?:CVDB|4000-)[:# -]*(\d+)',notes,re.I); issue=m.group(1) if m else ''
    if not series or not number or not year or not issue:
        raise SystemExit('ComicInfo requires Series, Number, Year, and ComicVine issue ID')
    try: issue_num=f'{int(float(number)):03d}'
    except ValueError: raise SystemExit(f'non-numeric issue number: {number}')
    target=Path(a.output).resolve() if a.output else cbz.parent/f'CV-{safe(series)}-#{issue_num}-({year})-{issue}.xml'
    print(f'proposal={target}')
    if a.dry_run: return 0
    if target.exists(): raise SystemExit(f'proposal already exists: {target}')
    target.write_bytes(ET.tostring(root,encoding='utf-8',xml_declaration=True))
    print('written=1'); return 0
if __name__=='__main__': raise SystemExit(main())
