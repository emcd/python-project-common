---
allowed-tools: Bash(hatch --env develop run:*), Bash(git status), Bash(git log:*), Bash(echo:*), Bash(ls:*), Bash(find:*), LS, Read, Glob, Grep, Write, Edit, MultiEdit, WebFetch
description: Write comprehensive tests following project testing guidelines and improve coverage
---

# Write Tests

**NOTE: This is an experimental workflow! If anything seems unclear or missing,
please stop for consultation with the user.**

For systematic test creation following project testing guidelines and conventions.

Test requirements: `$ARGUMENTS`

**CRITICAL**: Apply project testing principles consistently.
**HALT if**:
- No test requirements are provided
- Target code cannot be analyzed
- Testing principles would be violated

## Context

- Current git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Current test coverage: !`hatch --env develop run coverage report --skip-covered || echo "No coverage data available"`
- Existing test structure: !`find tests -name "*.py" | head -20`
- Test README: !`ls tests/README.md 2>/dev/null && echo "Present" || echo "Missing"`

## Prerequisites

Ensure that you:
- have verified access to / read target code modules
- understand what specific tests need to be written
- have read any relevant `CLAUDE.md` file
- understand the [test-writing
  guidelines](https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/tests.rst).

## Testing Principles (from project guidelines)

**Core Principles:**
1. **Dependency Injection Over Monkey-Patching**: Use injectable dependencies
   for testability
2. **Performance-Conscious**: Prefer in-memory filesystems (pyfakefs) over temp
   directories
3. **Avoid Monkey-Patching**: Never patch internal code; use dependency
   injection instead
4. **100% Coverage Goal**: Aim for complete line and branch coverage
5. **Test Behavior, Not Implementation**: Focus on observable behavior and
   contracts

**Anti-Patterns to Avoid:**
- Monkey-patching internal code (will fail with immutable objects)
- Excessive mocking of internal components
- Testing implementation details vs. behavior
- Using temp directories when pyfakefs suffices

**Organization:**
- Follow the systematic numbering conventions detailed in the test guidelines

## Safety Requirements

**CRITICAL**: You MUST halt the process and consult with the user if ANY of the
following occur:

- **Anti-Pattern Detection**: If proposed tests violate project principles
- **Coverage Regression**: If tests would reduce existing coverage
- **Architecture Conflicts**: If tests require monkey-patching internal code
- **Numbering Conflicts**: If test numbering clashes with existing conventions
- **Missing Dependencies**: If required test fixtures or dependencies are
  unavailable

**Your responsibilities:**
- Follow project style and test-writing conventions exactly.
- Use dependency injection patterns consistently.
- Prefer pyfakefs for filesystem operations.
- Maintain systematic test numbering.
- Ensure tests validate behavior, not implementation.

## Test Writing Process

Execute the following steps for test requirements: `$ARGUMENTS`

### 0. Pre-Flight Verification
**MANDATORY - Verify access to test-writing guide:**

Use WebFetch to access and confirm you can read the complete testing
guidelines:
https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/tests.rst

**CRITICAL**: You MUST successfully access and read the guide before
proceeding. If WebFetch fails, HALT and consult with the user.

### 1. Code Analysis Phase
Examine the target code to understand testing needs:

**Check for existing related tests to avoid duplication:**
- Search for existing test files covering target modules
- Review test coverage reports for current state
- Identify gaps rather than recreating existing tests

**For each target file:**
- Read the source code to understand public API
- Identify functions/classes that need testing
- Note dependency injection points
- Check for existing test coverage gaps

### 2. Test Structure Planning
Determine appropriate test organization and categories:

**Review existing test structure and plan test numbering following project conventions.**

**If tests/README.md is missing, create it with:**
- Test module numbering scheme specific to the package
- Rationale for any use of patch or other exceptions to standard patterns
- Project-specific testing conventions and fixtures

**Test Categories to Include:**
- **Basic Functionality Tests (000-099):** Happy path scenarios, input validation, basic error conditions
- **Feature-Specific Tests (100+ blocks):** Each public function/class gets its own 100-block with normal usage patterns, edge cases, and error handling
- **Integration Tests (higher numbers):** Cross-module interactions and end-to-end workflows

### 3. Test Implementation
Create tests following project conventions:

**Key Implementation Guidelines:**
- Use dependency injection for all external dependencies
- Prefer `pyfakefs.Patcher()` for filesystem operations
- Mock only third-party services, never internal code
- Include docstrings explaining what behavior is tested
- Follow existing naming conventions and code style

### 5. Coverage Validation
Verify tests improve coverage without regressions:
```bash
hatch --env develop run testers
hatch --env develop run coverage report --show-missing
```

**CRITICAL - VERIFY COVERAGE IMPROVEMENT:**
- Run full test suite to ensure no regressions
- Check that new tests increase overall coverage
- Verify no existing functionality is broken
- Confirm tests follow project numbering conventions

### 6. Code Quality Validation
Ensure tests meet project standards:
```bash
hatch --env develop run linters
```

**Requirements:**
- All linting checks must pass
- No violations of project coding standards
- Test docstrings are clear and descriptive
- Proper imports and dependencies

## Test Pattern Examples

**Dependency Injection Pattern:**
```python
async def test_100_process_with_custom_processor( ):
    ''' Process function accepts custom processor via injection. '''
    def mock_processor( data ):
        return f"processed: {data}"

    result = await process_data( "test", processor = mock_processor )
    assert result == "processed: test"
```

**Filesystem Operations (Preferred):**
```python
def test_200_config_file_processing( ):
    ''' Configuration files are processed correctly. '''
    with Patcher( ) as patcher:
        fs = patcher.fs
        fs.create_file( '/fake/config.toml', contents = '[section]\nkey="value"' )

        result = process_config_file( Path( '/fake/config.toml' ) )
        assert result.key == 'value'
```

**Error Handling:**
```python
def test_300_invalid_input_handling( ):
    ''' Invalid input raises appropriate exceptions. '''
    with pytest.raises( ValueError, match = "Invalid data format" ):
        process_invalid_data( "malformed" )
```

## Success Criteria

Tests are complete when:
- [ ] Coverage has measurably improved
- [ ] All new tests pass consistently
- [ ] No existing tests are broken
- [ ] Linting passes without issues
- [ ] Tests follow project numbering conventions
- [ ] Dependency injection is used appropriately
- [ ] No monkey-patching of internal code
- [ ] Performance-conscious patterns are applied

**Note**: Always run full validation (`hatch --env develop run testers && hatch
--env develop run linters`) before considering the task complete.

## Final Report

Upon completion, provide a brief report covering:
- Coverage improvements achieved (before/after percentages)
- Any technical conflicts encountered (e.g., dataclass/protocol issues, __slots__ conflicts)
- How any conflicts were resolved or worked around
- Pragma directives applied (# pragma: no cover, # pragma: no branch) and rationale
- Any deviations from standard patterns and justification
