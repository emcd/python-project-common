---
allowed-tools: [Read, Write, Edit, MultiEdit, LS, Glob, Grep, WebFetch, WebSearch, mcp__context7__resolve-library-id, mcp__context7__get-library-docs]
description: Python API design, module structure, and interface specifications
---

# Python Design Analysis

Analyze Python API design patterns, module structure, class hierarchies, interface definitions, and design patterns to provide guidance on Python-specific structural decisions.

Request from user: $ARGUMENTS

Stop and consult if:
- Architectural decisions are needed instead of design specifications
- Implementation details are requested instead of design specifications
- Requirements analysis is needed instead of design specifications

## Context

- Architecture overview: @documentation/architecture/summary.rst
- Filesystem patterns: @documentation/architecture/filesystem.rst
- Python practices: @.auxiliary/instructions/practices.rst
- Code style: @.auxiliary/instructions/style.rst
- Nomenclature: @.auxiliary/instructions/nomenclature.rst
- Germanic variants: @.auxiliary/instructions/nomenclature-germanic.rst
- Design documents: !`ls documentation/architecture/designs/`

## Prerequisites

Before providing design analysis, ensure:
- Understanding of current module organization and class hierarchies
- Familiarity with Python practices and style guidelines
- Knowledge of nomenclature conventions and naming patterns
- @.auxiliary/instructions/practices.rst patterns are followed

## Process Summary

Key functional areas:
1. **Design Analysis**: Examine current Python structure and design patterns
2. **Interface Specification**: Define clean API boundaries and contracts
3. **Module Organization**: Apply filesystem and import patterns effectively
4. **Class Design**: Create maintainable hierarchies and interface patterns
5. **Documentation**: Specify design decisions with examples and rationale

## Safety Requirements

Stop and consult the user if:
- Design decisions require architectural changes beyond Python structure
- Interface changes would break existing API contracts significantly
- Design conflicts with established filesystem organization patterns
- Requirements are unclear or insufficient for proper design specification
- Multiple design approaches have significant trade-offs requiring user input

## Execution

Execute the following steps:

### 1. Current Design Analysis
Examine existing Python structure and patterns:
- Review current module organization and import patterns
- Analyze existing class hierarchies and interface definitions
- Identify design patterns currently in use
- Assess alignment with practices and nomenclature guidelines
- Document current design strengths and improvement opportunities

### 2. Interface Specification
Define clean API boundaries and contracts:
- Specify public interfaces using wide parameter, narrow return patterns
- Design class hierarchies following Omniexception → Omnierror patterns
- Apply appropriate naming conventions from nomenclature guidelines
- Define type annotations using proper TypeAlias patterns
- Consider immutability preferences and container design patterns

### 3. Module Organization Design
Apply Python-specific organizational patterns:
- Design module structure following the standard organization order
- Plan `__` subpackage integration for centralized imports
- Specify exception hierarchies and their organization
- Design interface patterns for different component types
- Plan type alias organization and dependency management

### 4. Class and Function Design
Create maintainable Python structures:
- Design class hierarchies with appropriate base classes and mixins
- Specify function signatures with proper type annotations
- Apply nomenclature patterns for methods, attributes, and functions
- Design immutable data structures and container patterns
- Plan dependency injection and configuration patterns

### 5. Design Documentation
Create comprehensive design specifications:
- Document interface contracts and expected behaviors
- Provide design examples following style guidelines
- Specify exception handling patterns and error propagation
- Document design rationale and trade-off decisions
- Create interface specifications without implementation details

### 6. Design Validation
Ensure design quality and consistency:
- Verify alignment with practices, style, and nomenclature guidelines
- Check consistency with filesystem organization patterns
- Validate that wide parameter/narrow return patterns are followed
- Ensure proper separation between public and private interfaces
- Confirm that design supports expected usage patterns and extensibility

### 7. Summarize Updates
Provide concise summary of updates to the user.