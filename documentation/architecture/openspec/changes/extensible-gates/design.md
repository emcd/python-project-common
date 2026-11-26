# Design: Extensible Custom Gates (gha-1 retained)

## Context

Template tester/releaser workflows are rendered per project from Jinja;
any consumer-specific gate baked into those files is template-owned and
therefore clobbered or diverged by every Copier update. Rust-project-common
solved this with thin rendered callers plus consumer-owned `local--*.yaml`
files under `_skip_if_exists`, proven by nbspec (reference), cistella,
and litrpg. Our reusable workflows are version-tagged (`gha-1`); since
no shared `xrepo--*` input or output changes, no new family is needed.
Stakeholders: Template Owner (implements), downstream consumers (adopt
opt-in), Rust Template Owner (offered review of the adaptation draft).

## Goals / Non-Goals

Goals: opt-in custom gates that survive updates untouched; fail-closed
defaults (flag off = no custom lane); unimplemented gate reads red;
enabled gates joined to the real release-eligibility boundary (not just
workflow color); least-privilege custom jobs; `gha-1` refs and behavior
unchanged.

Non-Goals: changing any shared reusable-workflow interface; migrating
existing consumers (adoption is per-project, later); adding new gates
to the template's own default lane.

## Decisions

- **Retain `gha-1` refs; no family cut.** Every new behavior lives in
  generated callers and consumer files; initializer outputs the custom
  jobs need already exist. Alternative (new `gha-2` family) rejected:
  a major cut with no incompatible shared interface is version theater,
  and Tier-1 review correctly called it out.
- **`enable_custom_ci`, default false.** Matches the rust contract and
  keeps first-copy CI green for consumers that do not need custom gates.
  Alternative (always render + skip when stub) rejected: it normalizes
  red CI on fresh copies.
- **Fail-loud stubs, not no-op stubs.** An unimplemented gate must read
  red (exit 1 with a pointer message), never green. Alternative (empty
  success job) rejected: silent green is the failure mode being
  eliminated.
- **`_skip_if_exists` for the two local files only; callers stay
  template-owned.** File-boundary ownership (not line-boundary):
  Copier 3-way merge drops project-identical lines silently in our
  tree, so the boundary must be a file boundary. Alternative (protect
  all four files) rejected: it would freeze caller evolution, block
  false-to-true adoption and true-to-false rollback, and strand stale
  `uses`/`needs` references.
- **Custom results wired into publish `if:` conditions, not just a
  summary.** An `always()` summary can mark a run red after deployment;
  that is not a gate. Enabled applicable gates join
  `check-if-publish`'s dependency cone; publish and deploy jobs'
  conditions require their success. Legitimate inapplicability
  (mismatched tag, publication disabled) bypasses via the existing
  `is-release`/`should-publish` outputs, never via gate-result
  conflation.
- **Named tester final check (`final-gate`) only when the flag is
  on.** Flag-off renders stay behavior-identical (no new jobs);
  flag-on renders gain `final-gate` over template + custom gates,
  evaluated with `always()` plus explicit per-dependency results so
  failures, cancellations, and unexpected skips (including
  needs-driven aggregate skips) all report failure. The name is
  stable for branch protection. Alternative (unconditional final
  gate) rejected: it would change every consumer's workflow for zero
  benefit when the flag is off.
- **Least-privilege custom caller: `contents: read`, no `secrets:
  inherit`, no publishing identity.** Consumer tester code can run on
  pull requests; it must not be able to publish or deploy.
  Alternative (inherit caller permissions) rejected: privilege would
  flow to arbitrary consumer code by flipping one flag.
- **Single gate interface with normalized target input.** Reuses the
  existing initializer output keys/semantics verbatim — no second
  matrix schema. Production/pre-production is not split into separate
  custom workflows; one custom job takes a normalized target derived
  from the same dispatch/tag rules the publishing jobs use.

## Per-Destination Mapping

Planned destinations derive from the normalized target plus the
releaser triggers (tag push matching `v[1-9]+.*`, or manual dispatch
with a `which-pypi` choice) and per-writer predicates — never from
branch-push shapes, which do not trigger the releaser at all.
Downstream eligibility (metadata match, attestation success) stays
where it is today, and destinations are planned, not guaranteed:

| Dispatch shape | TestPyPI | GitHub Release (tag-gated steps) | Attestations (not tag-gated) | Publication branch | Pages deploy |
|---|---|---|---|---|
| Matching tag push (inputs absent → pypi) | — (production PyPI planned) | planned (tag-gated steps) | planned | planned via docsgen | planned via docsgen |
| Manual dispatch, testpypi default | planned if publication enabled | tag-gated steps only on tag refs | still runs (protected write under gate) | planned via docsgen | only on tag refs |
| Manual dispatch, pypi selected, non-tag | publish-pypi skipped by job condition | — | — (publish-github skipped) | docsgen still updates the branch | — (no tag ref) |
| Mismatched tag | — | — | — | — (docsgen/package never run) | — |
| Publication off, otherwise eligible | no publish jobs rendered | — | — (no publish job) | docsgen still updates the branch, under gate control | only on tag refs, under gate control |

`docsgen` sits outside `enable_publication` and runs on `is-release`
alone, so the publication-branch update is a protected write the
gate must cover even when no publish jobs render. Late
wheel-metadata mismatch stays a downstream control in the existing
version-check jobs (package/Release path only — `docsgen`/Pages for
that run already executed upstream of `check-if-publish`). The gate
never reads `should-publish` or other `check-if-publish` outputs:
`check-if-publish` already depends on `docsgen`, which depends on
custom success, so that read would form a cycle.

## Trust Boundary

Custom gates are owner-authored code with the same trust as the
generated workflows; the `_skip_if_exists` boundary exists for
update stability, not principal isolation. Release runs are a
single trust domain by premise: the selected release ref, gate
code, actions, and other executable inputs are trusted for
release because the operator chose reviewed refs — matching tags
or deliberate manual dispatches as documented practice — not
because triggers alone establish anything. Untrusted
pull-request contributions cannot feed writer runs: tester runs
are writer-free and no tester artifact feeds a privileged write.
The safeguards are capability removal (least privilege, no
secrets, no publishing identity) plus consumption pinning: publish
jobs consume only current-run artifacts from named template-owned
producers via explicit pinned names, with publisher-consumed names
reserved. When the flag is on, the `publish-github` executables restore
drops its `executables--*` wildcard (`merge-multiple`) in favor of
explicit per-platform names — generated code only, no
shared-interface change. Flag-off renders keep stock restores. The overlapping-name fixture covers exact and near-match
accidental collisions across distributions, executables, coverage,
and the default Pages artifact. Separately, distribution
re-download integrity is observed-byte only: `check-if-publish`
records digests of what it downloaded, and each downstream
distribution consumer re-verifies its own re-download against
those outputs — a mismatch fails closed. A collision already
present at baseline capture need not trigger a mismatch; the
digest fixture MUST change the bytes between baseline capture and
the downstream read (or omit the digest) to count as a
verification. Initial-collision detection stays a separate
fixture, not a digest property. Consumer files declare
`workflow_call` as their sole event; template validation rejects
any additional event, so no consumer-added trigger can bypass the
caller topology. Operator prerequisites (restricted tag creation,
dispatch/ref selection, per-release approvals) are documented
practice, explicitly deferred as follow-ups
(todos/handbook/40, todos/handbook/41) — local development is
primary, and GitHub-specific enforcement stays out of scope
pending the Praetor and agent identities direction.

## Risks / Trade-offs

- [Consumers enable the flag but never implement → permanent red] → Mitigation: stub message names the exact file and the flag to flip back; runbook documents the escape hatch.
- [Shared drift between template callers across consumers] → Mitigation: callers re-render from one Jinja source on every update.
- [Final-gate `needs` mismatch when flag flips mid-PR] → Mitigation: needs list is rendered from the same flag, so caller and gate always agree within one render.
- [Scope: Pages deploy joins the protected set] → Deliberate: `docsgen` carries `pages: write` on `is-release` alone, so an enabled failing gate must also withhold it; documented as an explicit choice, not an accident.
- [Review: Rust Owner's adaptation feedback is worthwhile independently] → Carried as a deferred review-routing item, not an implementation task.

## Migration Plan

1. Implement in template (question, Jinja callers, stubs,
   `_skip_if_exists` for the two local files).
2. Verify: update an enabled project both flag directions plus a
   repeat update; byte-compare customized locals; confirm no stale
   references after disable; e2e publication-eligibility scenario
   with failing stub (writes withheld) and working gate (writes
   proceed).
3. Dogfood onto this repo (flag off): rendered diff shows no behavior
   change and CI is green.
4. Downstream adoption per project: flip flag, fill stubs — each its
   own commit, no coordinated flag day.
5. Rollback: flag off + update; custom jobs vanish from the render;
   local files remain on disk, harmless.
6. Branch-protection activation/rollback sequencing (which checks to
   require, in what order, and how to stand down) is operator-owned
   and documented alongside rollout, not in the template.

## Open Questions

None remaining that block the contract: input schema (reuse
initializer keys verbatim) and single-gate interface (normalized
target) are decided above. Dogfood render is the final arbiter of the
exact input threading.
