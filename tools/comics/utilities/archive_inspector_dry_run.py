#!/usr/bin/env python3
"""Parallel, read-only inventory for raw comic archive intake."""
from __future__ import annotations
import argparse, concurrent.futures, os, subprocess, zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

TYPES={'.cbr','.cbz','.pdf'}; IMAGES={'.jpg','.jpeg','.png','.webp','.gif'}; NESTED={'.cbr','.cbz','.rar','.zip','.7z'}

def inspect(path: Path, deep: bool) -> dict:
    try:
        st=path.stat(); st2=path.stat(); stable=int(st.st_size==st2.st_size and st.st_mtime_ns==st2.st_mtime_ns)
        kind=path.suffix.lower()[1:]; valid='unknown'; detail=''; nested=pages=0
        if st.st_size==0: valid,detail='invalid','zero_length'
        elif path.suffix.lower()=='.cbz':
            with zipfile.ZipFile(path) as zf:
                names=zf.namelist(); nested=sum(Path(n).suffix.lower() in NESTED for n in names); pages=sum(Path(n).suffix.lower() in IMAGES for n in names)
                if deep: detail=zf.testzip() or ''
                valid='invalid' if detail else ('review' if not pages else 'valid')
                if not pages: detail='no_comic_pages'
        elif path.suffix.lower()=='.pdf':
            with path.open('rb') as fh: valid,detail=('valid','pdf_header') if fh.read(5)==b'%PDF-' else ('invalid','missing_pdf_header')
            pages='unknown'
        else:
            q=subprocess.run(['file','-b',str(path)],capture_output=True,text=True,timeout=30); detail=q.stdout.strip()[:160]; valid='valid' if 'rar' in detail.lower() else 'unknown'
        side=0
        for parent in (path.parent,*path.parents):
            if any((parent/n).is_file() for n in ('series.json','cvinfo')): side=1; break
        return {'path':str(path),'type':kind,'size':st.st_size,'stable':stable,'valid':valid,'nested':nested,'pages':pages,'sidecars':side,'detail':detail}
    except Exception as exc:
        return {'path':str(path),'type':path.suffix.lower()[1:],'size':0,'stable':0,'valid':'invalid','nested':0,'pages':0,'sidecars':0,'detail':f'{type(exc).__name__}: {exc}'}

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--root',default='/mnt/phoenix/media/incoming/jdownloader'); ap.add_argument('--report',default=''); ap.add_argument('--workers',type=int,default=max(1,os.cpu_count() or 1)); ap.add_argument('--deep',action='store_true',help='Fully test CBZ members; much slower'); a=ap.parse_args()
    root=Path(a.root).resolve(); paths=[p for p in sorted(root.rglob('*')) if p.is_file() and p.suffix.lower() in TYPES and not any(x.name=='_Stage-01' for x in p.parents)]
    report=Path(a.report) if a.report else Path('data/reports')/f"archive_inspector_dry_run_{datetime.now():%Y-%m-%d_%H%M%S}.md"; report.parent.mkdir(parents=True,exist_ok=True); start=datetime.now(); rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1,a.workers)) as pool:
        for i,row in enumerate(pool.map(lambda p:inspect(p,a.deep),paths),1):
            rows.append(row)
            if i%100==0 or i==len(paths):
                c=Counter(x['valid'] for x in rows); print(f"checked={i}/{len(paths)} current={row['path']} valid={c['valid']} invalid={c['invalid']} review={c['review']} unknown={c['unknown']} nested={sum(x['nested']>0 for x in rows)}",flush=True)
    end=datetime.now(); c=Counter(x['valid'] for x in rows)
    with report.open('w',encoding='utf-8') as f:
        f.write(f"# Archive Inspector Dry-Run Report\n\n- Root: `{root}`\n- Started: `{start.isoformat()}`\n- Completed: `{end.isoformat()}`\n- Workers: `{a.workers}`\n- Deep CBZ validation: `{a.deep}`\n- Stage-01 excluded: `yes`\n\n## Summary\n\n")
        for k,v in [('Files examined',len(rows)),('Stable',sum(x['stable'] for x in rows)),('Valid',c['valid']),('Invalid',c['invalid']),('Review',c['review']),('Unknown',c['unknown']),('Nested candidates',sum(x['nested']>0 for x in rows)),('Sidecar-bearing',sum(x['sidecars'] for x in rows))]: f.write(f'- {k}: **{v}**\n')
        f.write('\n## Inventory\n\n| Type | Stable | Validity | Size | Nested | Pages | Sidecars | Path | Detail |\n|---|---|---|---:|---:|---:|---:|---|---|\n')
        for x in rows: f.write(f"| {x['type']} | {x['stable']} | {x['valid']} | {x['size']} | {x['nested']} | {x['pages']} | {x['sidecars']} | `{x['path']}` | {x['detail'].replace('|','/')} |\n")
    print(f'completed report={report} files={len(rows)}'); return 0
if __name__=='__main__': raise SystemExit(main())
