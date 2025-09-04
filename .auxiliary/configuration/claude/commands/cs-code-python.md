---
description: Python implementation following established patterns and practices
---

# Python Implementation

Implement Python code following established patterns including functions,
classes, modules, tests, and refactoring while adhering to project practices
and style guidelines.

Request from user: $ARGUMENTS

## Context

- Architecture overview: @documentation/architecture/summary.rst
- Filesystem patterns: @documentation/architecture/filesystem.rst
- General practices: @.auxiliary/instructions/practices.rst
- Python development guide: @.auxiliary/instructions/practices-python.rst
- Code style: @.auxiliary/instructions/style.rst
- Nomenclature: @.auxiliary/instructions/nomenclature.rst
- Design documents: @documentation/architecture/designs/

## Prerequisites

Before implementing Python code, ensure:
- Understanding of implementation requirements and expected behavior
- Knowledge of existing codebase structure and patterns
- Clear design specifications or existing design documents if referenced

### Guide Consultation Requirements

Before implementing Python code, you MUST:
1. Read @.auxiliary/instructions/practices.rst for general development principles
2. Read @.auxiliary/instructions/practices-python.rst for Python-specific patterns
3. In a step on your TODO list, please attest that you have read the general and Python-specific practices guides and demonstrate your knowledge by writing one-sentence summaries on any three of the following topics:

- the comprehensive examples showing multiple principles cohesively
- proper module organization content order
- import organization and centralized import patterns
- wide parameter, narrow return type patterns for robust interfaces
- immutability preferences for data structures and containers
- exception handling with narrow try blocks and proper chaining
- documentation formatting requirements including narrative mood
- quality assurance principles including linter compliance

## Process Summary

Key functional areas:
1. **Requirements Analysis**: Understand implementation requirements and create persistent tracking
2. **Session Continuity**: Check for existing work and preserve context across sessions
3. **Implementation**: Write Python code following style guidelines and best practices
4. **Progress Tracking**: Maintain session and cross-session implementation progress
5. **Quality Assurance**: Run linters, type checkers, and tests to validate code
6. **Documentation**: Update persistent tracking and provide implementation summary

## Safety Requirements

Stop and consult the user if:
- Design specifications are needed instead of implementation
- Architectural decisions are required before implementation
- Requirements are unclear or insufficient for implementation
- Implementation conflicts with established architectural patterns
- Code changes would break existing API contracts or interfaces
- Quality checks reveal significant issues that require design decisions
- Type checker errors are encountered that cannot be resolved through standard remediation
- Multiple implementation approaches have significant trade-offs requiring user input

## Execution

Execute the following steps:

### 1. Requirements Analysis
Analyze implementation requirements and gather context:
- Review user requirements and any referenced design documents
- Examine existing codebase structure and relevant modules
- Identify integration points with existing code
- Understand expected behavior and edge cases
- Document implementation scope and constraints

#### 1.1 Create Implementation Tracking File
Before beginning implementation, create a persistent tracking file with descriptive naming:
- Format: `.auxiliary/notes/<short-implementation-title>--progress.md`
- Example: `.auxiliary/notes/user-metrics-export--progress.md`

Choose a concise but descriptive title that captures the main implementation goal.

Structure the tracking file with these sections:

### Context and References
- **Implementation Title**: [Brief description of what is being implemented]
- **Start Date**: [YYYY-MM-DD]
- **Reference Files**: [List all files explicitly provided as context/references at start]
  - `path/to/reference1.py` - [Brief description of relevance]
  - `path/to/reference2.rst` - [Brief description of relevance]
- **Design Documents**: [Any architecture or design docs referenced]
- **Session Notes**: [Link to current session TodoWrite items]

### Design and Style Conformance Checklist
- [ ] Module organization follows practices guidelines
- [ ] Function signatures use wide parameter, narrow return patterns
- [ ] Type annotations comprehensive with TypeAlias patterns
- [ ] Exception handling follows Omniexception → Omnierror hierarchy
- [ ] Naming follows nomenclature conventions
- [ ] Immutability preferences applied
- [ ] Code style follows formatting guidelines

### Implementation Progress Checklist
- [ ] [Specific function/class/module 1]
- [ ] [Specific function/class/module 2]
- [ ] [Integration point 1] tested
- [ ] [Integration point 2] tested

### Quality Gates Checklist
- [ ] Linters pass (`hatch --env develop run linters`)
- [ ] Type checker passes
- [ ] Tests pass (`hatch --env develop run testers`)
- [ ] Code review ready

### Decision Log
Document significant decisions made during implementation:
- [Date] [Decision made] - [Rationale]
- [Date] [Trade-off chosen] - [Why this approach over alternatives]

### Handoff Notes
For future sessions or other developers:
- **Current State**: [What's implemented and what's not]
- **Next Steps**: [Immediate next actions needed]
- **Known Issues**: [Any problems or concerns to address]
- **Context Dependencies**: [Critical knowledge for continuing work]

### 2. Session Continuity and Context Preservation
Before proceeding with implementation:

#### Check for Existing Implementation
```bash
ls .auxiliary/notes/*--progress.md
```

If continuing previous work:
- Read existing tracking file completely to understand context
- Review reference files listed in context section
- Check decision log for previous design choices
- Update "Current State" in handoff notes as you resume work

#### Context Preservation Requirements
Before beginning implementation:
- [ ] Create descriptive tracking file (`.auxiliary/notes/<title>--progress.md`)
- [ ] Record all reference files provided at session start
- [ ] Document initial understanding of requirements
- [ ] Note any existing related implementations or patterns found

During implementation:
- [ ] Update decision log when making design choices
- [ ] Record integration points and dependencies discovered
- [ ] Document deviations from original plan with rationale

Before session end:
- [ ] Update current state in handoff notes
- [ ] Ensure TodoWrite completions are reflected in persistent tracking where granularity aligns
- [ ] Record next steps for continuation

### 3. Implementation

**Write Python code following established patterns**:
- Apply comprehensive guide patterns for module organization, imports, annotations, immutability, exception handling, and documentation
- Consult the comprehensive guides when you need specific implementation details
- For complex annotation work or systematic annotation issues, consider using the `python-annotator` agent

### 4. Progress Tracking Requirements
Maintain dual tracking systems:
- **Session Level**: Use TodoWrite tool for immediate task management within current session
- **Cross-Session**: Update `.auxiliary/notes/<implementation-title>--progress.md` for persistent tracking
- **Synchronization**: When TodoWrite items align with persistent checklist granularity, update corresponding persistent checklist items (TodoWrite may be more fine-grained)
- **Context Preservation**: Record all reference files and design decisions in persistent file for future session continuity

### 5. Quality Assurance

Before proceeding, add this quality verification checklist to your TODO list:
- [ ] Code follows proper module organization patterns
- [ ] Imports follow organization rules with centralized patterns
- [ ] Type annotations use wide parameter, narrow return patterns
- [ ] Functions ≤30 lines, modules ≤600 lines
- [ ] Immutability preferences applied to data structures
- [ ] Exception handling uses narrow try blocks with proper chaining
- [ ] Documentation follows narrative mood requirements
- [ ] Quality assurance principles applied

#### Validation Commands
**Linting Validation** (zero-tolerance policy):
```bash
hatch --env develop run linters
```
All issues must be addressed per comprehensive guide principles. Do not use `noqa` without explicit approval.

**Type Checking** (systematic resolution):
```bash
hatch --env develop run linters  # Includes Pyright
```

**Type Error Resolution Process**:
1. **Code Issues**: Fix immediately using comprehensive guide type annotation patterns
2. **Third-party Stubs**: Follow guidance in Python-specific practices guide (ensure dependency in `pyproject.toml`, prune Hatch environment, Pyright `createstub`, manage stubs)
3. **Complex Issues**: Use `python-annotator` agent for systematic resolution

Stop and consult user if type errors cannot be categorized or require architectural decisions.

**Test Validation**:
```bash
hatch --env develop run testers
```
All tests must pass, including new implementations.

### 6. Documentation and Summary

**Provide implementation documentation**:
- Update persistent tracking file with implementation state
- Document design decisions and trade-offs in decision log
- Complete handoff notes for session continuity
- Note TODO items for future work

### 7. Summarize Implementation
Provide concise summary of what was implemented, including:
- Functions, classes, or modules created or modified
- Key design decisions and rationale
- Integration points and dependencies
- Quality assurance status: Confirm all linters, type checkers, and tests pass
- Checklist of principles and patterns applied during implementation
- Any remaining tasks or follow-up items
