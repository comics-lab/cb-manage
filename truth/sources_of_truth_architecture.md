# CB-MANAGE Sources of Truth Architecture

> Owner: Richard
> Source: CB-MANAGE operating model
> Last Verified: 2026-11-03
> Scope: External URLs, local documents, imported references, and generated records
> Status: Active

## Purpose

Define how CB-MANAGE identifies, reviews, and uses source material for the
comic archive and related software projects. The goal is to make provenance
and authority clear instead of treating every reachable page or file as
equally reliable.

## Source Classes

- **External reference:** Public documentation or standards identified by URL.
- **Local operational truth:** A reviewed project decision, procedure, or
  configuration record maintained in this repository.
- **Imported reference:** A copied or synchronized document whose original
  source, retrieval date, and limits are recorded.
- **Generated record:** An inventory or report valid for a stated generation
  time and input set; it may need refresh.
- **Candidate/working source:** Potentially useful material that has not passed
  authority and scope review.

## Authority and Intake

A source becomes an active truth only after its scope, owner or maintainer,
source location, verification state, and limitations are documented. Public
availability alone does not establish authority.

Use the [external source manifest](EXTERNAL/manifest.md) for URL candidates
and the [source record template](EXTERNAL/source_record_template.md) for
sources needing a fuller authority statement.

## Required Provenance

Each source record should identify:

- stable source ID and title;
- canonical URL or local path;
- source type and owner/maintainer, if known;
- exact project questions or scope it governs;
- date and method of verification;
- version, edition, or platform limits;
- review cadence and current status; and
- related local records or decisions.

Use `Unknown` or `Candidate` when evidence is missing. Do not guess.

## Usage Rules

- Prefer the primary publisher, maintainer, or official project documentation.
- Cite the specific page or section that supports a decision.
- Keep external source claims separate from CB-MANAGE decisions and local
  implementation behavior.
- When local behavior differs from upstream documentation, record the local
  exception and its owner; do not rewrite the upstream source's meaning.
- Record material source promotions, deprecations, or changes in the relevant
  topic/construction log.
- Never store credentials, access tokens, or private URLs in the public truth
  registry.

