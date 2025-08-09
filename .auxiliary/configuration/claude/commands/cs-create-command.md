---
allowed-tools: Write, Read, LS
description: Generate a new custom slash command with consistent structure and formatting
---

# Generate Slash Command

Generate a new custom slash command following established patterns for structure, tone, and formatting.

Target: $ARGUMENTS

**IMPORTANT**: You are creating slash commands for other Claude instances to execute. They will have no knowledge of:
- The concept of "arguments" being passed to slash commands
- The ARGUMENTS variable or its expansion
- The meta-context of slash command generation
- When creating content, avoid using the word "command" in titles or explanations - use terms like "process", "workflow", or "task" instead

Your job is to interpret the user's request and create a complete, self-contained slash command.

## Input Interpretation

The user's request may take various forms:
- Simple: `cs-analyze-performance`
- Descriptive: `Named cs-inquire.md with a process outlined in .auxiliary/notes/inquire-command.md`
- Reference-based: `Based on .auxiliary/notes/summarize-project-command.md`
- Complex: `cs-update-deps that checks package.json and updates dependencies safely`

Extract from the user's input:
1. **Filename** (must start with `cs-`)
2. **Purpose/functionality** (from description or referenced files)
3. **Special requirements** (referenced processes, specific tools needed)

## Context

- Current custom commands: !`ls .claude/commands/cs-*.md 2>/dev/null || echo "No cs-* commands found"`
- Referenced files (if any): Check for existence and read as needed
- Command template: @.auxiliary/configuration/claude/miscellany/command-template.md

## Prerequisites

Before creating the slash command, ensure:
- Clear understanding of the intended purpose
- Filename follows `cs-*` naming pattern
- No existing file with the same name
- Any referenced process files are accessible

## Generation Process

### 1. Analyze User Request

From the user's input, determine:
- **Filename** (extract `cs-*.md` name)
- **Purpose** (what should the generated slash command accomplish)
- **Required tools** (based on functionality)
- **Process details** (read any referenced files for specifics)

### 2. Read Template Structure

Read the template to get the base structure, then customize:
- Replace placeholder content with appropriate descriptions
- Customize sections based on purpose
- Select appropriate allowed-tools
- Add relevant @-references if applicable
- Add checklists to sections if applicable

### 3. Apply Formatting Standards

**Professional Tone:**
- Avoid making everything critical or important; no excessive
  attention-grabbing
- Avoid excessive emphasis (no all-caps headers, minimal bold text)
- Professional headers: `## Prerequisites` not `## MANDATORY PREREQUISITES`
- Use "Stop and consult" for when user input should be solicited

**Structure:**
- Include Prerequisites section early in document
- Include Context section with command expansions (exclamation point followed
  by command in backticks) for dynamic info when needed
- Use @-references for local documentation when applicable
- Provide clear Process Summary before detailed steps
- Include Safety Requirements section for error handling

### 4. Tool Selection

Choose appropriate allowed-tools based on functionality:

**Common tool combinations:**
- **File operations**: `Write, Read, Edit, MultiEdit, LS, Glob, Grep`
- **Git operations**: `Bash(git status), Bash(git add:*), Bash(git commit:*), Bash(git push:*)`
- **Python development**: `Bash(hatch --env develop run:*), Bash(pytest:*), Bash(ruff:*)`
- **GitHub operations**: `Bash(gh run list:*), Bash(gh run watch:*), Bash(gh pr create:*)`

### 5. Generate and Write File

1. **Read the template** from `.auxiliary/configuration/claude/miscellany/command-template.md`
2. **Customize all sections** based on the specific purpose
3. **Replace placeholders** with appropriate content for the target functionality
4. **Write the final file** to `.claude/commands/[filename].md`


### 6. Validation and Summary

After generation:
- Verify file structure matches established patterns
- Check that allowed-tools are appropriate for the functionality
- Ensure professional tone throughout (no excessive attention-grabbing, etc...)
- Confirm all required sections are present and customized
- Provide succinct summary of changes made to the user
