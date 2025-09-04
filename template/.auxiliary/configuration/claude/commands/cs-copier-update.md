---
allowed-tools: Read, Write, Edit, MultiEdit, LS, Glob, Grep, Bash(copier:*), Bash(git status), Bash(git add:*), Bash(git rm:*), Bash(rg:*), Bash(grep:*), Bash(hatch --env develop run make-all), TodoWrite
description: Synchronize project with Copier template updates, intelligently resolving merge conflicts
---

# Template Synchronization

Synchronize project with its Copier template by running updates and automatically resolving common merge conflict patterns while preserving local customizations.

Request from user: $ARGUMENTS

## Context

- Template answers file: @.auxiliary/configuration/copier-answers.yaml
- Current git status: !`git status --porcelain`
- Existing conflicts check: !`grep -r "^<<<<<<<\|^=======$\|^>>>>>>>" . --exclude-dir=.git || echo "No conflicts"`
- Project conventions: @.auxiliary/configuration/conventions.md

## Prerequisites

Before running template synchronization, ensure:
- Working directory is completely clean (no staged or unstaged changes)
- Copier is installed and accessible via command line
- Template answers file exists at `.auxiliary/configuration/copier-answers.yaml`
- Git repository is in a stable state for applying updates

## Process Summary

Key functional areas:
1. **Template Update**: Run copier update with project-specific settings
2. **Conflict Detection**: Identify and categorize merge conflicts from template changes
3. **Intelligent Resolution**: Automatically resolve conflicts favoring upstream improvements while preserving local customizations
4. **File Lifecycle Management**: Handle additions, renames, and deletions from template updates
5. **Validation**: Ensure complete conflict resolution and commit changes with template version

## Safety Requirements

Stop and consult the user if:
- Working directory is not clean (has staged or unstaged changes)
- Complex conflicts exist that could result in loss of local customizations
- Template artifacts cannot be reliably distinguished from intentional local content
- Multiple conflicting resolution strategies are equally valid
- Copier update fails with unrecoverable errors
- Critical project files show unexpected merge conflicts

## Execution

Execute the following steps:

### 1. Pre-Update Validation
Check project state and prepare for template synchronization:
- Verify git working directory is completely clean (halt if any changes exist)
- Confirm template answers file exists and is readable
- Document any existing conflicts to avoid confusion
- Ensure repository is on the expected branch

### 2. Execute Template Update
Run copier update with project-specific configuration:
```bash
copier update --answers-file .auxiliary/configuration/copier-answers.yaml --skip-answered
```
- Capture copier output to extract template version information
- Detect update completion status and any reported conflicts
- Identify new, modified, and deleted files from the update

### 3. Conflict Analysis and Categorization
Systematically identify and categorize all conflicts:
- Scan for merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- Classify conflicts by type:
  - **Structure consolidation**: Old sections moved into organized subsections
  - **Upstream additions**: New template content (toctree entries, sections, files)
  - **Language refinements**: Policy and wording improvements
  - **Template artifacts**: TODO comments, placeholder content
  - **Complex conflicts**: Overlapping local and upstream modifications

### 4. Intelligent Conflict Resolution
Apply resolution strategies based on conflict categorization:

**Auto-resolve structure consolidation conflicts:**
- Accept new organization when local content is preserved in new structure
- Remove orphaned sections that were properly consolidated

**Auto-resolve upstream additions:**
- Accept new toctree entries, sections, and configuration additions
- Stage new files and directories from template

**Auto-resolve language refinements:**
- Accept upstream wording and policy improvements
- Preserve local semantic modifications when they don't conflict

**Handle template artifacts intelligently:**
- Detect TODO comments and placeholder content that may have been intentionally removed
- Avoid reintroducing template boilerplate that conflicts with project maturity

### 5. File Lifecycle Management
Handle template-driven file changes:
- Stage all new files and directories added by template
- Process file renames (e.g., `cs-develop-tests.md` → `cs-develop-pytests.md`)
- Remove obsolete files that have been replaced or are no longer needed
- Update git index to reflect all template changes

### 6. Resolution Verification
Ensure complete and accurate conflict resolution:
- Scan entire project for remaining merge conflict markers
- Verify no orphaned conflict sections remain
- Confirm all auto-resolved conflicts maintain local customizations
- Validate file integrity and proper git staging

### 7. Project Validation
Verify template changes don't break project functionality:
```bash
hatch --env develop run make-all
```
- Run full project validation including linting, type checking, and tests
- Ensure all quality gates pass after template synchronization
- Address any validation failures before proceeding to commit

### 8. Commit Template Changes
Create commit with template version information:
- Extract template version from copier output or updated answers file
- Generate commit message: "Update project from Copier template (v{version})."
- Include standard co-authoring footer for Claude Code
- Use git commit (requires user approval) to commit all staged changes

### 9. Conflict Resolution Report
Provide comprehensive summary of synchronization results:
- List all conflicts automatically resolved with resolution strategy
- Report new files, renames, and deletions processed
- Identify any conflicts requiring manual intervention
- Confirm template version successfully applied
- Note any remaining tasks or follow-up actions needed