# CLI Repository Commands Proposal

## Background

The `configure-clone.bash` script from `gh-repositor` performs two distinct functions:
1. Git infrastructure setup (LFS, pre-commit hooks)
2. LLM development environment preparation (symlinks, documentation)

## Proposed Solution

Integrate this functionality into `emcdproj` as repository management commands.

## Command Structure

```bash
# Using pipx
pipx run --spec emcd-projects emcdproj repository setup-git-hooks
pipx run --spec emcd-projects emcdproj repository prepare-llm-agents

# Using uvx  
uvx --from emcd-projects emcdproj repository setup-git-hooks
uvx --from emcd-projects emcdproj repository prepare-llm-agents
```

## Implementation Plan

### CLI Integration (`cli.py`)
- Add `repository` command group
- Add `setup-git-hooks` subcommand
- Add `prepare-llm-agents` subcommand
- Support common options: `--dry-run`, `--force`

### Core Logic (`repository.py`)
New module in `emcdproj` package containing:
- Repository root detection
- Git LFS installation and configuration
- Pre-commit hook setup
- Symlink creation for LLM configs (CLAUDE.md, .mcp.json, etc.)
- Documentation downloading from python-project-common
- Safe file operations with proper error handling

### Functionality Split

**setup-git-hooks**:
- Validate Git repository
- Install/update Git LFS
- Configure pre-commit hooks for Python projects
- Validate hook installation

**prepare-llm-agents**:
- Create symlinks to `.auxiliary/configuration/` files
- Download project documentation guides
- Set up Claude/Gemini configuration files
- Validate LLM environment

## Benefits

1. **No Import Shadowing**: Functionality lives in proper package namespace
2. **Consistent CLI**: Leverages existing `emcdproj` CLI framework
3. **Standard Distribution**: Available via `pipx`/`uvx` without local files
4. **Testable**: Proper Python package structure enables testing
5. **Single Responsibility**: Clear separation between Git and LLM setup
6. **Cross-Platform**: Pure Python eliminates bash dependencies

## Migration

- Keep existing bash script temporarily with deprecation notice
- Point users to new `emcdproj repository` commands
- Remove bash script after adoption period

## Next Steps

1. Implement `repository.py` module with core functionality
2. Add CLI commands to `cli.py`
3. Write tests for repository operations
4. Update documentation
5. Deprecate bash script