---
allowed-tools: [Read, Write, Edit, MultiEdit, LS, Glob, Grep, WebFetch, WebSearch, Bash(ls:*), Bash(find:*), Bash(tree:*), mcp__context7__resolve-library-id, mcp__context7__get-library-docs]
description: Python API design, filesystem organization, module structure, and interface specifications
---

# Python Design Analysis

Analyze Python API design patterns, filesystem organization, module structure, class hierarchies, interface definitions, and design patterns to provide guidance on Python-specific structural decisions and project organization. Focus exclusively on interface contracts, signatures, and type specifications—never implementation details or method bodies.

Request from user: $ARGUMENTS

## Context

- Architecture overview: @documentation/architecture/summary.rst
- Filesystem patterns: @documentation/architecture/filesystem.rst
- Python practices: @.auxiliary/instructions/practices.rst
- Python practices (detailed): @.auxiliary/instructions/practices-python.rst
- Code style: @.auxiliary/instructions/style.rst
- Python style (detailed): @.auxiliary/instructions/style-python.rst
- Nomenclature: @.auxiliary/instructions/nomenclature.rst
- Germanic variants: @.auxiliary/instructions/nomenclature-germanic.rst
- Design documents: !`ls documentation/architecture/designs/`

## Prerequisites

Before providing design analysis, ensure:
- Understanding of module organization and class hierarchies
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
- Architectural decisions are needed instead of design specifications
- Implementation details are requested instead of design specifications
- Requirements analysis is needed instead of design specifications
- User requests actual code implementations instead of specifications
- Design decisions require architectural changes beyond Python structure
- Interface changes would break existing API contracts significantly
- Design conflicts with established filesystem organization patterns
- Requirements are unclear or insufficient for proper design specification
- Multiple design approaches have significant trade-offs requiring user input

## Execution

Execute the following steps:

### 1. Design Analysis
Examine Python structure and patterns:
- Review module organization and import patterns
- Analyze class hierarchies and interface definitions
- Identify design patterns in use
- Assess alignment with practices and nomenclature guidelines
- Document design strengths and improvement opportunities

### 2. Interface Specification
Define clean API boundaries and contracts following practices guidelines:

Define interfaces through signatures and type annotations only. Avoid specifying how methods should be implemented internally—focus on contracts, not implementation logic.

- All function and class signatures must follow @.auxiliary/instructions/practices.rst patterns exactly
- Specify public interfaces using wide parameter, narrow return patterns (e.g., __.cabc.Sequence, __.cabc.Mapping for inputs)
- Return narrow concrete types (list, dict, tuple, __.immut.Dictionary for outputs)
- Design class hierarchies following Omniexception → Omnierror patterns
- Apply appropriate naming conventions from nomenclature guidelines
- Define type annotations using proper TypeAlias patterns with __.typx.TypeAlias
- Consider immutability preferences and container design patterns

### 3. Filesystem and Module Organization Design
Apply Python-specific organizational patterns and filesystem structure:
- Design project filesystem organization and update filesystem.rst as needed
- Design module structure following the standard organization order
- Plan `__` subpackage integration for centralized imports
- Specify exception hierarchies and their organization
- Design interface patterns for different component types
- Plan type alias organization and dependency management

### 4. Class and Function Design
Create maintainable Python structures following practices guide exactly:

Design class structures through their public contracts and type relationships. Specify signatures, inheritance patterns, and interface boundaries—never internal implementation logic or method bodies.

- Design class hierarchies with appropriate base classes and mixins (__.immut.Object, __.immut.Protocol, etc.)
- Specify function signatures using practices guide patterns (wide inputs, narrow outputs, proper spacing)
- Apply nomenclature patterns for methods, attributes, and functions from nomenclature guidelines
- Design immutable data structures and container patterns
- Plan dependency injection and configuration patterns with sensible defaults

### 5. Design Documentation
Create comprehensive design specifications without implementations:

Use atemporal language in all specifications. Avoid temporal terms like 'new', 'current', 'existing', 'future'—designs should read as canonical specifications independent of implementation timeline.

- Generate design documents following established format
- Update `documentation/architecture/designs/index.rst` to include designs
- Provide only signatures, contracts, and interface specifications - no implementations
- Do not provide exception class implementations, function bodies, or method implementations
- Document interface contracts and expected behaviors (contracts only, not code)
- Provide design examples using signatures and type annotations only
- Specify exception handling patterns and error propagation (exception classes by name/signature only)
- Document design rationale and trade-off decisions

### 6. Design Validation
Ensure design quality and consistency:
- Verify alignment with practices, style, and nomenclature guidelines
- Check consistency with filesystem organization patterns
- Validate that wide parameter/narrow return patterns are followed
- Ensure proper separation between public and private interfaces
- Confirm that design supports expected usage patterns and extensibility

### 7. Summarize Updates
Provide concise summary of updates to the user.