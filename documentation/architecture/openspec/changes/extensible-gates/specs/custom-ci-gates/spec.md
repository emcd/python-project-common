## ADDED Requirements

### Requirement: Opt-in Custom CI Gates
The template SHALL offer an `enable_custom_ci` Copier question (default
false) that renders `custom` gate jobs calling consumer-owned reusable
workflows. With the flag off, no custom lane is rendered at all.

#### Scenario: Default copy renders no custom lane
- **WHEN** a developer generates a project without enabling custom CI
- **THEN** the rendered tester and releaser workflows contain no `custom`
  job and no reference to `local--tester.yaml` or `local--releaser.yaml`

#### Scenario: Enabled copy renders thin custom callers
- **WHEN** a developer generates a project with `enable_custom_ci` true
- **THEN** the rendered tester and releaser workflows each contain a
  `custom` job that calls the corresponding consumer-owned
  `local--*.yaml` workflow with the declared inputs

### Requirement: Consumer File Ownership
Consumer-owned gate files SHALL survive template updates byte-identical;
rendered callers remain template-owned and re-render on every update.

#### Scenario: Updates never overwrite consumer gates
- **WHEN** a Copier update runs against a project with implemented
  `local--tester.yaml` / `local--releaser.yaml`
- **THEN** the update leaves those files byte-identical (`_skip_if_exists`
  ownership), re-renders the thin caller jobs, and a repeat update is
  a no-op on all four files

#### Scenario: Unimplemented gate reads red
- **WHEN** a project enables custom CI but leaves a stub
  unimplemented
- **THEN** the stub step fails loudly (non-zero exit) so CI reads red,
  never green

#### Scenario: Rollback leaves no stale references
- **WHEN** a project flips `enable_custom_ci` back to false and updates
- **THEN** the rendered workflows contain no `custom` job, no
  `local--*.yaml` reference in `needs` or final-gate evaluation, and
  CI behaves exactly as a project that never enabled the flag

### Requirement: Release-Eligibility Wiring
Enabled applicable custom gates SHALL join the release-eligibility
boundary. Gate failures, cancellations, or unexpected skips MUST NOT
permit protected writes.

#### Scenario: Failing custom gate blocks publication
- **WHEN** an enabled applicable custom gate fails, is cancelled, or
  skips unexpectedly
- **THEN** PyPI publication, GitHub Release creation, Pages
  deployment, publication-branch updates, and attestations are all
  withheld for that run

#### Scenario: Working custom gate permits publication
- **WHEN** all enabled applicable gates succeed and the release is
  otherwise eligible
- **THEN** protected writes proceed exactly as without custom gates

#### Scenario: Publication disabled still allows eligible Pages
- **WHEN** publication is disabled but the run is otherwise eligible
  for documentation deployment
- **THEN** PyPI publication and GitHub Release creation are withheld
  while Pages deployment proceeds, and an enabled custom gate still
  controls the Pages deploy

#### Scenario: Mismatched tag withholds everything
- **WHEN** the tag does not match release dispatch rules
- **THEN** all protected writes are withheld independent of custom
  gate results, and gate jobs that never render are not treated as
  failures

#### Scenario: Pages-only eligibility gated end to end
- **WHEN** a run is eligible only for Pages deployment (not a
  publishable release) and custom gates are enabled
- **THEN** Pages deployment requires custom gate success, evaluated
  against the same normalized target as publishable releases

### Requirement: Normalized Gate Target Without Cycles
The custom gate SHALL take a single normalized `target` input derived
from dispatch/tag rules, covering publishable releases, Pages-only
runs, and non-release runs. Gate inputs SHALL come from upstream
initialize/dispatch outputs, never from `check-if-publish` outputs.

#### Scenario: Target covers all dispatch shapes
- **WHEN** a run dispatches as a publishable release, a Pages-only
  build, or a plain validation run
- **THEN** the normalized target names that shape, and the gate
  evaluates only the destinations the shape makes eligible

#### Scenario: No evaluation cycle
- **WHEN** the `check-if-publish` job depends on `docsgen`, and
  `docsgen` depends on custom gate success
- **THEN** the gate's target and applicability inputs resolve without
  reading `should-publish` or any other `check-if-publish` output

### Requirement: Per-Destination Planned Mapping
The normalized target SHALL map each dispatch shape to planned
destinations per destination, derived from the releaser triggers
(tag push matching `v[1-9]+.*`, or manual dispatch with a
`which-pypi` choice) and the per-writer predicates below.
Destinations are labeled planned, never guaranteed: downstream
eligibility (metadata match, attestation success) still applies.

Writer predicates (existing behavior, retained):
- `docsgen` runs on `is-release` with `contents:write`,
  `id-token:write`, `pages:write`; it invokes the pinned `gha-1`
  documenter (production default true), so the website
  publication-branch update is a protected write separate from the
  documenter's tag-only Pages deployment.
- `publish-pypi` runs only when `should-publish` is true AND
  (`which-pypi` is `testpypi` or the ref is a tag); ordinary matching
  tag pushes carry no inputs and therefore target production PyPI.
- `publish-github` runs on `always()` plus `should-publish` and
  upstream successes; its attestation step is NOT tag-gated, but
  Create Release and Publish Artifacts steps are tag-gated.
- Mismatched tags yield `is-release` false: docsgen and package
  never run, so the run is test/report only.

#### Scenario: Matching tag push targets production
- **WHEN** dispatch is a tag push matching the tag pattern, the
  tag version matches the package version, and publication is
  enabled
- **THEN** production PyPI publication, GitHub Release creation,
  and the publication-branch/Pages update are all planned, each
  still subject to gate success and its own downstream checks

#### Scenario: Manual TestPyPI dispatch
- **WHEN** dispatch is manual with `which-pypi` left at its
  `testpypi` default (any ref)
- **THEN** TestPyPI publication is planned if publication is
  enabled; GitHub Release steps execute only on tag refs;
  attestation still executes as a protected write under the gate

#### Scenario: Manual PyPI dispatch off-tag publishes nothing
- **WHEN** dispatch is manual with `which-pypi` set to `pypi` on a
  non-tag ref
- **THEN** `publish-pypi` is skipped by its job condition, while
  `docsgen` still runs and updates the publication branch

#### Scenario: Mismatched tag runs test and report only
- **WHEN** dispatch is a tag that does not match the package version
- **THEN** no destination is planned, `docsgen` and `package` never
  run, and nothing publishes or deploys regardless of gate results

#### Scenario: Publication disabled still deploys the branch
- **WHEN** publication is disabled but the run is otherwise eligible
- **THEN** no publish jobs render at all, while `docsgen` still
  performs the publication-branch update; an enabled custom gate
  still controls that write

#### Scenario: Late metadata mismatch blocks package path only
- **WHEN** built wheel metadata disagrees with the tag version
- **THEN** the existing version check withholds the package and
  GitHub Release path; `docsgen`/Pages for that run already
  executed upstream of `check-if-publish` and are unaffected by
  the mismatch control

### Requirement: Named Tester Final Check
The rendered tester workflow SHALL include a stably-named final check
job, `final-gate`, whenever the flag is on. It MUST NOT report success
if any required template or custom prerequisite fails, is cancelled,
or unexpectedly skips — including cases where normal `needs` handling
would skip the aggregate instead of reporting failure. The job name
is stable and documented for branch protection rules.

#### Scenario: Prerequisite failure fails the check
- **WHEN** any required template or custom prerequisite fails or is
  cancelled
- **THEN** `final-gate` reports failure via `always()` plus explicit
  per-dependency result evaluation, never bare `needs` passthrough

#### Scenario: Unexpected skip fails the check
- **WHEN** any required prerequisite skips for a reason outside the
  designed inapplicability paths
- **THEN** `final-gate` reports failure rather than skipping silently

#### Scenario: Inner required skip fails the check
- **WHEN** a required inner job skips while its wrapper reports
  success
- **THEN** `final-gate` reports failure: affirmative completion is
  required, wrapper success never stands in for it

#### Scenario: Writer boundaries hold under always()
- **WHEN** verification uses non-publishing fixtures against the
  `publish-github` `always()` boundary and the
  publication-disabled Pages path
- **THEN** no protected write executes on gate failure, and
  publication-disabled Pages still deploys only under gate success

#### Scenario: Whole-run cancellation is not success
- **WHEN** the whole run is cancelled
- **THEN** the outcome never counts as success, though no runnable
  aggregate is required in that case

### Requirement: Least-Privilege Custom Jobs
Custom caller jobs SHALL run with explicit least-privilege token
permissions and MUST NOT inherit secrets, publishing credentials, or
deployment identity.

#### Scenario: Custom job permissions
- **WHEN** the `custom` job runs on any trigger including pull requests
- **THEN** it holds at most `contents: read`, inherits no secrets,
  and cannot perform publishing or deployment writes

#### Scenario: Privilege stays in existing jobs
- **WHEN** publishing or deployment authorization is required
- **THEN** it remains in the existing privileged jobs, never in
  consumer gate code; any future grant is an explicit reviewed change,
  not an implicit part of the flag

### Requirement: Consumer Trust Boundary
Custom gate jobs SHALL run without secret-bearing or
deployment-capable environments. Release runs are a single trust
domain: the selected release ref, gate code, actions, and other
executable inputs are trusted for release, and untrusted
pull-request contributions cannot feed writer runs — established by
tag/manual triggers (run separation), not by owner identity or code
approval. Publish jobs SHALL consume only current-run artifacts
from named template-owned producers via explicit pinned names (no
wildcards); publisher-consumed names are reserved and custom jobs
SHALL NOT upload under them. An overlapping-name fixture SHALL
verify accidental collisions (exact and near-match) resolve to
expected output or no write, covering distributions, executables,
coverage, and the default Pages artifact. Deliberate same-run
substitution is out of scope: a run-ID suffix alone is not
isolation, and same-run executable inputs are trusted for release
by premise — if that premise ever fails, enforced binding becomes
necessary before enabling the configuration.

#### Scenario: No secret or deployment capability
- **WHEN** the custom job runs on any trigger
- **THEN** it holds no secrets, no OIDC identity, no pages or
  deployment rights, and no environment carrying them

#### Scenario: Reserved publisher names fail closed
- **WHEN** a custom job uploads an artifact under a reserved
  publisher-consumed name (exact or near-match)
- **THEN** verification shows the privileged path consumes the
  trusted producer's artifact or withholds the write; silent
  substitution never occurs

#### Scenario: Accidental collisions resolve safely
- **WHEN** fixtures exercise exact and near-match accidental
  collisions across distributions, executables, coverage, and the
  default Pages artifact in non-publishing runs
- **THEN** each resolves to expected output or no write

#### Scenario: Diagnostics stay separate from trusted outputs
- **WHEN** custom gates emit logs, summaries, or annotations
- **THEN** those outputs never serve as attestations, distributions,
  or any other trusted producer output

#### Scenario: Privileged writes require successful producers
- **WHEN** a privileged write is evaluated
- **THEN** it requires successful (not merely non-failed) producer
  jobs, and unexpected skips withhold the write

### Requirement: Distribution Handoff Integrity
`check-if-publish` (a generated, template-owned job) SHALL,
when the flag is on, record SHA-256 digests of the distributions
it observes as job outputs. Each downstream distribution consumer
(`publish-pypi`, `publish-github`) SHALL then verify its own
downloads against those outputs before its write; a missing or
mismatched digest withholds that write. Flag-off renders contain
no digest steps. This covers re-download integrity only: no source
provenance, no initial-collision detection, and no executables,
coverage, or Pages binding — those paths rely on explicit names
plus the separate accidental-collision fixtures.

#### Scenario: Digest mismatch withholds publication
- **WHEN** a publish job's downloaded distribution digest does not
  match the `check-if-publish` recorded output
- **THEN** that job does not execute its write

#### Scenario: Overlapping-name fixture with digest check
- **WHEN** fixtures change the distribution bytes between the
  `check-if-publish` baseline capture and a downstream publish
  job's re-download (or omit the recorded digest)
- **THEN** the digest check fails closed; verification asserts the
  mismatch path, not merely file presence. Collisions already
  present at baseline capture are covered by the separate
  accidental-collision fixture, not by this check

### Requirement: workflow_call-Only Consumer Triggers
Consumer-owned gate files SHALL declare `workflow_call` as their
sole event (reusable workflows require an `on:` block); any
additional event is rejected. A consumer-added
`pull_request_target` (or any) trigger would bypass the caller's
trigger topology entirely.

#### Scenario: workflow_call-only passes
- **WHEN** a consumer file declares only `on: workflow_call`
- **THEN** template validation accepts it

#### Scenario: Extra trigger fails closed
- **WHEN** a consumer file declares `workflow_call` plus any other
  event
- **THEN** template validation rejects it before the flag can be
  enabled for that consumer

### Requirement: Trusted Dispatch Practice
Tester pull-request runs SHALL remain outside all writer input
scopes; privileged writes occur only on matching tag dispatches
or operator-chosen manual dispatches. Dispatch selection itself
is documented operator practice, not template enforcement, and
no trust-based refusal for a manual ref is implemented or
promised.

#### Scenario: Mismatched tag withholds writers
- **WHEN** the tag does not match release dispatch rules
- **THEN** no writer job executes, independent of custom gates

#### Scenario: Non-tag manual PyPI selection skips publish
- **WHEN** a manual dispatch selects a non-tag ref with `which-pypi`
  set to `pypi`
- **THEN** the publish job skips while `docsgen` may still update
  the publication branch

#### Scenario: Non-tag manual TestPyPI may publish
- **WHEN** a manual dispatch selects any ref with `which-pypi`
  left at `testpypi` and publication is enabled
- **THEN** TestPyPI publication proceeds subject to gate success
  and downstream checks

#### Scenario: Tester runs never feed writers
- **WHEN** tester workflows run on pull requests
- **THEN** no artifact they produce is consumed by any privileged
  write in any run

### Requirement: Release-Path Affirmative Completion
Writer predicates SHALL require affirmative success of required
jobs — producer jobs and custom gates as separate checks — never
mere non-failure. An inner required skip masked by wrapper
success in the release path SHALL fail the release closed, and
this negative plus an affirmative control SHALL be exercised at
the writer predicates, including the publication-off docs path.

#### Scenario: Inner release-path skip fails closed
- **WHEN** a required job in the release path skips while its
  wrapper reports success
- **THEN** no privileged write executes for that run

#### Scenario: Affirmative control at writer predicates
- **WHEN** fixtures drive the release path with all required jobs
  reporting success, including publication-off docs deployment
- **THEN** the eligibility decision and each writer proceed exactly
  as the predicates specify

### Requirement: gha-1 Compatibility
The extensible contract SHALL reuse the existing `gha-1`
reusable-workflow refs unchanged. No shared `xrepo--*` interface
changes, so no major family cut is needed.

#### Scenario: Shared refs unchanged regardless of flag
- **WHEN** a project pins reusable workflows to `gha-1`
- **THEN** the shared workflow refs and their behavior are identical
  before and after this contract lands, whether or not the project
  enables the flag

#### Scenario: Flag-off generated behavior unchanged
- **WHEN** a project leaves `enable_custom_ci` false
- **THEN** its rendered workflows are behavior-identical to before
  this contract (no new jobs); flag-on renders add jobs by design
