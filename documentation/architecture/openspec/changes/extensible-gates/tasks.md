## 1. Questionnaire

- [ ] 1.1 Add `enable_custom_ci` boolean question (default false) with help text describing the custom-gate contract
- [ ] 1.2 Add `local--tester.yaml` and `local--releaser.yaml` (consumer files only — never the rendered callers) to `_skip_if_exists` in `copier.yaml`

## 2. Rendered Callers

- [ ] 2.1 Render `custom` job in template tester workflow Jinja behind the flag, calling `local--tester.yaml` with existing initializer outputs (platforms, python-versions, matrix-exclusions) verbatim — no new matrix schema
- [ ] 2.2 Render `custom` job in template releaser workflow Jinja behind the flag with a normalized target input derived from the same dispatch/tag rules the publishing jobs use (no production/pre-production split)
- [ ] 2.3 Render a named tester final check (`final-gate`) only when the flag is on, covering template + custom gates with defined non-success handling; flag-off renders gain no jobs
- [ ] 2.4 Wire enabled custom results into the publish/deploy `if:` conditions (`check-if-publish` dependency cone plus PyPI, GitHub Release, publication-branch and Pages deploy jobs) so failures, cancellations, or unexpected skips withhold protected writes; keep `is-release`/`should-publish` inapplicability separate from gate results
- [ ] 2.5 Emit SHA-256 digests of downloaded distributions as `check-if-publish` outputs and verify publish-job downloads against them before any privileged write (the pinned packager exposes only a version output, so digests originate in the generated job, not `needs.package`) — flag-on renders only
- [ ] 2.6 Replace the `publish-github` executables wildcard restore (`executables--*` + `merge-multiple`) with explicit per-platform artifact names so custom uploads cannot merge into publish inputs — flag-on renders only
- [ ] 2.7 Give the `custom` caller explicit least privilege (`contents: read`, no secrets inheritance, no publishing identity)
- [ ] 2.8 Reject consumer files whose `on:` block contains any event besides `workflow_call` during template validation (positive workflow_call-only fixture, negative extra-trigger fixture)

## 3. Consumer Stubs

- [ ] 3.1 Add `local--tester.yaml` stub that fails loudly until implemented, declaring the input contract
- [ ] 3.2 Add `local--releaser.yaml` stub that fails loudly until implemented, declaring the input contract
- [ ] 3.3 Verify a fresh copy with flag off renders no custom lane and CI is green; with flag on renders callers plus stubs and CI is red until stubs are filled

## 4. Verification (no family cut — `gha-1` refs retained)

- [ ] 4.1 Update an enabled project in both flag directions plus a repeat update: byte-compare customized locals (identical), confirm no stale `uses`/`needs` references after disable
- [ ] 4.2 Run an end-to-end publication-eligibility scenario with a failing stub (protected writes withheld) and a working gate (writes proceed per eligibility) — assert eligibility, not just workflow color; cover the Pages-only case and a mismatched tag
- [ ] 4.3 Verify the tester `final-gate` reports failure (not skip, not success) for at least one failed prerequisite, one unexpectedly skipped prerequisite, and one inner-required-skip-masked-by-wrapper-success fixture
- [ ] 4.4 Verify release-path affirmative completion with fixtures: an inner-required-skip in the release path fails the release closed, and an all-success control (including publication-off docs) proceeds exactly per predicates; producer-job success and gate success asserted as separate checks
- [ ] 4.5 Cover the late wheel-metadata refusal with a mismatched tag/version fixture: `check-if-publish` reports ineligible and no publish job runs
- [ ] 4.6 Verify writer boundaries with non-publishing fixtures: `publish-github` `always()` boundary (including its non-tag-gated attestation step), publication-disabled Pages path, and whole-run cancellation never counting as success
- [ ] 4.7 Audit the trust boundary: no secrets/OIDC/deployment rights in the custom caller, publish jobs pinned to template-owned artifact producers by explicit current-run name (no wildcards), publisher-consumed names reserved against custom uploads, diagnostics separated from trusted outputs
- [ ] 4.8 Verify the accidental-collision fixtures (exact and near-match) resolve to expected output or no write across distributions, executables, coverage, and the default Pages artifact, in non-publishing runs; record the single-trust-domain premise and its operator prerequisites (restricted tag creation, dispatch/ref selection)
- [ ] 4.9 Cover the per-destination mapping cases in the eligibility verification, broken out by writer (publication branch, Pages deploy, attestations, GitHub Release): matching tag push with publication enabled (production PyPI), manual TestPyPI dispatch, manual PyPI dispatch off-tag (publish skipped, branch still updated), mismatched tag (test/report only), publication-disabled branch update under gate control
- [ ] 4.10 Audit the consumption paths (check-if-publish/publish-pypi exact restores, publish-github exact + explicit per-platform restores, documenter coverage consumption) against the pinned-producer rule, including the overlapping-name fixtures
- [ ] 4.11 Dogfood the template onto this repo with flag off; confirm rendered diff shows no behavior change and CI is green
- [ ] 4.12 Document branch-protection activation/rollback sequencing as operator-owned alongside rollout

## 5. Docs

- [ ] 5.1 Document the contract (flag, inputs, stub-filling, escape hatch, permission boundary, release-eligibility wiring) in `documentation/applying-template-updates.md`

## Deferred (not implementation — no checkboxes)

- Cutting a `gha-2` family: deferred unless a shared `xrepo--*` input or output actually changes. Revisit only with a named incompatible interface.
- Rust Template Owner adaptation review: review-routing, handled alongside Tier-1/Tier-2 flow, not an implementation step.
- Tier-2 review of the publication/permission contract: required before implementation per Tier-1.
- Per-release approval gates and publish-environment protections (tag rules, required reviewers, dispatch constraints): explicitly deferred follow-ups (todos/handbook/40, todos/handbook/41); documented operator practice only, no template enforcement in this change.
