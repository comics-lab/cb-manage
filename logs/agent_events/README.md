# Agent Event Ledger

`agent-events.jsonl` is the append-only structured lifecycle and governance
ledger. It stores allowlisted metadata and approved identifiers only.

Generated aggregate reports are stored under `reports/`. Usage telemetry, when
available, is stored separately under `../usage/usage.jsonl`.

Do not store prompts, responses, tool payloads, credentials, SQL, database
output, PII, or hidden reasoning in this directory.

