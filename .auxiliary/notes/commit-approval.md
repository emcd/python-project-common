# Commit Approval Mechanism

## Problem

Despite having "Do **not** commit without explicit user approval" in conventions, Claude Code agents sometimes lose track of this instruction and commit without asking. The recent addition of explicit review language ("Do the changes that I am about to commit look good to you?") may help, but we need a backup enforcement mechanism.

## Proposed Solution

Implement a two-part system similar to the existing `pre-bash-python-check` hook:

### 1. User Approval Command

Create `git approve-staged` (or similar) that:
- Captures a hash of currently staged changes
- Creates `.git/COMMIT_APPROVED` sentinel file with the hash
- Allows user to explicitly approve the current staged changeset

Implementation options:
- Git alias in project `.gitconfig`
- Custom script in `.auxiliary/scripts/`
- Shell function users add to their environment

### 2. PreToolUse Hook

Create `.auxiliary/scripts/claude/pre-git-commit-check` that:
- Intercepts any `git commit` commands from Claude
- Checks for valid `.git/COMMIT_APPROVED` file
- Validates that staged changes hash matches approval hash
- Blocks commit if approval missing or stale
- Provides helpful error message directing Claude to request approval

### Workflow

1. User stages changes with `git add`
2. User reviews changes with `git status` and `git diff --cached`
3. User approves with `git approve-staged`
4. Claude can now commit (or user can commit directly)
5. Any new staging invalidates the approval

### Benefits

- **Explicit approval**: User must take deliberate action to approve changes
- **Change integrity**: Approval becomes invalid if staged content changes
- **Familiar pattern**: Follows existing hook architecture
- **Fail-safe**: Blocks commits even if Claude ignores conventions
- **Flexible**: Works for both Claude and direct user commits

### Edge Cases to Handle

- Multiple commit attempts with same approval
- Partial staging after approval
- Hook failures and error handling
- Cleanup of stale approval files
- Integration with existing Git workflows

### Alternative Mechanisms Considered

- **Git pre-commit hook**: Would work but PreToolUse gives better error messages to Claude
- **Git aliases replacing commit**: Could be confusing for users
- **Interactive prompts**: Don't work well in Claude Code environment
- **Existing solutions**: Custom approach gives full control and clean integration

## Next Steps

1. Implement basic `git approve-staged` command
2. Create PreToolUse hook for git commit blocking
3. Test with various staging/approval scenarios
4. Document usage in project conventions
5. Consider integration with specialized commands that use commits

## Notes

- This enforces the "equal partner" philosophy - user explicitly approves rather than Claude asking permission
- Maintains token efficiency by not showing diffs in Claude interactions
- Provides safety net for complex multi-file changes where context might be lost