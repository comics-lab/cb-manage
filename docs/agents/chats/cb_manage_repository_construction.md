# CB-MANAGE Repository Construction

> Logging rules: [`Extended_Logging_Runbook.md`](../system/runbooks/Extended_Logging_Runbook.md)
>
> Status: Active, append-only construction record

## Construction Outline

- [x] Establish repository `.gitignore` baseline.
- [x] Create the guide-derived directory structure.
- [x] Create `AGENTS.md` and `AGENTS-master.md` outlines.
- [x] Create non-secret `config/local.yaml`.
- [x] Transfer and adapt the SSO-MANAGE logging policy.
- [x] Install structured event and usage-accounting schemas.
- [x] Install lifecycle capture, validation, reporting scripts, and tests.
- [x] Install the usage-accounting persona, contract, and skill.
- [x] Add the initial agent registry, routing matrix, and system index.
- [ ] Populate the broader CB-MANAGE persona, contract, and skill inventory.
- [ ] Add repository governance validation for the complete load chain.
- [ ] Create the first handoff/resume pair after the initial construction phase.
- [ ] Review and trust `.codex/hooks.json`, then verify capture in a new session.
- [ ] Define approved pricing profiles only if cost accounting is required.
- [x] Audit SSO-MANAGE wiki workflows, workflow helpers, and local Git hooks.
- [ ] Install and adapt the wiki synchronization workflow and helper scripts.
- [ ] Add a `WIKI_PUSH_TOKEN` Actions secret if the repository `GITHUB_TOKEN`
  cannot push to the separate wiki repository.
- [x] Initialize a truth index and external source manifest for URL-backed documentation.
- [ ] Identify and verify the first comic archive and software documentation sources.

## Session — 2026-11-03 — Logging parity bootstrap

### Objective

Give CB-MANAGE the same privacy-preserving human-readable and structured logging
baseline used by SSO-MANAGE without copying historical SSO logs or domain data.

### Source Components

- SSO-MANAGE extended logging runbook and usage-accounting governance.
- Usage-accounting persona, contract, skill, schemas, scripts, and regression tests.
- Repository-local Codex hook configuration.

### Changes

- Created the complete logging directory and documentation chain.
- Adapted repository identity from SSO-MANAGE to CB-MANAGE.
- Preserved append-only, redaction, uncertainty, and explicit-governance rules.
- Kept authentication, prompts, tool payloads, SQL, PII, and hidden reasoning out of the transfer.

### Validation

- Five regression tests passed.
- All four Python scripts compiled successfully.
- The repository skill passed the bundled `quick_validate.py` check.
- Hook and schema JSON files parsed successfully.
- The initial 12-record event ledger passed lifecycle validation.
- The first Markdown and JSON aggregate reports were generated successfully.
- No usage ledger was created because no authoritative or explicitly estimated
  token record was available; usage remains `unpriced/unknown`.

### Next Checkpoint

Review the generated files, enable trusted hooks in a new session, and update
this record with observed capture results.

## Session — 2026-11-03 — Wiki and Git hook assessment

### Observed State

- GitHub Wiki is enabled and the `comics-lab/cb-manage.wiki.git` repository is
  initialized and reachable on its `master` branch.
- GitHub Discussions is enabled.
- GitHub Actions is enabled with all actions allowed.
- CB-MANAGE has no checked-in `.github` workflows or workflow helper scripts.
- No repository Actions secrets are currently listed.

### Reusable SSO-MANAGE Components

- `.github/workflows/sync-wiki.yml` is the primary reusable workflow.
- `.github/scripts/sync-to-wiki.sh` builds a bounded Markdown manifest, creates
  wiki-safe page slugs, rewrites internal links, builds a sidebar, and pushes
  the wiki repository.
- `.github/scripts/bootstrap-local-config.sh` validates and loads the non-secret
  project identity used by the workflow.

### Deferred Components

- `backup.yml` depends on the CSU organization reusable workflow and cloud
  identity; do not copy it until cross-organization access is verified.
- Transcript capture/archive helpers require a transcript policy and source
  tree that CB-MANAGE does not yet have.
- SSO-MANAGE `.git/hooks` contains only generated Git LFS hooks. CB-MANAGE has
  no LFS tracking rules, so those hooks should not be copied.

### Next Checkpoint

Adapt and dry-run the wiki sync files locally, then add the required token only
if a live workflow proves that the default `GITHUB_TOKEN` cannot push the wiki.

## Session — 2026-11-03 — Truth registry scaffold

### Objective

Establish a source-of-truth index and manifest for external URLs and
documentation without pre-approving unspecified sites.

### Changes

- Added `truth/TRUTHS_INDEX.md`, `truth/EXTERNAL/manifest.md`, a per-source
  template, and the source architecture policy.
- Transcribed eleven candidate URLs from the user-provided intake stub into the
  manifest, then removed the redundant stub after checking the migration.
- Added the intake stub to the truth index; all external entries remain
  `Candidate` and unverified.
- Kept the registry scoped to CB-MANAGE's comic archive and related software;
  no unrelated domain sources were copied from SSO-MANAGE.

### Validation

- Local Markdown links resolve; `git diff --check` passed.
- URL reachability, page contents, ownership, and authority were not checked;
  each entry is explicitly marked `Candidate` and `Not verified`.

