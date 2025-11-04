# Template Injections vs. Examples Analysis

**Date**: 2025-11-04
**Context**: Evaluating alternative to current injectable foundational constructs in Copier template

## Executive Summary

This document analyzes shifting from conditional injection of foundational constructs (exceptions, Rust extensions) to an example-based model where users copy and rename template code. The primary motivation is reducing merge conflicts during template updates.

**Key Finding**: The example-based approach is architecturally sound and solves the merge conflict problem, but trades immediate usability for long-term flexibility. Recommendation varies by feature type—Rust extensions are strong candidates for examples, while basic exceptions may benefit from a hybrid approach.

## Current State

### How Injection Currently Works

1. **Conditional file creation**: Files like `exceptions.py` only created when `inject_exceptions: true`
2. **Conditional imports**: `__init__.py` conditionally imports via Jinja markers
3. **Binary decision**: Either you get the foundation code or you don't
4. **Update model**: Template updates can cause merge conflicts in customized injected files

### Current Injectable Features

- **Foundational Constructs** (`inject_foundations`)
  - Base exceptions (`inject_exceptions`): `exceptions.py` with `Omniexception` and `Omnierror`

- **Rust Extensions** (`enable_rust_extension`)
  - Complete crate structure: `Cargo.toml`, `build.rs`, `src/lib.rs`
  - PyO3 bindings boilerplate
  - Test integration

## Strengths of Example-Based Approach

### 1. Reduced Merge Conflicts
Once users copy and rename examples, those files become entirely theirs—future template updates won't touch them. This directly addresses the primary pain point.

### 2. Clearer Ownership Boundaries
Clear distinction between "template-provided examples" and "user's production code." No ambiguity about file ownership.

### 3. Flexibility
Users can copy, modify, and mix-and-match patterns without being locked into template structure.

### 4. Multiple Variations
Could provide multiple example patterns:
- `exceptions_simple.py.example`
- `exceptions_rich.py.example`
- `exceptions_hierarchy.py.example`

Shows different approaches rather than forcing one.

### 5. Lower Barrier to Customization
Users don't feel like they're "fighting the template"—they simply choose not to copy examples or heavily modify them.

## Weaknesses and Concerns

### 1. Discoverability Problem

**Issue**: Examples outside active code are easy to forget or overlook.

**Consequences**:
- Users might not realize examples exist
- Examples might become stale if not tested
- Documentation burden increases

**Mitigation Strategies**:
- Place examples in highly visible location (`examples/` at project root)
- Generate README in examples directory
- Add comments in `__init__.py` pointing to relevant examples
- Mention examples prominently in project README

### 2. Testing and Linting Exclusion

**Challenge**: Examples must be:
- Valid Python syntax (for IDE support)
- Not imported anywhere (to avoid affecting package)
- Excluded from coverage, linting, type checking
- Kept in sync with best practices

**Implementation Options**:

#### Option A: Non-Python Extension
```
examples/
  foundations/
    exceptions.py.example
    rich_exceptions.py.example
  rust_extension/
    lib.rs.example
```

- **Pros**: Simple, clearly not executable code
- **Cons**: No syntax highlighting, no IDE help, manual rename required

#### Option B: Separate Directory with Exclusions
```
examples/
  __init__.py  # Empty or raises NotImplementedError
  foundations/
    exceptions.py
    rich_exceptions.py
```

Configure exclusions in `pyproject.toml`:
```toml
[tool.coverage.run]
omit = ["examples/*"]

[tool.pyright]
exclude = ["examples"]

[tool.ruff]
exclude = ["examples"]
```

- **Pros**: Real Python files with full IDE support, easy to copy-paste
- **Cons**: More configuration complexity, risk of accidental import

#### Option C: Documentation Examples
```
documentation/examples/
  exceptions.rst
    .. code-block:: python
       # Full working example
```

- **Pros**: Naturally separated, can include extensive explanation
- **Cons**: Less convenient to copy, harder to maintain variations

**Recommendation**: Option B provides best developer experience while maintaining clear boundaries.

### 3. Boilerplate Burden

**Issue**: With injection, users get working code immediately. With examples, every project requires:
1. Deciding which examples to use
2. Copying files
3. Renaming symbols to match package
4. Updating imports
5. Customizing to needs

**When This Matters**:
- Truly foundational patterns used identically by 95% of projects
- Patterns with significant boilerplate (Rust extensions)

**When This Doesn't Matter**:
- Optional features with high variation
- Advanced patterns sophisticated users will customize anyway

### 4. The Rename Problem

**Issue**: Examples work generically but users must rename symbols.

Example:
```python
# examples/foundations/exceptions.py
class Omniexception(BaseException):
    """Base for all exceptions."""
    pass

# User copies to mypackage/exceptions.py
# Still says "Omniexception"—should rename to MyPackageError
```

**Mitigation Options**:
- Use obviously-generic names (`ExampleBaseException`) signaling "rename me"
- Provide renaming instructions in comments
- Accept that power users will handle this
- Use hybrid approach (see below)

## Hybrid Approaches

### Hybrid 1: Starter + Examples

**Keep injection for absolute basics**, provide examples for variations:

- `inject_foundations: true` → Minimal `exceptions.py` with `Omniexception`/`Omnierror`
- `examples/foundations/` → Rich variations showing advanced patterns

**Rationale**:
- 90% of projects need basic exceptions → reduce toil
- Advanced users consult examples for inspiration
- Minimal merge conflict surface (basic exceptions rarely change)

### Hybrid 2: Conditional Examples

Examples generated only when feature is **disabled**:

```jinja
{% if not inject_exceptions %}
{# Generate examples/foundations/exceptions.py.example %}
{% else %}
{# Generate sources/{{ package_name }}/exceptions.py %}
{% endif %}
```

**Rationale**: First-time users get working injection, sophisticated users disabling injection get examples

**Problem**: Users wanting both injection and examples to study don't get examples

### Hybrid 3: Always Include Examples, Injection Controls Integration

```
template/
  sources/{{ package_name }}/
    {% if inject_exceptions %}exceptions.py{% endif %}
  examples/
    foundations/
      exceptions_basic.py     # What gets injected
      exceptions_rich.py      # Advanced variation
      exceptions_custom.py    # Another pattern
```

**Rationale**:
- Examples always available for reference
- Injection controls whether code is part of package
- Users can start with injection, later copy examples for customization
- Examples serve as documentation and inspiration

**Assessment**: This is the safest migration path.

## Application to Rust Extensions

### Why Rust Extensions Are Strong Candidates for Examples

**Strengths**:
1. **High Customization Likelihood**: Extensions are usually non-trivial and project-specific
2. **Complex Configuration**: Cargo.toml, build.rs, PyO3 bindings—lots to customize
3. **Learning Opportunity**: Can show multiple patterns (FFI styles, PyO3 features, async)
4. **Target Audience**: Users needing Rust extensions are sophisticated enough to handle copying

**Weaknesses**:
1. **Significant Boilerplate**: Setting up working extension is non-trivial
2. **Build System Integration**: pyproject.toml needs maturin/setuptools-rust config
3. **Testing Complexity**: Cross-language testing requires specific setup

**Recommendation**: Strong candidate for example-based approach due to high expected customization and sophisticated target audience.

### Possible Rust Extension Examples Structure

```
examples/
  rust_extension/
    README.md  # Explains different patterns
    minimal_ffi/
      Cargo.toml
      build.rs
      src/lib.rs
    pyo3_standard/
      Cargo.toml
      src/lib.rs
    pyo3_async/
      Cargo.toml
      src/lib.rs
```

## Recommendations

### Recommendation 1: Tiered Approach Based on Universality

**Keep injection for truly foundational, rarely-customized patterns**:
- Basic exception hierarchy (if 90%+ of projects use identically)

**Move to examples for high-customization features**:
- Rust extensions
- Advanced exception patterns
- CLI patterns beyond basics
- Future optional complex features

**Rationale**: Balance between reducing toil (injection for universals) and reducing merge conflicts (examples for customized features).

### Recommendation 2: If Going Full Example-Based, Use Option B

Implementation structure:
```
examples/
  README.md  # Describes available examples and usage
  __init__.py  # Empty or raises helpful error
  foundations/
    __init__.py
    exceptions_basic.py      # Minimal pattern
    exceptions_rich.py       # With attribute concealment
    exceptions_hierarchy.py  # Complex hierarchy
  rust_extension/
    __init__.py
    minimal_ffi/
      Cargo.toml
      build.rs
      src/lib.rs
    pyo3_full/
      Cargo.toml
      src/lib.rs
```

Required configuration:
```toml
# pyproject.toml
[tool.coverage.run]
omit = ["examples/*"]

[tool.pyright]
exclude = ["examples"]

[tool.ruff]
exclude = ["examples"]
```

Discoverability enhancements:
- Template README mentions examples prominently
- Comments in `__init__.py` pointing to relevant examples
- Examples include inline instructions for copying/renaming
- Each example directory has README explaining the pattern

### Recommendation 3: Migration Path with Validation

Phased approach to validate hypothesis:

**Phase 1**: Add examples directory alongside existing injection (Hybrid 3)
- No breaking changes
- Users can experiment with examples
- Gather usage data

**Phase 2**: Monitor which examples are used vs. injection
- Track template usage patterns
- Survey users about preferences
- Identify which patterns get customized

**Phase 3**: Deprecate injection for patterns where examples prove sufficient
- Announce deprecation with migration guide
- Maintain both for one major version

**Phase 4**: Remove injection for those patterns
- Clean removal after validation

**Benefit**: Validates hypothesis with real usage data before committing to breaking changes.

## Decision Framework

### Questions to Guide Decision

1. **What percentage of users customize injected foundations?**
   - If <10%: Keep injection (merge conflicts rare)
   - If 10-50%: Consider hybrid approach
   - If >50%: Move to examples (merge conflicts common)

2. **How sophisticated is target audience?**
   - Beginners: Prefer injection (less toil)
   - Mixed: Hybrid approach
   - Experts: Prefer examples (more control)

3. **How stable are foundational patterns?**
   - Stable: Injection acceptable (merge conflicts rare even if customized)
   - Evolving: Examples better (reduce pain during evolution)

4. **How much variation do you want to show?**
   - Single canonical pattern: Injection fine
   - Multiple valid approaches: Examples shine

### Feature-Specific Assessments

| Feature | Customization Likelihood | Target Audience | Recommendation |
|---------|-------------------------|-----------------|----------------|
| Basic Exceptions | Low-Medium | All users | Keep injection or Hybrid 1 |
| Advanced Exceptions | High | Power users | Examples |
| Rust Extensions | Very High | Expert users | Examples (strong candidate) |
| CLI Patterns | Medium | Mixed | Evaluate case-by-case |

## Conclusion

The example-based approach is **architecturally sound** and **solves the merge conflict problem**. However, it trades immediate usability for long-term flexibility.

**For Rust extensions specifically**: Strong recommendation to move to examples due to:
- High expected customization
- Sophisticated target audience
- Opportunity to show multiple valid patterns
- Complex boilerplate that benefits from documentation

**For basic exceptions**: Recommend gathering data on actual customization frequency before abandoning injection. Consider Hybrid 1 (minimal injection + rich examples) or Hybrid 3 (always provide examples, injection controls integration).

**Overall recommended approach**: Hybrid 3 with phased migration. This provides:
- Safety: No immediate breaking changes
- Flexibility: Both patterns available
- Data: Real usage informs future decisions
- Migration path: Clear evolution strategy

The key is matching the approach to each feature's actual customization patterns rather than applying one model universally.
