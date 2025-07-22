---
allowed-tools: Bash(hatch --env develop run:*), Bash(git:*), LS, Read, Glob, Grep, Edit, MultiEdit, Write, WebFetch
description: Systematically conform Python code to project style and practice standards
---

# Python Code Conformance

For bringing existing Python code into full compliance with project standards.

Target code: `$ARGUMENTS`

**CRITICAL**: This command focuses on style/practice conformance, not functionality changes.

## Context

- Current git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Linter status: !`hatch --env develop run linters || echo "Linting issues detected"`

## Prerequisites

- **MANDATORY**: Access project style guide:
  ```
  documentation/common/style.rst
  documentation/common/practices.rst
  ```
- Understand target files to be conformed
- Have read `CLAUDE.md` for project-specific guidance

## Common Conformance Issues

### 1. Spacing and Delimiters
**Issue:** Missing spaces in delimiters, operators
**Before:**
```python
def func(arg1,arg2="default"):
    result=process(arg1,{"key":"value"})
    return result
```
**After:**
```python
def func( arg1, arg2 = 'default' ):
    result = process( arg1, { 'key': 'value' } )
    return result
```

### 2. Docstring Format
**Issue:** Wrong quotes, spacing, structure
**Before:**
```python
def example():
    """Bad docstring format"""
    
class Example:
    """Multi-line
    description here"""
```
**After:**
```python
def example( ):
    ''' Proper docstring format. '''
    
class Example:
    ''' Multi-line description.
    
        Additional details here.
    '''
```

### 3. Import Organization
**Issue:** Module pollution, wrong structure
**Before:**
```python
from pathlib import Path
from collections import defaultdict
import asyncio
from . import utils
```
**After:**
```python
import asyncio
from collections import defaultdict
from pathlib import Path

from . import __
from . import utils as _utils
```

### 4. Type Annotations
**Issue:** Missing hints, wrong patterns
**Before:**
```python
def process(data, options=None):
    if options is None: options = {}
    return data
```
**After:**
```python
def process( data: str, options: dict | None = None ) -> str:
    if options is None: options = { }
    return data
```

### 5. Line Length and Continuation
**Issue:** Long lines, wrong continuation style
**Before:**
```python
result = some_very_long_function_name(first_argument, second_argument, third_argument, fourth_argument)
```
**After:**
```python
result = some_very_long_function_name(
    first_argument, second_argument, third_argument, fourth_argument )
```

### 6. Function and Class Structure
**Issue:** Wrong spacing, single-line forms
**Before:**
```python
def simple_func(x): return x * 2

class EmptyClass:
    pass
```
**After:**
```python
def simple_func( x: int ) -> int: return x * 2

class EmptyClass: pass
```

## Conformance Process

### 1. Analysis Phase
- Read target files to understand current state
- Run linters to identify specific violations
- Check against style guide patterns

### 2. Systematic Correction
Apply fixes in this order:
1. **Spacing/Delimiters**: Fix `( )`, `[ ]`, `{ }` patterns
2. **Quotes**: Single for literals, double for f-strings/logging
3. **Docstrings**: Triple single quotes with proper spacing  
4. **Imports**: Organization per style guide
5. **Type Hints**: Add missing annotations
6. **Line Length**: Split at 79 columns using parentheses
7. **Function Structure**: Single-line forms where appropriate

### 3. Validation
```bash
hatch --env develop run linters  # Must pass clean
hatch --env develop run testers  # Must not break functionality
```

## Safety Requirements

**HALT if:**
- Linters reveal complex architectural issues
- Changes would alter functionality
- Type annotations conflict with runtime behavior
- Import changes break dependencies
- Tests start failing

**Your responsibilities:**
- Maintain exact functionality while improving style
- Use project patterns consistently
- Reference style guides for complex cases
- Verify all changes with linters and tests

## Success Criteria

- [ ] All linting violations resolved
- [ ] No functionality changes
- [ ] Tests continue to pass
- [ ] Code follows all style guide patterns
- [ ] Imports properly organized
- [ ] Type annotations added where appropriate
- [ ] Line length within 79 columns
- [ ] Proper spacing and delimiter usage

**Note**: Always run full validation (`hatch --env develop run testers && hatch --env develop run linters`) before considering the task complete.

## Final Report

Upon completion, provide a brief report covering:
- Specific style violations corrected
- Number of files modified
- Any patterns that required manual intervention
- Linter status before/after
- Any deviations from standard patterns and justification