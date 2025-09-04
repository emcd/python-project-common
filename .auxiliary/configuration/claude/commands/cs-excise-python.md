---
allowed-tools: Read, Write, Edit, MultiEdit, LS, Glob, Grep, Bash(hatch --env develop run:*), Bash(git status), Bash(git diff), mcp__pyright__references, mcp__pyright__hover, mcp__pyright__diagnostics
description: Analyze Vulture dead code findings and remediate through selective removal or vulturefood.py whitelisting
---

# Python Dead Code Analysis and Remediation

Systematically analyze Vulture dead code findings and remediate through selective removal or vulturefood.py whitelisting using Pyright MCP server for accurate symbol reference verification.

Target files or scope: $ARGUMENTS

## Context

- Current git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Existing vulturefood entries: !`wc -l .auxiliary/configuration/vulturefood.py`
- Vulture configuration: @pyproject.toml (tool.vulture section)

## Prerequisites

Before running this analysis, ensure:
- Understanding of project codebase and critical symbols
- Read project documentation guides:
  - @.auxiliary/instructions/practices.rst
  - @.auxiliary/instructions/style.rst
- Vulture is installed and configured in the development environment
- Pyright MCP server is available for symbol reference verification

## Process Summary

Key functional areas:
1. **Detection and Parsing**: Run Vulture and parse output for unused symbols
2. **Reference Verification**: Use Pyright MCP server to verify actual symbol usage
3. **Classification Analysis**: Apply heuristics to identify false positives vs. genuine dead code
4. **Selective Remediation**: Present findings with confidence levels for user decision
5. **Implementation**: Remove dead code or add entries to vulturefood.py as appropriate

## Safety Requirements

Stop and consult the user if:
- Uncertain about whether a symbol should be removed or whitelisted
- Complex inheritance hierarchies with unclear symbol usage patterns
- Vulture reports conflict significantly with Pyright reference analysis
- Ambiguous decorator patterns that don't fit standard heuristics

## Execution

Execute the following steps:

### 1. Vulture Analysis and Parsing

Run Vulture to identify potentially unused symbols:
```bash
hatch --env develop run vulture --min-confidence=60
```

Examine the output to extract:
- Symbol names and types (functions, classes, variables)
- File locations and line numbers
- Confidence levels reported by Vulture
- Symbol categories (imports, definitions, assignments)

### 2. Pyright Reference Verification

For each symbol identified by Vulture, verify actual usage using Pyright MCP:

Use `mcp__pyright__references` with **bare symbol names** (not qualified paths):
- Correct: `symbolName="function_name"`
- Incorrect: `symbolName="module.package.function_name"`

Analyze reference results:
- No references found: Likely genuine dead code
- References found: Examine context for legitimacy
- Import-only references: May indicate transitional dead code

### 3. False Positive Classification

Apply systematic heuristics to identify false positives:

**Common False Positive Patterns:**
- Abstract methods and protocol implementations
- Decorator-registered functions (pytest fixtures, Flask routes, etc.)
- Magic methods and dunder attributes
- CLI entry points and script main functions
- Test fixtures and utilities used via dynamic discovery
- Library interface methods called by external code

**Analysis Criteria:**
- Decorator presence and types
- Inheritance relationships and abstract base classes
- Usage patterns in test files vs. main code
- External integration points and plugin systems

### 4. Autonomous Decision Making

Apply systematic decision logic:

**Remove Symbol If:**
- No references found via Pyright (zero references)
- No TODO comments mentioning future use of the symbol
- Not an entry point function (e.g., `main`)
- Not part of unimplemented interface or abstract base class
- Not decorated with framework-specific decorators

**Whitelist in vulturefood.py If:**
- Has references but appears to be false positive (decorators, abstract methods, etc.)
- Entry point functions like `main`
- Abstract/interface implementations
- Framework integration points with decorators
- Magic methods and protocol compliance

**Check for TODO Comments:**
Examine surrounding code and docstrings for TODO comments that reference the symbol or indicate planned future usage.

### 5. Implementation Decision

Act autonomously based on decision logic:

**For Symbol Removal:**
- Remove symbol definitions and any orphaned imports
- Verify removal doesn't break related functionality
- Run linters to ensure clean code after removal

**For Vulturefood Whitelisting:**
- Add entries to `.auxiliary/configuration/vulturefood.py` with format:
  ```python
  symbol_name            # description of why it's a false positive
  ```
- Group related entries and add explanatory comments
- Maintain alphabetical organization within groups

### 6. Validation and Verification

After remediation:
- Run Vulture again to confirm issues are resolved
- Execute linters to ensure code quality: `hatch --env develop run linters`
- Run tests to verify functionality: `hatch --env develop run testers`
- Verify git diff shows only intended changes

## Implementation Notes

**Pyright MCP Usage:**
- Use bare symbol names for accurate reference finding
- Leverage superior semantic analysis over text-based search tools
- Cross-reference hover information for additional context

**Vulturefood Management:**
- Maintain clear documentation for each whitelisted symbol
- Group related false positives with explanatory sections
- Prefer descriptive comments over generic suppression

**Safety Practices:**
- Remove code autonomously when decision criteria are clearly satisfied
- Prioritize false positive whitelisting when uncertainty exists
- Validate all changes through comprehensive testing