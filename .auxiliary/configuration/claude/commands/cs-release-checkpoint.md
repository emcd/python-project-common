---
allowed-tools: Bash(git status), Bash(git pull:*), Bash(git add:*), Bash(git commit:*), Bash(git tag:*), Bash(git push:*), Bash(gh run list:*), Bash(gh run watch:*), Bash(hatch version:*), Bash(hatch --env develop run:*), Bash(echo:*), Bash(ls:*), Bash(grep:*), Bash(date:*), LS, Read
description: Execute automated alpha checkpoint release with QA monitoring
argument-hint: "[alpha]"
---

# Release Checkpoint

**NOTE: This is an experimental workflow! If anything seems unclear or missing,
please stop for consultation with the user.**

For execution of an automated alpha checkpoint release on master branch.

Below is a validated process to create an alpha checkpoint release with automated
monitoring and version increment.

Target alpha increment: $ARGUMENTS
(optional - defaults to next alpha)

Verify current version is alpha format if no arguments provided.

Stop and consult if:
- Working directory has uncommitted changes
- Current version is not an alpha version (e.g., 1.3.0, 1.3rc1) and no target specified
- Git operations fail or produce unexpected output

## Context

- Current git status: !`git status`
- Current branch: !`git branch --show-current`
- Current version: !`hatch version`
- Recent commits: !`git log --oneline -10`

## Prerequisites

Before starting, ensure:
- GitHub CLI (`gh`) is installed and authenticated
- Working directory is clean with no uncommitted changes
- Currently on master branch
- Current version is an alpha version (e.g., 1.3a0)

## Process Summary

Key functional areas of the process:

1. **Pre-Release Quality Check**: Run local QA to catch issues early
2. **Changelog Generation**: Run Towncrier to build changelog
3. **QA Monitoring**: Push commits and monitor QA workflow with GitHub CLI
4. **Tag Release**: Create alpha tag with current version after QA passes
5. **Release Monitoring**: Monitor release workflow deployment
6. **Post-Release Cleanup**: Remove news fragments and bump alpha version

## Safety Requirements

Stop and consult the user if any of the following occur:

- **Step failures**: If any command fails, git operation errors, or tests fail
- **Workflow failures**: If QA or release workflows show failed jobs
- **Unexpected output**: If commands produce unclear or concerning results
- **Version conflicts**: If version bumps don't match expected patterns
- **Network issues**: If GitHub operations timeout or fail repeatedly

**Your responsibilities**:
- Validate each step succeeds before proceeding to the next
- Monitor workflow status and halt on any failures
- Provide clear progress updates throughout the process
- Maintain clean git hygiene
- Use your judgment to assess when manual intervention is needed

## Release Process

Execute the following steps:

### 1. Pre-Release Quality Check
Run local quality assurance to catch issues early:
```bash
git status && git pull origin master
hatch --env develop run linters
hatch --env develop run testers
hatch --env develop run docsgen
```

### 2. Changelog Generation
Run Towncrier to update changelog with current version:
```bash
hatch --env develop run towncrier build --keep --version $(hatch version)
git commit -am "Update changelog for v$(hatch version) release."
```

### 3. Quality Assurance Phase
Push commits and monitor QA workflow:
```bash
git push origin master
```

Workflow monitoring requirements:
After pushing, you MUST ensure you monitor the correct QA workflow run:

1. **Wait for workflow trigger**: Wait 10 seconds after pushing to allow GitHub to trigger the workflow
2. **Verify correct workflow**: Use `gh run list --workflow=qa --limit=5` to list recent runs
3. **Check timestamps**: Compare the workflow creation time with your push time using `date --utc`
4. **Ensure fresh run**: Only monitor a workflow run that was created AFTER your push timestamp
5. **If no new run appears**: Wait additional time and check again - do NOT assume an old completed run is your workflow

Once you've identified the correct QA run ID:
```bash
gh run watch <correct-qa-run-id> --interval 30 --compact
```

Do not proceed until workflow completes:
- Monitor QA workflow with `gh run watch` using the correct run ID
- Use `timeout: 300000` (5 minutes) parameter in Bash tool for monitoring commands
- If command times out, immediately rerun `gh run watch` until completion
- Only proceed to next step after seeing "✓ [workflow-name] completed with 'success'"
- Stop if any jobs fail - consult user before proceeding

### 4. Alpha Release Deployment
**Verify QA passed before proceeding to alpha tag:**
```bash
git tag -m "Alpha checkpoint v$(hatch version)." v$(hatch version)
git push --tags
```

Release workflow monitoring requirements:
After pushing the tag, you MUST ensure you monitor the correct release workflow run:

1. **Wait for workflow trigger**: Wait 10 seconds after pushing tags to allow GitHub to trigger the release workflow
2. **Verify correct workflow**: Use `gh run list --workflow=release --limit=5` to list recent runs
3. **Check timestamps**: Compare the workflow creation time with your tag push time using `date --utc`
4. **Ensure fresh run**: Only monitor a workflow run that was created AFTER your tag push timestamp
5. **If no new run appears**: Wait additional time and check again - do NOT assume an old completed run is your workflow

Once you've identified the correct release run ID:
```bash
gh run watch <correct-release-run-id> --interval 30 --compact
```

Do not proceed until workflow completes:
- Monitor release workflow with `gh run watch` using the correct run ID
- Use `timeout: 600000` (10 minutes) parameter in Bash tool for monitoring commands
- If command times out, immediately rerun `gh run watch` until completion
- Only proceed to next step after seeing "✓ [workflow-name] completed with 'success'"
- Stop if any jobs fail - consult user before proceeding

### 5. Post-Release Cleanup
Clean up Towncrier fragments:
```bash
git rm .auxiliary/data/towncrier/*.rst
git commit -m "Clean up news fragments."
```

### 6. Next Alpha Version
Bump to next alpha version:
```bash
hatch version alpha
git commit -am "Version: $(hatch version)"
```

### 7. Final Push
Push cleanup and version bump commits:
```bash
git push origin master
```
