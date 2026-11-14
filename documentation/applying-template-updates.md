# Applying Template Updates

This guide covers updating a project built from the python-project-common
Copier template. It is template-owned: corrections land here, not in
per-project files.

## Standard update

Run the update non-interactively with the baseline data file. Copier
requires the data file as a local file, not a URL — download it first
(replace `<ref>` with the template tag under adoption), then update:

```sh
DATA_FILE="$(mktemp)" || exit 1
trap 'rm -f "$DATA_FILE"' EXIT INT TERM
python3 -c "import sys, urllib.request; urllib.request.urlretrieve('https://raw.githubusercontent.com/emcd/python-project-common/<ref>/.auxiliary/data/copier/python-baseline-3.12.yaml', sys.argv[1])" "$DATA_FILE" || exit 1
grep -q '^python_version_min:' "$DATA_FILE" || exit 1
grep -q '^python_versions:' "$DATA_FILE" || exit 1
copier update \
    --data-file "$DATA_FILE" \
    --answers-file .auxiliary/configuration/copier-answers.yaml \
    --skip-answered \
    --defaults
```

`--trust` is intentionally absent: the template declares no Jinja
extensions, tasks, or migrations, so the unsafe-features gate never
trips (verified by running updates without it). `--skip-answered` keeps
recorded answers; `--defaults` answers new defaulted questions from
their defaults, so a release that adds defaulted questions still
completes non-interactively (verified: new answers recorded at their
defaults with stdin closed). New questions *without* defaults are
required: the update fails loudly naming the question instead of
hanging — supply the value with `--data` (e.g.
`--data new_answer=value`) or answer interactively. Track the latest
release by default: a bare `copier update`
selects the latest template tag on its own (template tags sort above
package tags under PEP 440). Pin `--vcs-ref` to a tag only when a specific
version was explicitly requested; a pin that merely dodges an environment
problem is a workaround, not a fix — fix the environment instead.

The data file carries the Python 3.12 baseline answers. Without it, the
update coerces to the new defaults (with `--defaults`) or requires
interactive input instead of migrating pinned versions — pass the file
for the canonical migration path.

Do not pass `--quiet`: the post-update banner is suppressed in quiet
mode, and you will miss conflict and follow-up notices.

Copier update is a three-way merge, not an overwrite: it re-renders the
old template at your recorded `_commit` and the new one, then merges the
template's evolution against yours. Conflict markers surface only where
both sides changed the same region. Verify `_commit` names the intended
tag afterwards — Copier records it by tag-name comparison, so check the
line rather than assuming it.

## Principles

1. **Accept structure and baselines from the template; preserve
   project-specific content.** The template owns hooks configuration,
   workflows, validators, classifiers, matrices, and the Python
   baseline; the project owns entry points, metadata, extras, data
   remapping, README customizations, and local exclusions. On conflict,
   project-owned files win: keep your customizations and take the
   template's structure around them.
2. **Conflicts are normal and visible.** `copier update` performs a 3-way
   merge. Ordinary overlapping changes surface as inline conflict
   markers, never silent overwrites — except `_skip_if_exists` paths,
   which are preserved as-is. Resolve every marker before committing;
   the `check-merge-conflict` hook is a backstop, not the plan.
3. **Keep the template-owned core.** After reconciling per Principle 1,
   the consumer should converge on: the pre-commit hook configuration,
   CI workflows, the validators wired into `linters`, the recorded
   answers file, and the towncrier fragment setup. Resolve conflicts
   keeping both sides where both apply — never strip one side.
4. **Never hand-edit the answers file.** It is overwritten by Copier.
   Drive answers with `--data-file` on update plus `--skip-answered`,
   and copy from the remote template source
   (`gh:emcd/python-project-common`), tracking latest unless a pinned
   `--vcs-ref` was explicitly requested.
5. **Reinstall hooks after updating.** Updates never reinstall Git
   hooks (hooks live in `.git`, not the tree). Run `pre-commit install
   --config .auxiliary/configuration/pre-commit.yaml` so any new hook
   types land — with a system-wide `pre-commit` installed via
   `uv tool install pre-commit`, independent of any Hatch environment.
6. **Python baseline is set by the template, not chosen per project.**
   The questionnaire enforces `>= 3.12`; the floor moves only with a
   template release, and the baseline data file carries it across.

## First Copy Checklist

- Clean work branch, clean tree.
- Saved answers file; remote template source.
- Run the copy; review the full diff file by file.
- Restore project-owned files; keep template-owned additions.
- Install hooks (see Principle 5).
- Run linters and the test suite; commit with the template ref recorded
  in the message.

## Update Checklist

- Clean tree; commit or stash first so the pre-update state is
  restorable (see Rollback). Note the template ref being updated from
  and to.
- Run `copier update`; resolve all conflict markers.
- Re-run `pre-commit install --config .auxiliary/configuration/pre-commit.yaml` so any new hook types land.
- Re-verify hooks and tests; commit.

Copier may propose deletions of retired template files (project
documentation layouts the template no longer ships, superseded
validators). Review each proposed deletion: accept template
retirements, keep project-owned content. If a hook fails on duplicate
keys after an update, treat it as a stale copy of a moved or
reformatted key until proven otherwise — delete the stale copy so the
file matches a fresh template render. If instead a hook fails on valid
new syntax (for example `check-ast` reporting `SyntaxError` on a `type`
statement the baseline supports), suspect a stale hook environment, not
the code: pre-commit caches per-hook interpreters, and an old cache can
parse with an interpreter older than the baseline. Refresh with
`pre-commit clean` and re-run; do not pin `language_version` to an
interpreter dev machines lack.

## Rollback

This procedure undoes an *uncommitted* update only — the tree must still
contain no update commit after your pre-update checkpoint commit. (For
an already-committed update, revert with a new history-preserving
commit — `git revert` the update commit — instead; do not rewrite
history.)

An update can leave three kinds of changes, and each needs its own
handling — a single restore command does not cover all of them:

1. Commit (or stash) before updating, so the checkpoint exists. The
   update itself must run on a clean tree.
2. Inventory the damage with `git status`: expect modified tracked
   files, possibly staged changes, and new untracked files the update
   generated.
3. Unstage everything without touching the worktree:
   `git reset` (leaves working-tree changes in place).
4. Restore modified tracked files, including the answers file:
   `git checkout -- .` (equivalently
   `git restore --source <pre-update-ref> -- .`). Verify the recorded
   answers match the checkpoint
   (`git diff <pre-update-ref> -- <answers-file>` shows nothing).
5. Remove ONLY update-generated untracked files, each reviewed by path
   (`rm <reviewed-path>...`). Never run a broad clean here:
   pre-existing ignored or untracked user work (notes, scratch, local
   configs) must survive. When in doubt whether a file is
   update-generated, check it against the pre-update commit.
6. Re-validate hooks and tests before recommitting.

Do NOT attempt to roll back across a baseline bump by feeding the old
values back in — validators in the new template reject retired answers
(a `python_version_min` below 3.12, or a minimum absent from the
supported versions, fails validation naming the minimum), because the
migration is one-way by design.
