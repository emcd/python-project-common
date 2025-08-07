# CLAUDE.md Reorganization Plan

## Current Problem
CLAUDE.md is generated from a template with cookie-cutter conventions instead of serving its intended purpose as project-specific memory. General practices now live in `.auxiliary/instructions/` for slash commands and subagents.

## Proposed Structure

1. **Project Overview** 
   - Generate from Copier template answers file (description, etc.)
   - Brief description of project purpose and key components

2. **Context**
   - Preserve existing guidance about README files and session notes
   - Reference (not @-include) README, PRD, `.auxiliary/instructions` 
   - Add @-reference to `.auxiliary/notes` directory for current TODOs
   - Add @-reference to `documentation/architecture` to show available docs
   - Mention context7 MCP server availability

3. **Operation**
   - Keep existing MCP tool guidance (rg coordinates, text-editor preferences, etc.)
   - Keep path preferences and scratch space guidance

4. **Commits** 
   - Preserve existing commit practices and code-conformer usage

5. **Project Notes** (unstructured, last section)
   - Accumulates project-specific lore via `#` command
   - Project-specific constraints and deviations
   - Natural organization, consolidate as needed
   - Relies on `documentation/architecture/decisions` and `.auxiliary/notes/todo.md` for structured items

## Benefits
- CLAUDE.md serves its intended purpose as project memory
- General conventions accessible via slash commands/subagents  
- Projects can customize without template constraints
- Clear separation of concerns between general practices and project specifics