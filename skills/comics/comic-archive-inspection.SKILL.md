# Comic Archive Inspection Skill

This skill applies only to the Archive Inspector role in Stage-01.

## Procedure

- Watch only the Archive Inspector `source/` queue or the raw JDownloader source when
  operating in bootstrap mode.
- Wait for a stable size and closed file before claiming work.
- Process a single payload or download directory at a time.
- Detect nested archives before ordinary conversion.
- Re-run inspection after every unpack or conversion operation.
- Accept CBR, CBZ, and PDF input; produce CBZ output for downstream roles.
- Verify archive readability, comic-page presence, and nonzero output size.
- Build a publisher/series directory only after identity evidence is sufficient.
- Resolve series metadata in this order: current media tree, local CBL cache, local GCD,
  Metron API, then ComicVine API.
- Cache and record every API response; keep remote requests sequential and rate-limited.
- Write Mylar-compatible nested-`metadata` `series.json`, `cvinfo`, and the structured
  result record without fabricating IDs.
- Move success to `comicinfo-resolver/`; move failure to this role's `error/`.

## Do Not

- Do not process files that are still downloading.
- Do not overwrite an existing archive or create arbitrary numbered copies.
- Do not silently discard original source payloads.
- Do not edit CBL data or the canonical ComicVine cache.
- Do not perform bulk remote ComicVine lookups.
- Do not send incomplete trees to the next role.

## Result Record

Every item must record `source`, `original_name`, `input_type`, `input_size`, `input_hash`,
`output_paths`, `output_hashes`, `conversion_tools`, `series`, `publisher`, `status`,
`failure_class`, `started_at`, and `completed_at`.
