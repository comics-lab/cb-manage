# Comic tools manifest

Source repository: `/home/rmleonard/Projects/cirrus`

The copied files are locally developed Cirrus comic workflow tools. They are not
copies of Codex, Comicbox, Mylar3, CLU-comics, Calibre, or other upstream
applications.

## Safety classes

| Class | Meaning |
|---|---|
| Audit | Read-only inventory or validation. |
| Plan | Produces a report or proposal; no archive change when dry-run is used. |
| Metadata-write | Rewrites ComicInfo.xml, MetronInfo.xml, or related archive data. |
| Organize | Renames or moves files/directories. |
| Promote | Copies or moves material into an application import tree. |
| Remote | May contact ComicVine or another external service; use caching and throttling. |

## Primary tools

| Tool | Class | Purpose |
|---|---|---|
| `cbz_audit.py` | Audit | Inspect CBZ structure, metadata placement, and readiness. |
| `archive_inspector_dry_run.py` | Audit/Plan | Inventory archives without changing them. |
| `prepass_normalize.py` | Plan/Metadata-write/Organize | Use local sidecars and cache data to normalize metadata and paths. |
| `metadata_consistency_enrich.py` | Plan/Metadata-write | Audit and optionally write ComicInfo and MetronInfo into CBZ files. |
| `pass1_write_comicinfo.py` | Remote/Metadata-write | Write ComicInfo for high-confidence ComicVine matches. |
| `mylar_v3_buildout.py` | Organize/Metadata-write/Promote | Build Mylar-compatible names, sidecars, XML, and import branches. |
| `resolve_issue_from_local_metadata.py` | Plan | Resolve candidate ComicVine IDs from local GCD/CBL/Metron evidence. |
| `verify_comicvine_ambiguity.py` | Remote/Plan | Verify ambiguous ComicVine IDs at a throttled pace. |
| `refresh_cbl_cache_if_stale.py` | Plan | Refresh the local CBL-derived cache when stale. |
| `build_cbl_cache.py` | Plan | Build the CBL lookup cache. |
| `write_external_comicinfo.py` | Plan | Create an external ComicInfo proposal without altering the CBZ. |

The remaining utilities support conversion, cache reports, seed operations,
quarantine/rebuild work, weekly-pack inspection, filename normalization, and
Mylar import operations. Consult each tool's `--help` and the runbooks before
use.

## When an agent should suggest tools

- Unknown intake contents: suggest `archive_inspector_dry_run.py` or `cbz_audit.py`.
- Need local identity matching: suggest cache refresh, then
  `resolve_issue_from_local_metadata.py`.
- Need a proposed metadata/path change: suggest `prepass_normalize.py --dry-run`.
- Need XML consistency: suggest `metadata_consistency_enrich.py --dry-run`.
- Need ComicVine tagging: suggest `pass1_write_comicinfo.py --dry-run`, only after
  local evidence has been exhausted.
- Need Mylar staging: suggest `mylar_v3_buildout.py --dry-run`.
- Any ambiguity or conflicting IDs: stop at review and do not auto-correct source
  caches.
