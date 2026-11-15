# Stage-01 Agent Framework

This framework defines the first bounded test of the file-driven comic intake roles.
It is a coordination model, not permission to mutate production media without an apply
command and a reviewed plan.

## Queue Roles

```text
archive-inspector/      producer: inspect and normalize raw payloads
comicinfo-resolver/    consumer: resolve identity and report only
```

The Archive Inspector produces completed series directories. The ComicInfo Resolver
consumes those directories and does not write XML, sidecars, archives, or cache rows in
the dry-run.

## Backpressure Rule

- Archive Inspector may process up to 10 items for this test.
- It must stop claiming new work when 10 completed items exist in
  `comicinfo-resolver/`.
- The stop event must be logged with a timestamp and queue count.
- The resolver may start only after the count reaches 10, or after an explicit timeout
  decision recorded in the report.
- The inspector must remain asleep while the resolver processes the test batch.

## Dry-Run Semantics

The dry-run uses a staging sandbox or a simulated move manifest. It must not move,
rename, extract, convert, rewrite, delete, or overwrite files in the production
JDownloader tree. It may read source archives and existing sidecars. The report must
show the proposed source and destination for every item.

## Resolver Read-Only Scope

For each of the 10 proposed series directories, the resolver may inspect:

- CBZ structure and embedded XML
- adjacent `series.json` and `cvinfo`
- current media-tree context
- local CBL cache
- local GCD data

Remote APIs are disabled for this test. The resolver writes only its Markdown report.
It must not create or update `ComicInfo.xml`, `MetronInfo.xml`, `series.json`, `cvinfo`,
CBZ files, CBL sources, or SQLite cache rows.

## Required Events

The orchestration log must contain:

1. `archive_inspector_started`
2. ten `archive_item_ready` events
3. `archive_inspector_paused queue=10`
4. `comicinfo_resolver_started mode=read-only`
5. ten resolver result events
6. `comicinfo_resolver_completed`

The final report must include event timestamps, queue counts, source/destination paths,
status, evidence sources, unresolved fields, and errors.

## Exit Criteria

The test passes only if exactly 10 items are represented in the proposed resolver queue,
the inspector pauses at the queue limit, the resolver remains read-only, and no production
archive has a changed hash, mtime, path, or contents.
