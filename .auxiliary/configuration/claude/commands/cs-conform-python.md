---
allowed-tools: Bash(hatch --env develop run:*), Bash(git:*), LS, Read, Glob, Grep, Edit, MultiEdit, Write, WebFetch
description: Systematically conform Python code to project style and practice standards
---

# Python Code Conformance

For bringing existing Python code into full compliance with project standards.

Target code: `$ARGUMENTS`

Focus on style/practice conformance, not functionality changes.

## Prerequisites

- Read project documentation guides first:
  - @.auxiliary/instructions/practices.rst
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

## Compliance Standards

### Design Standards

#### 1. Module Organization

Content Order:
1. Imports (following practices guide patterns)
2. Common type aliases (`TypeAlias` declarations)
3. Private variables/functions for defaults (grouped semantically)
4. Public classes and functions (alphabetical)
5. All other private functions (alphabetical)

Scope and Size:
- Maximum 600 lines
- Action: Analyze oversized modules with separation of concerns in mind.
Suggest splitting into focused modules with narrower responsibilities or
functionality.

#### 2. Imports

- At the module level, other modules and their attributes MUST be imported as
  private aliases, except in `__init__`, `__`, or specially-designated
  re-export modules.
- Within function bodies, other modules and their attributes MAY be imported as
  public variables.
- Subpackages SHOULD define a special `__` re-export module, which has `from
  ..__ import *` plus any other imports which are common to the subpackage.
- Common modules, such as `os` or `re`, SHOULD be imported as public within the
  special package-wide `__.imports` re-export module rather than as private
  aliases within an implementation module.
- The `__all__` attribute SHOULD NOT be provided. This is unnecessary if the
  module namespace only contains public classes and functions which are part of
  its interface; this avoid additional interface maintenance.

#### 3. Dependency Injection

- Ask: is this function testable without monkeypatching?
- Functions SHOULD provide injectable parameters with sensible defaults instead
  of hard-coded dependencies within function implementation.

#### 4. Robustness Principle (Postel's Law)
"Be conservative in what you send; be liberal in what you accept."

- Public functions SHOULD define wide, abstract argument types.
- All functions SHOULD define narrow, concrete return types.
- Private functions MAY define narrow, concrete argument types.

#### 5. Immutability

- Classes SHOULD inherit from immutable classes (`__.immut.Object`,
  `__.immut.Protocol`, `__.immut.DataclassObject`, etc...).
- Functions SHOULD return values of immutable types (`None`, `int`, `tuple`,
  `frozenset`, `__.immut.Dictionary`, etc...) and not mutable types (`list`,
  `dict`, `set`, etc...).

#### 6. Proper Exception Management

- One `try .. except` suite per statement which can raise exceptions. I.e.,
  avoid covering multiple statements with a `try` block whenever possible.
- Tryceratops complaints MUST NOT be suppressed with `noqa` pragmas.
- Bare exceptions SHOULD NOT be raised.
    - Exemption: `NotImplementedError` MAY be raised as a bare exception.
    - Relevant exception classes SHOULD be used from the relevant `exceptions`
      module within the package.
    - New exception classes MAY be created as needed within the relevant
      `exceptions` module; these MUST follow the nomenclature guide and be
      inserted in correct alphabetical order.

### Quality Assurance

#### 1. Linter Suppressions

- Linter suppressions MUST be reviewed critically.
- Linter complaints SHOULD NOT be suppressed via `noqa` or `type` pragmas
  without compelling justification.
- Suppressions that mask design problems MUST be investigated and resolved
  rather than ignored.

Acceptable Suppressions:
- `noqa: PLR0913` MAY be used for a CLI or service API with many parameters,
  but data transfer objects SHOULD be considered in most other cases.
- `noqa: S*` MAY be used for properly constrained and vetted  subprocess
  executions or Internet content retrievals.

Unacceptable Suppressions (require investigation):
- `type: ignore` MUST NOT be used, except in extremely rare circumstances. Such
  suppressions usually indicate missing third-party dependencies or type stubs,
  inappropriate type variables, or a bad inheritance pattern.
- `__.typx.cast` SHOULD NOT be used, except in extremely rare circumstances.
  Such casts suppress normal type checking and usually the same problems as
  `type: ignore`.
- Most other `noqa` suppressions.

### Style Standards

#### 1. Spacing and Delimiters

- Space padding MUST be present inside delimiters.
    - Format: `( arg )`, `[ item ]`, `{ key: value }`
    - Format: `( )`, `[ ]`, `{ }`, not `()`, `[]`, `{}`
- Space padding MUST be present around keyword argument `=`.
    - Format: `foo = 42`

#### 2. Strings

- Docstrings MUST use triple single quotes with narrative mood.
    - Format: `''' Processes data... '''` not `"""Process data..."""`
- F-strings and `.format` strings MUST be enclosed in double quotes.
    - Format: `f"text {variable}"`, not `f'text {variable}'`
    - Format: `"text {count}".format( count = len( items ) )`
- F-strings and format strings MUST NOT embed function calls.
- Exception messages and log messages SHOULD be enclosed in double quotes
  rather than single quotes.
- Plain data strings SHOULD be enclosed in single quotes, unless they contain
  single quotes.

#### 3. Vertical Compactness

- Blank lines MUST NOT appear within function bodies.
- Vertical compactness MUST be maintained within function implementations.
- Single-line statements MAY follow certain block keywords on the same line
  when appropriate.
    - Format: `if condition: return value`
    - Format: `elif condition: continue`
    - Format: `else: statement`
    - Format: `try: statement`

#### 4. Multi-line Constructs

- Function invocations, including class instantiations, SHOULD place the
  closing `)` on the same line as the last argument to the function.
- The last argument of an invocation MUST NOT be followed by a trailing comma.
- Comprehensions and generator expressions SHOULD place the closing delimiter
  on the same line as the last statement in the comprehension or generator
  expression.
- Parenthetical groupings SHOULD place the closing delimiter on the same line
  as the last statement in the grouping.
- All other multi-line constructs (functions signatures, annotations, lists,
  dictionaries, etc...) MUST place the closing delimiter on a separate line
  following the last item and MUST dedent the closing delimiter to match the
  opening line indentation.
- If a closing delimiter is not on the same line as the last item in a
  multi-line construct, then the last item MUST be followed by a trailing
  comma.

#### 5. Nomenclature

- Argument, attribute, and variable names SHOULD NOT be compound words,
  separated by underscores, except in cases where this is necessary to
  disambiguate.
- Argument and variable names SHOULD NOT duplicate parts of the function name.
- Attribute names SHOULD NOT duplicate parts of the class name.
- Class names SHOULD adhere to the nomenclature guide.
- Function names SHOULD adhere to the nomenclature guide.

#### 6. Comments

- Comments that describe obvious behavior SHOULD NOT be included.
- TODO comments SHOULD be added for uncovered edge cases and future work.
- Comments MUST add meaningful context, not restate what the code does.

### Comprehensive Example: Real-World Function with Multiple Violations

Here is a function that demonstrates many compliance violations:

```python
def _group_documents_by_field(
    documents: list[ dict[ str, __.typx.Any ] ],
    field_name: __.typx.Optional[ str ]
) -> dict[ str, list[ dict[ str, __.typx.Any ] ] ]:
    ''' Groups documents by specified field for inventory format compatibility.
    '''
    if field_name is None:
        return { }

    groups: dict[ str, list[ dict[ str, __.typx.Any ] ] ] = { }
    for doc in documents:
        # Get grouping value, with fallback for missing field
        group_value = doc.get( field_name, f'(missing {field_name})' )
        if isinstance( group_value, ( list, dict ) ):
            # Handle complex field types by converting to string
            group_value = str( group_value )  # type: ignore[arg-type]
        elif group_value is None or group_value == '':
            group_value = f'(missing {field_name})'
        else:
            group_value = str( group_value )

        if group_value not in groups:
            groups[ group_value ] = [ ]

        # Convert document format back to inventory object format
        inventory_obj = {
            'name': doc[ 'name' ],
            'role': doc[ 'role' ],
            'domain': doc.get( 'domain', '' ),
            'uri': doc[ 'uri' ],
            'dispname': doc[ 'dispname' ]
        }
        if 'fuzzy_score' in doc:
            inventory_obj[ 'fuzzy_score' ] = doc[ 'fuzzy_score' ]
        groups[ group_value ].append( inventory_obj )
    return groups
```

Violations identified:
1. **Narrow parameter types**: `list[dict[...]]` instead of wide `__.cabc.Sequence[__.cabc.Mapping[...]]`
2. **Type suppression abuse**: `# type: ignore[arg-type]` masks real design issue
3. **Mutable container return**: Returns `dict` instead of `__.immut.Dictionary`
4. **Function body blank lines**: Empty lines breaking vertical compactness
5. **Vertical compactness**: `return { }` could be same line as `if`
6. **Unnecessary comments**: "Handle complex field types by converting to string" states obvious
7. **F-string quotes**: Using single quotes in f-strings instead of double
8. **Nomenclature duplication**: `group_value` repeats "group" from function name
9. **Underscore nomenclature**: `field_name` could be `field`, `group_value` could be `value`
10. **Mutable container creation**: Using `{ }` and `[ ]` instead of immutable alternatives
11. **Trailing comma**: Missing trailing comma in dictionary, affecting delimiter placement
12. **Single-line else**: `group_value = str(group_value)` could be same line as `else`
13. **Design pattern**: Could use `collections.defaultdict` instead of manual initialization

Corrected version:
```python
def _group_documents_by_field(
    documents: __.cabc.Sequence[ __.cabc.Mapping[ str, __.typx.Any ] ],
    field: __.typx.Absential[ str ] = __.absent,
) -> __.immut.Dictionary[
    str, tuple[ __.cabc.Mapping[ str, __.typx.Any ], ... ]
]:
    ''' Groups documents by specified field. '''
    if __.is_absent( field ): return __.immut.Dictionary( )
    groups = __.collections.defaultdict( list )
    for doc in documents:
        value = doc.get( field, f"(missing {field})" )
        if isinstance( value, ( list, dict ) ): value = str( value )
        elif value is None or value == '': value = f"(missing {field})"
        else: value = str( value )
        obj = __.immut.Dictionary(
            name = doc[ 'name' ],
            role = doc[ 'role' ],
            domain = doc.get( 'domain', '' ),
            uri = doc[ 'uri' ],
            dispname = doc[ 'dispname' ],
            **( { 'fuzzy_score': doc[ 'fuzzy_score' ] }
                if 'fuzzy_score' in doc else { } ) )
        groups[ value ].append( obj )
    return __.immut.Dictionary(
        ( key, tuple( items ) ) for key, items in groups.items( ) )
```

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

## Tool Preferences

- **Precise coordinates**: Use `rg --line-number --column` for exact line/column positions
- **File editing**: Prefer `text-editor` MCP tools for line-based edits to avoid conflicts
- **File synchronization**: Always reread files with `text-editor` tools after modifications by other tools (like `pyright` or `ruff`)
- **Batch operations**: Group related changes together to minimize file modification conflicts between different MCP tools

## Conformance Process

### 1. Analysis Phase (PHASE 1)
- Examine target files to understand current state  
- Run linters to identify specific violations
- Identify architectural patterns that need updating
- Generate comprehensive compliance report
- **Requirements**: Complete review and report before any remediation
- **Focus**: Reference specific lines with concrete examples and explain reasoning

### 2. Systematic Correction (PHASE 2)
Apply fixes in systematic order:
1. **Module Organization**: Reorder imports, type aliases, functions per practices guide
2. **Wide/Narrow Types**: Convert function parameters to wide abstract types
3. **Import Cleanup**: Remove namespace pollution, use private aliases and __ subpackage
4. **Type Annotations**: Add missing hints, create `TypeAlias` for complex types
5. **Exception Handling**: Narrow try block scope, ensure proper chaining
6. **Immutability**: Replace mutable with immutable containers where appropriate
7. **Spacing/Delimiters**: Fix `( )`, `[ ]`, `{ }` patterns
8. **Docstrings**: Triple single quotes, narrative mood, proper spacing
9. **Line Length**: Split at 79 columns using parentheses

**Requirements**: 
- Maintain exact functionality while improving standards adherence
- Validate with `hatch --env develop run linters` (must produce clean output)
- Run `hatch --env develop run testers` to ensure no functionality breaks

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
