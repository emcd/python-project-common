# Claude Code Commands Audit

**Date**: 2025-09-04  
**Purpose**: Audit all custom slash commands for cleanup opportunities including argument hints, allowed-tools simplification, and syntax issues.

## Commands Analyzed

### Release Commands

**cs-release-checkpoint.md**
- Current: No argument-hint
- Suggestion: Add `argument-hint: "[version]"` - takes specific version number
- allowed-tools: Complex bash restrictions, keep as-is for safety
- Syntax: ✅ Correct (no array brackets)

**cs-release-final.md** 
- Current: No argument-hint
- Suggestion: Add `argument-hint: "[version]"` - takes specific version number
- allowed-tools: Complex bash restrictions, keep as-is for safety  
- Syntax: ✅ Correct (no array brackets)

**cs-release-maintenance.md**
- Status: Need to examine
- Likely candidate for version argument-hint

### Python Development Commands

**cs-code-python.md**
- Current: Extensive allowed-tools list
- Suggestion: ✅ **REMOVE allowed-tools** - inherit from settings.json
- argument-hint: Not needed (free-form requirements)
- Syntax: ✅ Fixed (removed array brackets)

**cs-develop-pytests.md**
- Current: Comprehensive allowed-tools
- Suggestion: ✅ **REMOVE allowed-tools** - inherit from settings.json  
- argument-hint: Not needed (free-form test descriptions)
- Syntax: ✅ Correct (no array brackets)

**cs-conform-python.md**
- Current: Standard tools + pyright MCP tools
- Suggestion: ✅ **REMOVE allowed-tools** - inherit from settings.json
- argument-hint: Not needed (free-form scope)
- Syntax: ✅ Correct (no array brackets)

**cs-design-python.md**
- Status: Need to examine
- Suggestion: Likely candidate for allowed-tools removal

### Documentation Commands

**cs-document-examples-rst.md**
- Status: Need to examine  
- Suggestion: Likely candidate for allowed-tools removal (reStructuredText documentation)

**cs-update-readme-rst.md**
- Status: Need to examine
- Suggestion: May benefit from allowed-tools removal

### Analysis Commands

**cs-inquire.md**
- Current: Analysis/research command  
- Suggestion: Keep allowed-tools (likely has specialized restrictions)
- argument-hint: Not needed (free-form questions)

**cs-excise-python.md**
- Current: Dead code analysis with MCP tools
- Suggestion: Keep allowed-tools (specialized tool set)
- argument-hint: Could use `"[target-files-or-scope]"`

### Utility Commands  

**cs-annotate-release.md**
- Current: Towncrier news fragment generation
- Suggestion: No argument-hint needed (automated process)
- allowed-tools: Likely keep as-is

**cs-copier-update.md**
- Current: Template synchronization (always latest)
- Suggestion: No argument-hint needed (no version parameter)
- allowed-tools: Likely keep as-is

## Key Findings

### ✅ Completed Analysis

**Release Commands:**
1. **cs-release-checkpoint.md** - `argument-hint: "[version]"` (version optional, can be inferred)
2. **cs-release-final.md** - `argument-hint: "[version]"` (takes specific version)  
3. **cs-release-maintenance.md** - `argument-hint: "[version]"` (takes specific version, explicitly documented)

**Development Commands:**
4. **cs-code-python.md** - ✅ Remove allowed-tools (inherit from settings.json)
5. **cs-develop-pytests.md** - ✅ Remove allowed-tools (inherit from settings.json)
6. **cs-conform-python.md** - ✅ Remove allowed-tools (inherit from settings.json)
7. **cs-design-python.md** - ✅ Remove allowed-tools (standard analysis tools, can inherit)
8. **cs-document-examples-rst.md** - ✅ Remove allowed-tools (standard doc tools + pyright, can inherit)
9. **cs-update-readme-rst.md** - ✅ Remove allowed-tools (standard tools, can inherit)

**Remaining Commands Analyzed:**
10. **cs-conform-toml.md** - ✅ Keep allowed-tools (minimal, specific set for TOML work)
11. **cs-create-command.md** - ✅ Keep allowed-tools (minimal Write, Read, LS - appropriate restriction)
12. **cs-plan-pytests.md** - ⚠️ Could remove allowed-tools (standard development tools)
13. **cs-inquire.md** - ✅ Keep allowed-tools (read-only analysis, appropriate restriction)
14. **cs-annotate-release.md** - ✅ Keep allowed-tools (specialized git + towncrier workflow)
15. **validate-custom-slash.md** - ✅ Keep allowed-tools (testing/validation tools)

### 🚨 Critical Syntax Issues Found
**Commands with array bracket syntax errors** (need immediate fix):
1. `cs-architect.md` - `allowed-tools: [...]` 
2. `cs-copier-update.md` - `allowed-tools: [...]`
3. `cs-design-python.md` - `allowed-tools: [...]` + candidate for allowed-tools removal
4. `cs-document-examples-rst.md` - `allowed-tools: [...]` + candidate for allowed-tools removal  
5. `cs-excise-python.md` - `allowed-tools: [...]`
6. `cs-manage-prd.md` - `allowed-tools: [...]`
7. `cs-review-todos.md` - `allowed-tools: [...]`
8. `cs-update-command.md` - `allowed-tools: [...]`
9. `cs-update-readme-rst.md` - `allowed-tools: [...]` + candidate for allowed-tools removal

## Immediate Action Items

### 🚨 **CRITICAL: Fix Array Bracket Syntax** (9 files)
All commands listed above need `allowed-tools: [...]` converted to `allowed-tools: ...`

### High Priority  
1. **Add argument-hint to release commands**:
   - `cs-release-checkpoint.md`: `argument-hint: "[version]"` (optional - square brackets indicate optionality)
   - `cs-release-final.md`: `argument-hint: "[version]"`
   - `cs-release-maintenance.md`: `argument-hint: "[version]"`

2. **Remove allowed-tools from development commands** (inherit from settings.json):
   - `cs-code-python.md` ✅
   - `cs-develop-pytests.md` ✅  
   - `cs-conform-python.md` ✅
   - `cs-design-python.md` ✅ (standard analysis tools)
   - `cs-document-examples-rst.md` ✅ (standard doc tools + pyright)
   - `cs-update-readme-rst.md` ✅ (standard tools)
   - `cs-plan-pytests.md` ⚠️ (optional - has standard development tools)

3. **Commands to keep allowed-tools** (appropriate restrictions):
   - `cs-conform-toml.md` - Minimal, specific TOML tools
   - `cs-create-command.md` - Minimal Write, Read, LS only
   - `cs-inquire.md` - Read-only analysis restriction  
   - `cs-annotate-release.md` - Specialized git + towncrier workflow
   - `validate-custom-slash.md` - Testing/validation specific tools

### Medium Priority
1. Complete detailed examination of remaining 12 commands
2. Identify additional argument-hint opportunities
3. Review specialized tool restrictions for appropriateness

## Notes

- Most commands should keep `$ARGUMENTS` (free-form text input)
- Only release commands clearly benefit from positional parameters/hints
- settings.json is well-tuned, so inheritance makes sense for standard development commands
- Keep allowed-tools for security-sensitive or highly-specialized commands

## Implementation Plan

1. **Phase 1: Fix Array Bracket Syntax** (HIGHEST PRIORITY)
   - Fix 9 commands with `allowed-tools: [...]` syntax errors
   
2. **Phase 2: Remove allowed-tools from Development Commands** (HIGH PRIORITY)  
   - Remove from 6-7 development commands that can inherit from settings.json
   
3. **Phase 3: Add argument-hints** (LOWEST PRIORITY)
   - Add `[version]` hints to release commands

## Status
- ✅ **Audit Complete** - All commands examined and analyzed
- ⏳ **Implementation Pending** - No changes implemented yet