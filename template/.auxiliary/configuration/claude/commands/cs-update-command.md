---
allowed-tools: Read, Write, Edit, MultiEdit, LS, Glob, Grep
description: Update existing slash command with missing instructions or reinforced guidance
---

# Update Slash Process

Update an existing custom slash command to address missing instructions,
reinforce guidance which LLMs are ignoring, add missing tool permissions, or
make structural improvements.

Target command and instructions: $ARGUMENTS

Stop and consult if:
- The target file doesn't exist or isn't a slash command
- Major structural changes are requested that would fundamentally alter the command purpose
- Changes conflict with established project patterns

## Context

- Command template: @.auxiliary/configuration/claude/miscellany/command-template.md
- Project conventions: @.auxiliary/configuration/conventions.md

## Prerequisites

Before updating the command, ensure:
- Clear understanding of what improvements are needed
- Target file exists and is accessible
- Any referenced files or patterns are available
- Changes align with project conventions and existing process patterns

## Process Summary

Key functional areas:
1. **Analysis**: Read current command and identify improvement areas
2. **Content Updates**: Add missing instructions or reinforce existing guidance
3. **Structure Review**: Consider organizational improvements when appropriate
4. **Tone Refinement**: Ensure professional language without excessive emphasis
5. **Validation**: Verify updates maintain command effectiveness

## Safety Requirements

Stop and consult the user if:
- Process changes would break existing workflows or dependencies
- Updates conflict with established project conventions
- Structural modifications require significant rework of command logic

## Execution

Execute the following steps:

### 1. Command Analysis
Read and analyze the current command:
- Review existing content, structure, and tool permissions
- Identify areas needing improvement or reinforcement
- Assess tone and language for professional standards
- Note any missing instructions or unclear guidance

### 2. Content Enhancement
Apply requested improvements:
- Add missing instructions where gaps are identified
- Reinforce guidance that needs stronger emphasis
- Remove excessive bold formatting or shouty language
- Eliminate redundant repetition within sections
- Ensure clear, actionable language throughout

### 3. Structural Review
Consider organizational improvements:
- Evaluate section ordering and logical flow
- Improve prerequisites or context sections if needed
- Enhance command summary for clarity
- Adjust safety requirements as appropriate
- Ensure consistent formatting patterns

### 4. Tool and Permission Updates
Review and adjust technical aspects:
- Verify allowed-tools are appropriate for updated functionality
- Check that `@`-references and shell command expansions are current
- Ensure any context commands have proper tool permissions to run (e.g., `Bash(ls:*)` for `ls` commands)
- Ensure context section provides relevant dynamic information
- Validate that command can execute with given permissions

### 5. Professional Polish
Apply formatting and tone standards:
- Use professional headers without excessive emphasis
- Maintain clear, direct language without redundancy
- Ensure consistency with project conventions
- Remove any attention-grabbing formatting that isn't necessary
- Balance guidance strength with readability

### 6. Validation and Summary
Complete the update command:
- Review updated content for completeness and clarity
- Verify all requested improvements have been addressed
- Ensure command maintains effectiveness while addressing issues
- Provide succinct summary of changes made to the user
