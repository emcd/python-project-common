# Claude GitHub Actions Enhancement Plan

## Overview

Upgrade Claude GitHub Actions workflow from beta to v1 and add MCP server integration to provide enhanced capabilities for workflow Claude instances.

## Goals

1. Upgrade Claude Code action from beta to v1
2. Add manual workflow triggers for testing
3. Integrate context7 and librovore MCP servers
4. Make coding standards available via instruction downloads
5. Enable same tooling availability as local Claude Code sessions

## MCP Server Strategy

### Selected Servers
- **context7**: Documentation and SDK reference via `npx -y @upstash/context7-mcp`
- **librovore**: Structured documentation search via `uvx librovore serve`

### Dependencies
- Node.js setup for npx (using `setup-node` action)
- UV installation for uvx (`pip install uv`)

### Rationale
- Focuses on high-value documentation servers
- Avoids complex Go-based language server installations
- Leverages standard GitHub Actions ecosystem

## Implementation Plan

### Step 1: Beta to V1 Upgrade
- Update `.github/workflows/xrepo--claude.yaml:53`
- Change `anthropics/claude-code-action@beta` to `anthropics/claude-code-action@v1`
- **CORRECTION**: Parameter changes required for v1:
  - `allowed_tools` → `claude_args: --allowedTools "${{ inputs.allowed-tools }}"`
  - `timeout_minutes` → `claude_args: --timeout ${{ inputs.timeout-minutes }}`
- Commit changes

### Step 2: Add Manual Triggers
- Add `workflow_dispatch` trigger to workflow
- Commit changes
- Push master branch

### Step 3: Testing Strategy (Revised)
- Test directly on `master` branch due to GitHub Actions security constraints
- Temporarily modify `.github/workflows/claude.yaml` to point to xrepo workflow `@master`
- GitHub Actions validates workflow files must be identical to default branch, preventing branch isolation
- Will revert to `@gha-1` after successful testing and tag update

### Step 4: MCP Integration
Add to xrepo workflow:
```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '18'

- name: Install UV
  run: pip install uv

- name: Create MCP Configuration
  run: |
    cat > .mcp.json << 'EOF'
    {
      "mcpServers": {
        "context7": {
          "command": "npx",
          "args": ["-y", "@upstash/context7-mcp"]
        },
        "librovore": {
          "command": "uvx",
          "args": ["librovore", "serve"]
        }
      }
    }
    EOF
    echo "::notice::Created custom MCP configuration with context7 and librovore"

- name: Download Instructions (already handled by configure-clone.bash pattern)
```

### Step 5: Testing
- Test via workflow_dispatch or issue creation with `/claude` trigger
- Ask workflow Claude: "Can you see what MCP servers are available to you?"
- Validate context7 and librovore accessibility
- Test subagent availability

### Step 6: Production Integration
- Revert temporary workflow pointer
- Merge to master
- Create new `gha-1.*` tag
- Force-retarget `gha-1` floating tag with preserved message

## Progress Status

### Completed ✅
1. **Claude Code action v1 upgrade** - Fixed parameter conversion to `claude_args`
2. **Manual workflow triggers** - `workflow_dispatch` with prompt parameter working
3. **Parameter plumbing** - Prompt flows from dispatch to cross-repo workflow  
4. **Basic workflow functionality** - All setup steps and Claude execution working

### Current Phase: MCP Server Integration 🔄

#### Step 4A: Add MCP Configuration Generation
- Add Node.js setup step for context7 
- Add UV installation step for librovore
- Create custom `.mcp.json` with context7 and librovore servers
- Position before "Execute Claude Code" step

#### Step 4B: Add Instructions Download
- Add step to download/stage instructions to `.auxiliary/instructions`
- Ensure instructions are available before Claude execution
- Follow existing pattern from configure-clone.bash

#### Step 4C: Test MCP Integration
- Test via workflow_dispatch with MCP validation prompt
- Verify Claude can see context7 and librovore MCP servers
- Verify subagent availability (depends on instructions)

### Remaining: Production Integration 📋
1. Update `gha-1` tag with complete working configuration
2. Revert claude.yaml to point back to `@gha-1` 
3. Final validation and documentation update

## Risk Mitigation

- Branch isolation prevents production impact
- Incremental testing validates each component
- Easy rollback via workflow pointer reversion
- Timeout increases if needed (current: 20 minutes)

## Dependencies Status

- GitHub Actions workers: Node.js pre-installed ✅
- Python/pip: Pre-installed ✅  
- UV package: Needs installation
- Context7 MCP: Available via npx
- Librovore: Available via uvx

## Notes

- MCP servers auto-start via Claude Code action
- Instructions download timing flexible (before Claude action execution)
- Validation via direct query to workflow Claude instance
- Maintains existing workflow security and permissions model