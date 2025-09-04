---
description: Systematically conform Python code to project style and practice standards
---

# Python Code Conformance

For bringing existing Python code into full compliance with project standards.

Target: $ARGUMENTS

Focus on style/practice conformance, not functionality changes.

## Prerequisites

- Read project documentation guides first:
  - @.auxiliary/instructions/practices.rst
  - @.auxiliary/instructions/practices-python.rst
  - @.auxiliary/instructions/style.rst
  - @.auxiliary/instructions/nomenclature.rst
- Understand target files to be conformed
- Have read `CLAUDE.md` for project-specific guidance

## Context

- Current git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`

## Execution Structure

**Phase 1: Comprehensive Review**
Perform complete analysis and generate detailed compliance report before making any changes.

**Phase 2: Systematic Remediation**
Apply all identified fixes in systematic order, validating with linters after completion.

### Project Standards

Before proceeding with conformance analysis, you MUST:
1. Read @.auxiliary/instructions/practices.rst for general development principles
2. Read @.auxiliary/instructions/practices-python.rst for Python-specific patterns
3. In a step on your TODO list, please attest that you have read the general and Python-specific practices guides and demonstrate your knowledge by writing one-sentence summaries on any three of the following topics:

- the wide parameter, narrow return type pattern for robust interfaces
- the import organization rules and centralized import patterns
- when to use different immutable base classes (Object vs DataclassObject vs Protocol)
- the exception hierarchy pattern (Omniexception → Omnierror)
- the comprehensive examples showing multiple principles cohesively
- the module organization content order and size limits

## Conformance Verification

### Module Organization Verification
Confirm compliance with module organization patterns:
- [ ] Content follows proper order: imports, type aliases, private defaults, public classes/functions, private functions
- [ ] Module size ≤600 lines (analyze oversized modules for separation of concerns)
- [ ] Functions ≤30 lines each

### Import Organization Verification
Confirm compliance with import organization patterns:
- [ ] Module-level imports use private aliases (except in `__init__`, `__`, re-export modules)
- [ ] Common modules (os, re, etc.) imported through centralized `__.imports` rather than per-module
- [ ] No namespace pollution through public imports
- [ ] Subpackages define `__` re-export module with `from ..__ import *`
- [ ] No `__all__` attribute provided (unnecessary interface maintenance)

### Type Annotation Verification
Confirm compliance with type annotation patterns:
- [ ] Public functions use wide, abstract argument types (`__.cabc.Sequence`, `__.cabc.Mapping`)
- [ ] All functions define narrow, concrete return types (`list`, `dict`, `tuple`, `__.immut.Dictionary`)
- [ ] Proper function signature spacing following formatting guidelines
- [ ] `TypeAlias` declarations for complex types

### Immutability Verification
Confirm compliance with immutability patterns:
- [ ] Classes inherit from `__.immut.Object`, `__.immut.Protocol`, `__.immut.DataclassObject`
- [ ] Functions return immutable types (`tuple`, `frozenset`, `__.immut.Dictionary`) not mutable types (`list`, `dict`, `set`)
- [ ] Dependency injection with sensible defaults applied

### Exception Handling Verification
Confirm compliance with exception handling patterns:
- [ ] One `try..except` suite per statement that can raise exceptions
- [ ] Narrow try block scope maintained
- [ ] Proper exception chaining and hierarchy usage
- [ ] No bare exceptions raised (except `NotImplementedError`)

### Documentation Verification
Confirm compliance with documentation patterns:
- [ ] Docstrings use triple single quotes with narrative mood
- [ ] Exception messages in double quotes
- [ ] No comments describing obvious behavior
- [ ] TODO comments for uncovered edge cases

### Style Formatting Verification
Confirm compliance with formatting standards:
- [ ] Space padding inside delimiters: `( arg )`, `[ item ]`, `{ key: value }`
- [ ] Space padding around keyword argument `=`: `foo = 42`
- [ ] F-strings in double quotes: `f"text {variable}"`
- [ ] No blank lines within function bodies
- [ ] Single-line statements on same line when appropriate: `if condition: return value`
- [ ] Proper multi-line construct delimiter placement

### Quality Assurance Verification
Confirm compliance with quality assurance principles:
- [ ] Critical review of all linter suppressions
- [ ] No `type: ignore` usage (investigate underlying issues)
- [ ] No `__.typx.cast` usage (investigate type system issues)
- [ ] Minimal `noqa` pragmas with compelling justification only

### Violation Analysis Reference

For comprehensive violation examples and correction patterns, see the comprehensive examples in practices-python.rst, which demonstrate proper application of all conformance principles in cohesive, real-world contexts.

When analyzing violations, reference the specific sections of practices-python.rst that address each violation type rather than duplicating examples here.

## Review Report Format

Phase 1 Output:
1. **Compliance Summary**: Overall assessment with file-by-file breakdown
2. **Standards Violations**: Categorized list with specific line references and explanations
3. **Complexity Analysis**: Function and module size assessments
4. **Remediation Plan**: Systematic order of fixes to be applied
5. **Risk Assessment**: Any changes that require careful validation

Phase 2 Output:
1. **Applied Fixes**: Summary of all changes made, categorized by standard
2. **Validation Results**: Linter output before and after changes
3. **Files Modified**: Complete list with brief description of changes
4. **Manual Review Required**: Any issues requiring human judgment

## Conformance Process

### 1. Analysis Phase (PHASE 1)
- Examine target files to understand current state
- Run linters to identify specific violations
- Identify architectural patterns that need updating
- Generate comprehensive compliance report
- **Requirements**: Complete review and report before any remediation
- **Focus**: Reference specific lines with concrete examples and explain reasoning

### 2. Systematic Correction (PHASE 2)

Before applying any fixes, confirm:
- [ ] I have completed comprehensive analysis with specific line references
- [ ] I understand each violation type and its corresponding practices-python.rst section
- [ ] I have a systematic remediation plan prioritized by impact

**Apply fixes in appropriate order**:
1. **Module Organization**: Reorder per established organizational patterns
2. **Import Organization**: Apply centralized import organization rules
3. **Type Annotations**: Convert to wide parameter/narrow return patterns
4. **Immutability**: Apply immutable container and base class patterns
5. **Exception Handling**: Apply narrow try block and hierarchy patterns
6. **Documentation**: Apply narrative mood and formatting patterns
7. **Formatting**: Apply spacing, delimiter, and vertical compactness standards
8. **Quality Assurance**: Apply linter compliance and suppression principles

For comprehensive type annotation work or complex type checking issues, consider using the `python-annotator` agent.

**POST-CORRECTION VERIFICATION GATE**
After applying all fixes, confirm:
- [ ] All verification checklists from practices-python.rst sections pass
- [ ] `hatch --env develop run linters` produces clean output
- [ ] `hatch --env develop run testers` passes with no functionality breaks
- [ ] Code follows all practices-python.rst patterns exactly

## Safety Requirements

Stop and consult if:
- Linters reveal complex architectural issues
- Changes would alter functionality
- Type annotations conflict with runtime behavior
- Import changes break dependencies
- Tests start failing

Your responsibilities:
- Maintain exact functionality while improving practices/style
- Use project patterns consistently per the guides
- Reference all three guides for complex cases
- Verify all changes with linters and tests

## Success Criteria

- [ ] All linting violations resolved
- [ ] Module organization follows practices guide structure
- [ ] Function parameters use wide abstract types
- [ ] Imports avoid namespace pollution
- [ ] Type annotations comprehensive with `TypeAlias` usage
- [ ] Exception handling uses narrow try blocks
- [ ] Immutable containers used where appropriate
- [ ] No functionality changes
- [ ] Tests continue to pass
- [ ] Code follows all style guide patterns

**Note**: Always run full validation (`hatch --env develop run linters && hatch
--env develop run testers`) before considering the task complete.

## Final Report

Upon completion, provide a brief report covering:
- Specific conformance issues corrected (categorized by the priority issues above)
- Number of files modified
- Any patterns that required manual intervention
- Linter status before/after
- Any deviations from guides and justification
