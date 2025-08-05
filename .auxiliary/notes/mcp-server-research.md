# MCP Server Research: Documentation-Focused Tools

Research conducted for extending template MCP capabilities with documentation analysis and structured data extraction tools.

## Context

- **Goal**: Enhance `template/.auxiliary/configuration/mcp-servers.json` for all generated projects
- **Focus**: Documentation analysis, structured data extraction, Sphinx/MkDocs support
- **Requirements**: Free, no API keys, template-friendly

## Verified MCP Servers

### 1. GitMCP ⭐⭐⭐⭐⭐ (Recommended)

**Repository**: https://github.com/idosal/git-mcp
**Website**: https://gitmcp.io/
**Status**: ✅ Verified and Active

**Key Features**:
- Zero setup required - no API keys, no local installation
- Cloud-hosted - users add `gitmcp.io/{owner}/{repo}` to config
- Documentation-first approach - prioritizes `llms.txt`, docs, README
- Intelligent search tools: `fetch_documentation`, `search_documentation`, `search_code`
- GitHub-specific (covers 99% of use cases)
- Reduces AI hallucinations with up-to-date context

**Template Integration**:
```json
{
  "mcpServers": {
    "project-docs": {
      "command": "mcp-server-fetch",
      "args": ["https://gitmcp.io/{{ github_owner }}/{{ repo_name }}"]
    }
  }
}
```

**Pros**: 
- Effortless setup for users
- Perfect for template parameterization
- No maintenance overhead
- Privacy-focused (no data retention)

**Cons**: 
- GitHub-only (not a major limitation)
- Requires internet connection

### 2. Buger's Docs-MCP ⭐⭐⭐⭐

**Repository**: https://github.com/buger/docs-mcp
**NPM**: `@buger/docs-mcp`
**Status**: ✅ Verified

**Key Features**:
- Powered by Probe search engine
- Supports both GitHub repos and local directories
- Flexible configuration (config file, CLI args, env vars)
- Handles multiple content types
- Optional automatic Git repository updates

**Usage**:
```bash
npx -y @buger/docs-mcp@latest --gitUrl <repository>
```

**Template Integration**:
```json
{
  "mcpServers": {
    "local-docs": {
      "command": "npx",
      "args": ["-y", "@buger/docs-mcp@latest", "--directory", "."]
    }
  }
}
```

**Pros**:
- Works with local directories
- Good for development workflows
- No API keys required
- Flexible content sources

**Cons**:
- Requires local installation via npx
- More complex configuration options

### 3. Arabold's Docs-MCP ⭐⭐⭐

**Repository**: https://github.com/arabold/docs-mcp-server
**Status**: ✅ Verified

**Key Features**:
- Indexes documentation from websites, GitHub, npm, PyPI, local files
- Semantic chunking with logical boundary preservation
- Multiple embedding model providers (OpenAI, Gemini, Azure, AWS)
- Version-aware documentation retrieval
- Docker deployment options

**Pros**:
- Comprehensive documentation indexing
- Advanced semantic processing
- Multiple deployment options
- Privacy-focused (runs locally)

**Cons**:
- More complex setup (Docker recommended)
- May require embedding model configuration
- Heavier resource requirements

## Unverified/Questionable Packages

### ❌ @zk-armor/mcp-sphinx-docs
- **Status**: Could not verify npm package exists
- **Issue**: Listed on LobeHub MCP directory but npm registry page inaccessible
- **Conclusion**: Do not recommend until verified

## Alternative Documentation Solutions

### Sphinx-Contrib MCP Extension
**Repository**: https://github.com/sphinx-contrib/mcp
**Purpose**: Sphinx extension for documenting MCP tools (not an MCP server itself)

### GitHub's Official MCP Server
**Repository**: https://github.com/github/github-mcp-server
**Status**: Public preview, GitHub-focused

## Recommendations for Template

### Multi-Tier MCP Strategy

Recommended configuration for `template/.auxiliary/configuration/mcp-servers.json`:

```json
{
  "mcpServers": {
    "project-docs": {
      "command": "mcp-server-fetch",
      "args": ["https://gitmcp.io/{{ github_owner }}/{{ repo_name }}"]
    },
    "local-docs": {
      "command": "npx", 
      "args": ["-y", "@buger/docs-mcp@latest", "--directory", "."]
    }
  }
}
```

### Implementation Priority

1. **Start with GitMCP** - zero friction, perfect for template parameterization
2. **Add Buger's Docs-MCP** - optional local development enhancement
3. **Consider Arabold's** - for projects needing advanced semantic search

## Advantages Over Firecrawl

1. **No API keys or costs** - all free and open source
2. **Documentation-optimized** - designed specifically for doc analysis
3. **Template-friendly** - can be parameterized with Copier variables
4. **Privacy-focused** - work without external data retention
5. **Multiple format support** - Sphinx, MkDocs, Markdown, HTML

## Integration with Custom MCP Server

These tools complement the in-development structure-aware MCP server:
- **GitMCP/Docs-MCP**: General doc retrieval and search
- **Custom MCP Server**: Structure-aware analysis of Sphinx/MkDocs sites
- **Combined**: Complete documentation analysis pipeline

## Next Steps

1. Test GitMCP integration in template
2. Validate Copier variable substitution works correctly
3. Document setup instructions for generated projects
4. Consider contributing Sphinx-specific MCP server if gap exists

---

*Research conducted: August 2025*
*Status: GitMCP recommended for immediate template integration*