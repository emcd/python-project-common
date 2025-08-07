---
allowed-tools: [Read, Write, Edit, MultiEdit, LS, Glob, Grep, Bash, TodoWrite, mcp__text-editor__get_text_file_contents, mcp__text-editor__edit_text_file_contents, mcp__ruff__diagnostics, mcp__ruff__edit_file, mcp__ruff__hover, mcp__ruff__references, mcp__ruff__rename_symbol, mcp__ruff__definition, mcp__pyright__diagnostics, mcp__pyright__edit_file, mcp__pyright__hover, mcp__pyright__references, mcp__pyright__rename_symbol, mcp__pyright__definition, mcp__context7__resolve-library-id, mcp__context7__get-library-docs]
description: Python implementation following established patterns and practices
---

# Python Implementation

Implement Python code following established patterns including functions,
classes, modules, tests, and refactoring while adhering to project practices
and style guidelines.

Request from user: $ARGUMENTS

Stop and consult if:
- Design specifications are needed instead of implementation
- Architectural decisions are required before implementation
- Requirements are unclear or insufficient for implementation
- Multiple implementation approaches have significant trade-offs requiring user input

## Context

- Architecture overview: @documentation/architecture/summary.rst
- Filesystem patterns: @documentation/architecture/filesystem.rst
- Python practices: @.auxiliary/instructions/practices.rst
- Code style: @.auxiliary/instructions/style.rst
- Nomenclature: @.auxiliary/instructions/nomenclature.rst
- Germanic variants: @.auxiliary/instructions/nomenclature-germanic.rst
- Design documents: !`ls documentation/architecture/designs/`
- Current package structure: !`ls sources/`

## Prerequisites

Before implementing Python code, ensure:
- Understanding of implementation requirements and expected behavior
- Familiarity with project practices, style, and nomenclature guidelines
- Knowledge of existing codebase structure and patterns
- Clear design specifications or existing design documents if referenced

## Process Summary

Key functional areas:
1. **Requirements Analysis**: Understand implementation requirements and context
2. **Design Conformance**: Ensure alignment with established patterns and practices
3. **Implementation**: Write Python code following style guidelines and best practices
4. **Quality Assurance**: Run linters, type checkers, and tests to validate code
5. **Documentation**: Provide implementation summary and any necessary documentation

## Safety Requirements

Stop and consult the user if:
- Implementation conflicts with established architectural patterns
- Code changes would break existing API contracts or interfaces
- Quality checks reveal significant issues that require design decisions
- Requirements are ambiguous or incomplete for proper implementation
- Multiple valid implementation approaches exist with different trade-offs

## Execution

Execute the following steps:

### 1. Requirements Analysis
Analyze implementation requirements and gather context:
- Review user requirements and any referenced design documents
- Examine existing codebase structure and relevant modules
- Identify integration points with existing code
- Understand expected behavior and edge cases
- Document implementation scope and constraints

### 2. Design Conformance Checklist
Ensure implementation aligns with project standards:
- [ ] Module organization follows practices guidelines (imports → type aliases → defaults → public API → private functions)
- [ ] Function signatures use wide parameter, narrow return patterns
- [ ] Type annotations are comprehensive and use proper TypeAlias patterns
- [ ] Exception handling follows Omniexception → Omnierror hierarchy
- [ ] Naming follows nomenclature conventions with appropriate linguistic consistency
- [ ] Immutability preferences are applied where appropriate
- [ ] Code style follows spacing, vertical compactness, and formatting guidelines

### 3. Implementation
Write Python code following established patterns:
- Implement functions, classes, or modules as specified
- Apply centralized import patterns via `__` subpackage
- Use proper type annotations with `__.typx.TypeAlias` for complex types
- Follow style guidelines for spacing, formatting, and structure
- Implement proper exception handling with narrow try blocks
- Apply nomenclature patterns for consistent naming
- Ensure functions are ≤30 lines and modules are ≤600 lines

### 4. Implementation Tracking Checklist
Track progress against requirements:
- [ ] All specified functions/classes have been implemented
- [ ] Required functionality is complete and tested
- [ ] Integration points with existing code are working
- [ ] Edge cases and error conditions are handled
- [ ] Documentation requirements are satisfied

### 5. Quality Assurance
Validate code quality and conformance:
```bash
hatch --env develop run linters
```
Address any linting issues that arise.

```bash
hatch --env develop run testers
```
Ensure all tests pass, including any new tests created.

### 6. Documentation and Summary
Provide implementation documentation:
- Document any non-obvious design decisions or trade-offs
- Create or update relevant docstrings following narrative mood guidelines
- Note any TODO items for future enhancements
- Verify alignment with filesystem organization patterns

### 7. Summarize Implementation
Provide concise summary of what was implemented, including:
- Functions, classes, or modules created or modified
- Key design decisions and rationale
- Integration points and dependencies
- Any remaining tasks or follow-up items
