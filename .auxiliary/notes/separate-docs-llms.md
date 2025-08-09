# Separate Documentation and LLM Configuration Repository

## Motivation

### Current Problems

1. **Heavyweight Documentation Release Process**
   - Must create full stable releases of `python-project-common` for documentation updates
   - Templates reference published HTML documentation at `stable/` URLs
   - Small documentation changes require full project release cycle

2. **Publication Sync Issues**  
   - LLM instruction scraper uses `docs-1` tag (reST sources)
   - Templates reference `stable` HTML documentation 
   - These can get out of sync, causing inconsistencies

3. **Configuration Drift**
   - Template and main versions of LLM commands drift apart
   - Manual synchronization required between `.auxiliary/configuration/claude/commands/` files
   - Error-prone process leads to inconsistent command behavior

4. **Multi-Language Template Future**
   - Plan to create Rust Copier template alongside Python template
   - Need shared documentation and LLM configuration across language-specific templates
   - Don't want overlapping Copier templates generating same content

## Proposed Solution

### New Repository Architecture

Create separate repository (e.g., `emcddocs` or `llm-project-common`) containing:

**Shared Content:**
- `.auxiliary/instructions/` (architecture, practices, nomenclature guides)
- `.auxiliary/configuration/claude/commands/` (slash commands)
- `.auxiliary/configuration/claude/miscellany/` (templates, etc.)

**Repository Infrastructure:**
- Populated from Copier template for CLI framework, Sphinx, testing
- `emcddocs prepare-llm-agents` CLI command for environment setup
- Adapted website publishing workflow from existing `website.py`

### Publishing Workflow

**Lightweight Tag-Based Process:**
1. Update documentation or LLM commands in new repository
2. Tag release as `docs-1`, `docs-2`, etc.
3. GitHub workflow publishes documentation to versioned path: `/docs-1/`
4. No heavyweight release process - just tag and publish

**Reference Updates:**
- Update `python-project-common` templates to reference `/docs-1/` URLs directly
- `configure-clone.bash` pulls reST sources from same `docs-1` tag
- Single source of truth eliminates sync issues

### Configuration Separation

**New Repository (versioned, shared):**
- Documentation guides (`.auxiliary/instructions/`)
- LLM commands (`.auxiliary/configuration/claude/commands/`)
- Command templates and miscellany

**Copier Templates (project-specific):**
- `settings.json.jinja` (auto-allow permissions, hooks)
- `mcp-servers.json.jinja` (server configurations)  
- `conventions.md.jinja` (if containing project-specific context)

**Rationale:** MCP configurations are largely independent of LLM commands and change less frequently. Template generation handles conditional logic well.

### Distribution Mechanism

**Updated `configure-clone.bash`:**
- Download instructions from new repository's tagged releases
- Download LLM commands via same tag-based scraping
- Replace current Copier-based distribution of commands

**CLI Integration:**
- `emcddocs prepare-llm-agents` replaces repository configuration functionality
- Self-contained in new repository for version alignment
- Available via `uvx emcddocs@docs-1 prepare-llm-agents`

## Benefits

### Operational
- **Rapid LLM iteration:** Update commands/instructions without heavyweight releases
- **Eliminated drift:** Single source of truth for all LLM configuration
- **Simplified publication:** Lightweight tag-based process instead of full releases

### Architectural  
- **Multi-language ready:** Python and Rust templates share same LLM/docs repository
- **Clean separation:** Project structure (Copier) vs. evolving content (tag-based)
- **Single source of truth:** Both templates and LLM scrapers reference same versioned source

### Maintenance
- **Consistent commands:** No template/main version drift
- **Version alignment:** CLI tool version matches documentation version
- **Simplified workflow:** Tag, publish, pull - no complex coordination

## Implementation Plan

### Phase 1: New Repository Setup
1. Create new repository populated from Copier template
2. Move `.auxiliary/instructions/` and `.auxiliary/configuration/claude/commands/`
3. Implement `emcddocs prepare-llm-agents` CLI command
4. Adapt website publishing workflow for tag-based releases

### Phase 2: Update Distribution
1. Modify `configure-clone.bash` to pull from new repository
2. Update template references from `stable/` to `docs-1/` URLs
3. Test tag-based publishing and scraping workflow

### Phase 3: Migration and Cleanup
1. Remove LLM commands from `python-project-common` template
2. Update documentation to reference new workflow
3. Validate multi-project usage and prepare for Rust template

## Edge Cases and Considerations

**MCP Server Dependencies:**
- Commands may reference MCP servers expected by templates
- Current interdependency is minimal and stable (context7, pyright, ruff)
- Accept minor coordination cost rather than complex abstraction

**Backward Compatibility:**
- Existing projects continue using current `configure-clone.bash`
- Gradual migration as projects update LLM environments
- Tag versioning allows projects to pin to known-good configurations

**Publication Coordination:**
- If MCP servers are withdrawn, requires updates in both repositories
- Frequency is low enough that manual coordination is acceptable
- Alternative abstraction layers add more complexity than value