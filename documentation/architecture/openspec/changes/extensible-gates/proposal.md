## Why

Downstream projects that need project-specific CI gates (extra linters, deployment checks, integration suites) must carry those gates inside template-rendered workflow files, so every Copier update either clobbers custom gates or forces consumers to carry divergence. Rust-project-common proved the fix in production (nbspec reference implementation, cistella and litrpg adopting): custom gates live in consumer-owned files that template updates never touch.

## What Changes

- Add an `enable_custom_ci` Copier question (default false) that renders opt-in `custom` gate jobs in the template tester and releaser workflows.
- The `custom` jobs call consumer-owned `local--tester.yaml` / `local--releaser.yaml` reusable workflows as independent gates; final-gate evaluation includes them only when rendered.
- ONLY the consumer files are `_skip_if_exists`-protected. Rendered callers stay template-owned and re-render on every update; consumer implementations are never overwritten.
- Ship fail-loud stubs for both local files on first copy: an unimplemented gate reads red, never green. With the flag off, no custom lane is rendered at all.
- Enabled applicable gates join the release-eligibility boundary: failures, cancellations, or unexpected skips must not permit protected writes (PyPI publish, GitHub Release creation, Pages deploy). Legitimate inapplicability (mismatched tag, publication disabled) stays separate from gate results; per-destination mapping (TestPyPI needs no tag, Release/Pages require tags) derives from the normalized target alone.
- Custom gates are owner-authored and trusted like the generated workflows; the boundary covers what they execute and reference (untrusted contributions, third-party actions, accidental collisions): least privilege, consumption pinning (explicit artifact names, no wildcards), distribution digest checks (`check-if-publish` records observed digests; publish jobs verify before writing), and `workflow_call`-only consumer triggers.
- Custom jobs run least-privilege (`contents: read`, no secret inheritance, no publishing identity); authorization and publishing stay in the existing privileged jobs.
- No `gha-2` family: no shared `xrepo--*` interface changes, so `gha-1` refs are retained unchanged and no major cut is needed.
- Enforcement prerequisites beyond the template (restricted tag creation, required-reviewer environments, per-release approvals) are explicitly deferred as follow-ups, not gates on this change; dispatch discipline stays documented operator practice.

## Capabilities

### New Capabilities

- `custom-ci-gates`: consumer-owned extensible tester/releaser gates — opt-in question, thin-caller rendering, consumer-file ownership, fail-loud stubs, release-eligibility wiring, permission boundary.

### Modified Capabilities

- `project-lifecycle`: reusable GHA workflow contract gains the optional custom-gate jobs; `gha-1` pins and behavior are unchanged (delta spec).

## Impact

- `copier.yaml` (new question + two `_skip_if_exists` entries), template tester/releaser workflow Jinja, two new stub files.
- Downstream adoption is opt-in per project; nothing changes behavior until a consumer flips the flag.
- Review offered by rust-project-common Template Owner on the adaptation draft.
