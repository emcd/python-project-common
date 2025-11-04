# Foundation Injection Enhancement Plan

**Date**: 2025-11-04
**Context**: Enhancing foundation injection to use immutable exceptions and include common dependencies

## Background

We want to update the injected `Omniexception` base class to inherit from `__.immut.exceptions.Omniexception` (provided by the `frigid` package) to enforce class and instance immutability. However, this creates a bootstrapping problem for foundation packages like `frigid`, `absence`, and `classcore` that cannot depend on themselves or their dependents.

### Key Insight

Merge conflicts with injected exceptions have not been a problem in practice. Most customization of `exceptions.py` is **additive** (adding project-specific exception subclasses), which doesn't conflict with template updates to the base `Omniexception`/`Omnierror` classes.

### Current State

- `inject_foundations`: Boolean flag that gates `inject_exceptions`
- `inject_exceptions`: When enabled, creates `exceptions.py` with plain `Omniexception` and `Omnierror` classes
- Currently NOT used in any template files directly, only in `copier.yaml` as a conditional

## Proposed Approach

### 1. Update Foundation Injection Behavior

When `inject_foundations: true`:
- **Add default dependencies**: `frigid`, `absence`, `dynadoc`
- **Inject immutable exceptions**: Subclass `Omniexception` from `__.immut.exceptions.Omniexception`

### 2. Disable Foundation Injection for Foundation Packages

Foundation packages that cannot have these dependencies:
- `classcore` - Provides base object system (already has `inject_foundations: false`)
- `frigid` - Provides immutability (currently has `inject_foundations: true` - needs update)
- `absence` - Provides absence sentinel (needs verification and possible update)
- `accretive` - Sister package to frigid (needs verification and possible update)

### 3. Rationale for This Approach

**Why this is pragmatic**:
- Only 3-4 packages need special treatment (foundation layer)
- The vast majority of projects are application-level and benefit from immutable exceptions
- We already manually add `frigid`, `absence`, and `dynadoc` to most projects—automating reduces toil
- Merge conflicts have not been a problem in practice
- Simple implementation with clear mental model

**When this works well**:
- ✅ Most projects (>80%) are application-level and use these dependencies
- ✅ Base exception classes in template rarely change (merge conflicts rare)
- ✅ New foundation packages created infrequently
- ✅ Template primarily for our ecosystem

## Implementation Tasks

### Task 1: Update copier.yaml

#### Update inject_foundations

```yaml
inject_foundations:
    type: bool
    help: |
        Include foundational constructs (base exceptions using immutable patterns).

        Dependencies added: frigid, absence, dynadoc

        Set to FALSE for foundation packages that cannot depend on these:
        - classcore (provides base object system)
        - frigid (provides immutability)
        - absence (provides absence sentinel)
        - accretive (sister package to frigid)
    default: false
```

#### Update inject_exceptions (keep as-is)

```yaml
inject_exceptions:
    type: bool
    help: 'Include base exceptions for package?'
    when: "{{ inject_foundations }}"
    default: false
```

### Task 2: Update pyproject.toml.jinja

Add conditional dependencies when `inject_foundations: true`:

```toml
dependencies = [
    "python >= 3.10",
    {% if inject_foundations %}
    "absence >= 0.3",  # Absence sentinel
    "dynadoc >= 0.3",  # Dynamic documentation
    "frigid >= 0.15",  # Immutable data structures
    {% endif %}
    # ... other dependencies
]
```

**Note**: Verify current minimum versions for these packages.

### Task 3: Update sources/{{ package_name }}/__/imports.py.jinja

Ensure frigid is aliased to `immut` when foundations are injected:

```python
{% if inject_foundations %}
import frigid as immut
{% endif %}
```

**Note**: Verify current import structure and integrate appropriately with existing import cascade pattern.

### Task 4: Update exceptions.py.jinja

Update to inherit from immutable base:

```python
# template/sources/{{ package_name }}/{% if inject_exceptions %}exceptions.py{% endif %}.jinja

''' Family of exceptions for package API. '''

from . import __


class Omniexception(__.immut.exceptions.Omniexception):
    ''' Base for all exceptions raised by package API. '''


class Omnierror(Omniexception, Exception):
    ''' Base for error exceptions raised by package API. '''

    def render_as_markdown(self) -> tuple[str, ...]:
        ''' Renders exception as Markdown lines for display. '''
        return (f"❌ {self}",)
```

**Note**: Review if `render_as_markdown()` should be included in base or if it's project-specific.

### Task 5: Update Foundation Packages

For packages that must disable foundation injection:

#### frigid
- Update `.auxiliary/configuration/copier-answers.yaml`
- Set `inject_foundations: false`
- Set `inject_exceptions: false`
- Keep existing hand-crafted `exceptions.py`

#### absence
- Verify current copier answers
- Update if needed: `inject_foundations: false`, `inject_exceptions: false`

#### accretive
- Verify current copier answers
- Update if needed: `inject_foundations: false`, `inject_exceptions: false`

#### classcore
- Already has `inject_foundations: false` ✅
- No changes needed

### Task 6: Documentation

Update template README to explain foundation injection:

```markdown
## Foundation Injection

The template can inject foundational constructs including:
- Base exception classes (`Omniexception`, `Omnierror`) with immutability
- Common dependencies: `frigid`, `absence`, `dynadoc`

**For most projects**: Enable `inject_foundations: true` and `inject_exceptions: true`

**For foundation packages** (classcore, frigid, absence, accretive):
- Set `inject_foundations: false`
- These packages provide foundational constructs and cannot depend on themselves
```

## Verification Steps

After implementation:

1. **Test new project generation**:
   - Generate test project with `inject_foundations: true`
   - Verify dependencies added to `pyproject.toml`
   - Verify `exceptions.py` uses `__.immut.exceptions.Omniexception`
   - Verify imports in `__/imports.py` include `frigid as immut`

2. **Test foundation package updates**:
   - Run `copier update` on frigid with `inject_foundations: false`
   - Verify no conflicts, no unwanted changes
   - Repeat for absence, accretive if applicable

3. **Test existing project updates**:
   - Run `copier update` on an existing project like agentsmgr
   - Verify smooth merge or identify expected conflicts
   - Document any manual migration steps needed

## Migration Notes

### For Existing Projects

When existing projects update to the new template version:

**If they had `inject_exceptions: true`**:
- Will need to update `exceptions.py` base class inheritance
- Will need to ensure `frigid as immut` import exists
- Dependencies will be automatically added

**Migration steps**:
1. Accept template updates to `pyproject.toml` (adds dependencies)
2. Accept template updates to `__/imports.py` (adds frigid import)
3. Review `exceptions.py` changes:
   - Base class changes from plain to `__.immut.exceptions.Omniexception`
   - Custom exception subclasses should merge cleanly (additive changes)

**If they had `inject_exceptions: false`**:
- No changes needed
- Can optionally enable foundations if desired

### For Foundation Packages

1. **Before template update**: Set `inject_foundations: false` in copier answers
2. **Run template update**: Should see no changes to exceptions or dependencies
3. **Verify**: Existing hand-crafted code remains untouched

## Open Questions

1. **Dependency versions**: What are the current minimum versions for `frigid`, `absence`, `dynadoc`?

2. **Import cascade structure**: What is the current pattern in `__/imports.py`? How should frigid import be integrated?

3. **render_as_markdown()**: Should this method be in the base `Omnierror` template, or is it project-specific?

4. **accretive and absence status**: Do these packages currently have foundation injection enabled? Need to verify their copier answers.

5. **Other common dependencies**: Are there other packages besides `frigid`, `absence`, `dynadoc` that should be added as defaults?

## Success Criteria

- ✅ New projects with `inject_foundations: true` get immutable exceptions and common dependencies
- ✅ Foundation packages (frigid, absence, accretive, classcore) can disable injection cleanly
- ✅ Existing projects can update with minimal conflicts
- ✅ Documentation clearly explains when to enable/disable foundations
- ✅ All verification tests pass

## Future Considerations

- Monitor merge conflicts over time to validate assumption they remain rare
- If conflicts become problematic, consider adding example-based escape hatch
- Consider whether other foundational constructs should be injected in future
