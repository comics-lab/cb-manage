# Agent Usage Accounting Governance

## Source precedence

1. Provider usage API or invoice, when model and billing period match.
2. Runtime usage event or exit summary.
3. User-supplied runtime summary preserved as numeric data.
4. Local estimate based on a documented tokenizer or runtime counter.
5. Qualitative estimate only; never convert it to money.

Never merge sources without retaining `source` and `source_timestamp`.

## Canonical dimensions

| Field | Meaning | Rule |
| --- | --- | --- |
| `input_tokens` | Active input sent for processing | Exclude cached tokens unless source defines otherwise |
| `cached_input_tokens` | Reused input reported by runtime | Diagnostic; do not add to total by default |
| `output_tokens` | Generated output | Reasoning inclusion follows source definition |
| `reasoning_tokens` | Internal reasoning dimension | Usually a subset of output; never add twice |
| `total_tokens` | Runtime-reported total | Prefer authoritative total over recomputation |
| `cost` | Monetary estimate | Only with a dated pricing profile |

Common check: `total_tokens ≈ input_tokens + output_tokens`. If the provider
defines another formula, preserve that definition and use the provider total.
Cached input may be much larger than active input because context is reused.

## Allocation and confidence

Use `direct` when runtime attribution is explicit, `shared` when no defensible
split exists, and `proportional` only with a recorded allocation basis. Child
allocations must not exceed the parent total.

- `authoritative`: provider/runtime total with matching identity and time.
- `reported`: user-provided exit summary.
- `estimated`: documented local approximation.
- `unknown`: insufficient evidence; no cost calculation permitted.

## Cost calculation

For per-million-token rates:

`cost = input_billable_tokens / 1,000,000 * input_rate`

`+ output_billable_tokens / 1,000,000 * output_rate`

Apply cached-input or reasoning rates only when explicitly defined. Keep
currency, pricing date, model version, and source with the result. Otherwise
report `unpriced`.

## Review gates

- Collection: confirm scope, source, identifiers, and redaction.
- Reconciliation: check dimensions, parent/child totals, duplicates, timestamps,
  and whether reasoning is nested within output.
- Publication: publish only approved aggregates and metadata; remove prompts,
  SQL, database output, credentials, tokens, and PII. State that accounting is
  not necessarily provider billing.
