---
description: Creates practical, testable examples documentation
---

# Document Examples

Develops practical, testable examples for documentation under
`documentation/examples/` that increase test coverage while remaining relatable
and succinct.

Topic: $ARGUMENTS

## Context

- Project structure: @documentation/architecture/filesystem.rst
- Existing examples: !`ls -la documentation/examples/ 2>/dev/null || echo "No examples directory"`
- Code coverage data: !`hatch --env develop run testers 2>/dev/null || echo "No coverage data available"`

## Prerequisites

Before creating examples documentation:
- Understand the target audience (developers vs end users)
- Analyze existing codebase to identify core functionality patterns
- Review existing examples for organization, completeness, and thematic inspiration
- Examine @.auxiliary/instructions/ for style and nomenclature requirements

## Process Summary

Key functional areas:
1. **Analysis**: Survey codebase and existing examples to identify documentation gaps
2. **Theme Development**: Create coherent scenarios that demonstrate functionality progression
3. **Content Creation**: Write succinct examples using proper reStructuredText formatting
4. **Validation**: Ensure examples follow project practices and can serve as informal tests

## Safety Requirements

Stop and consult the user if:
- Examples require creating contrived scenarios that don't reflect real usage
- Multiple conflicting themes emerge without clear organizational strategy
- Proposed examples would expose internal implementation details inappropriately
- Documentation format conflicts with existing project conventions

## Execution

Execute the following steps:

### 1. Analyze Existing Documentation Structure

Survey the current documentation to understand patterns and identify gaps. Read
existing example files to understand established themes and formatting
approaches.

### 2. Survey Codebase for Example Opportunities

Identify public API surfaces and common usage patterns. Analyze coverage
reports in `.auxiliary/artifacts/coverage-pytest` if available.

Look for:
- Public classes and functions that need demonstration
- Common workflows that span multiple components
- CLI commands and their typical usage patterns
- Error handling scenarios that users should understand

### 3. Develop Thematic Coherence

Based on analysis, choose one of these organizational approaches:

- **Domain scenarios**: Practical use cases
- **API progression**: Basic to advanced usage of core functionality
- **Workflow examples**: End-to-end processes showing component interaction
- **CLI workflows**: Command sequences for common tasks

### 4. Create Example Documentation

Write examples following these requirements:

- Use Sphinx reStructuredText format with proper double backticks for inline literals
- Include blank lines before list items per reStructuredText conventions
- Structure as progression from simple to complex scenarios
- Use doctest format for Python API examples where testable
- Use code-block format for CLI examples with explicit command annotation
- Keep code blocks comment-free; put explanatory text between blocks
- Follow @.auxiliary/instructions/practices.rst for general code organization
- Follow @.auxiliary/instructions/style.rst for formatting
- Follow @.auxiliary/instructions/nomenclature.rst for naming
- When documenting Python code, also follow .auxiliary/instructions/practices-python.rst for comprehensive Python standards
- When documenting Rust code, also follow .auxiliary/instructions/practices-rust.rst for comprehensive Rust standards
- When documenting TOML configuration, also follow .auxiliary/instructions/practices-toml.rst for comprehensive TOML standards

### 5. Ensure Practical Relevance

Verify each example:

- Demonstrates functionality users actually need
- Shows practical data and scenarios, remaining minimalist rather than elaborate
- Includes appropriate error cases and edge conditions
- Can serve as informal test coverage for documented features
- Follows established project patterns for similar examples

### 6. Validate Documentation Quality

Review final documentation for:

- Proper reStructuredText syntax and formatting
- Consistent theme and progression across examples
- Adherence to project style guidelines
- Executable/testable nature of code examples
- Clear explanatory text that guides readers through concepts

### 7. Provide Summary

Provide a succinct summary to the user describing:

- What examples were created or updated
- The organizational theme chosen and why
- Key functionality areas covered
- How the examples serve both documentation and testing goals
