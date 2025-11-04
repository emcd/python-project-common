# Import Cascades and Exception Patterns

## Overview

This document explains how imports cascade through the package hierarchy and how exception classes should be defined and accessed throughout the codebase.

## Core Principles

1. **Internals Independence**: The `__` (internals) package must NEVER import from other parts of the package. It provides foundational utilities that the rest of the package depends on.

2. **Cascading Through `__` Modules**: Each subpackage has a `__.py` re-export module that imports from its parent's `__` module using `from ..__ import *`. This creates an inheritance chain.

3. **Exception Placement**: Exceptions should be defined at the most specific scope where they are needed. If an exception is only used in one subpackage, define it there.

4. **No Parent Package Imports**: Regular modules within a subpackage should NEVER import from parent packages using `from .. import` or `from ... import`. They should only use local imports (`from . import`) or reference items through the `__` namespace.

## Exception Definition Patterns

### Base Exception Classes

Base exception classes are defined in `sources/aiwb/exceptions.py`:

```python
class Omniexception( __.immut.Object, BaseException ):
    ''' Base for all exceptions raised by package API. '''

class Omnierror( Omniexception, Exception ):
    ''' Base for error exceptions raised by package API. '''

class SupportError( Omnierror, NotImplementedError ):
    ''' Attempt to use implementation which is not available. '''
```

### Package-Level Exceptions

Each major package can have its own `exceptions.py` module for exceptions used across that package:

```python
# sources/aiwb/controls/exceptions.py
from . import __

class ControlValueMisclassification( __.Omnierror, TypeError ):
    ''' Control value has incorrect type. '''

    def __init__( self, control_name: str, expected_type: str, actual_type: str ):
        super().__init__(
            f"Control '{control_name}' expected {expected_type}, "
            f"got {actual_type}." )
```

### Subpackage-Level Exceptions

For exceptions used only in a specific subpackage, define them locally:

```python
# sources/aiwb/invocables/ensembles/probability/exceptions.py
from . import __

class DiceSpecificationInvalidity( __.Omnierror, ValueError ):
    ''' Invalid dice specification format or constraints. '''

    def __init__( self, specification: str, issue: str ):
        super().__init__(
            f"Invalid dice specification {specification!r}: {issue}." )
```

## Import Cascade Mechanics

### The `__` Module Chain

Each subpackage's `__.py` module establishes the inheritance chain:

```python
# sources/aiwb/controls/__.py
from ..__ import *              # Inherits from parent internals
from ..exceptions import *      # Makes base exceptions available

# sources/aiwb/invocables/__.py
from ..__ import *              # Inherits from parent internals
from ..exceptions import *      # Makes base exceptions available

# sources/aiwb/invocables/ensembles/__.py
from ..__ import *              # Inherits everything from invocables.__
                                # (including exceptions, no need to re-import)

# sources/aiwb/invocables/ensembles/probability/__.py
from ..__ import *              # Inherits everything from ensembles.__
                                # (including exceptions through the chain)
```

### Why This Works

1. Top-level packages import exceptions: `from ..exceptions import *`
2. Child packages inherit through `__`: `from ..__ import *`
3. Grandchild packages inherit the full chain: `from ..__ import *`

This means `Omnierror` is available as `__.Omnierror` at any depth without needing to re-import from the top-level exceptions module.

### Exception Module Access Patterns

**CORRECT - Local import pattern:**
```python
# sources/aiwb/controls/core.py
from . import __
from . import exceptions as _exceptions

if invalid:
    raise _exceptions.ControlValueMisclassification( name, expected, actual )
```

**CORRECT - For provider clients accessing cascaded exceptions:**
```python
# sources/aiwb/providers/clients/openai/conversers.py
from . import __

if error:
    raise __.ProviderCredentialsInavailability( 'openai', 'OPENAI_API_KEY' )
```

**WRONG - Parent package import:**
```python
# sources/aiwb/controls/core.py
from . import __
from .. import exceptions as _exceptions  # ❌ WRONG - parent import

if invalid:
    raise _exceptions.ControlValueMisclassification( name, expected, actual )
```

**WRONG - Multi-level parent import:**
```python
# sources/aiwb/invocables/ensembles/probability/calculations.py
from . import __
from ...exceptions import DiceSpecificationInvalidity  # ❌ WRONG - spaghetti

if invalid:
    raise DiceSpecificationInvalidity( dice, "invalid" )
```

## Exception Cascading in Subpackages

Some subpackages need to cascade their parent's exceptions to their modules. This is done in the `__.py` module:

```python
# sources/aiwb/providers/clients/__.py
from ..__ import *              # Inherit parent internals
from .._api import *            # Inherit parent API types
from ..exceptions import *      # CASCADE parent exceptions

# Now client modules can access provider exceptions via __
# sources/aiwb/providers/clients/anthropic/clients.py
from . import __

raise __.ProviderCredentialsInavailability( 'anthropic', api_key_name )
```

For deeply nested packages, cascading happens automatically through the `from ..__ import *` chain.

## Checklist for Adding New Exceptions

1. **Determine Scope**: Where is this exception used?
   - One module only? Consider inline definition or local exceptions module
   - Across a subpackage? Create/use subpackage exceptions.py
   - Across the package? Use top-level package exceptions.py

2. **Create Exception Class**:
   - Inherit from `__.Omnierror` (or other `__.Omni*` base) FIRST
   - Then inherit from appropriate stdlib exception
   - Use semantic constructor parameters, not pre-formatted strings
   - Name without "Error" suffix (e.g., `ControlValueMisclassification` not `ControlValueMisclassificationError`)

3. **Import Pattern**:
   - Exception module: `from . import __`
   - Using module: `from . import exceptions as _exceptions`
   - Access: `_exceptions.YourException()` or `__.YourException()` if cascaded

4. **Update `__.py` if Needed**:
   - Top-level packages need `from ..exceptions import *`
   - Deeply nested packages inherit automatically
   - Check if exceptions are accessible where needed

5. **Test**:
   - Verify application runs: `hatch run aiwb-application inspect configuration`
   - Check linters: `hatch --env develop run ruff check --select TRY,E501 sources/aiwb/`

## Common Pitfalls

1. **Importing base exceptions into `__` internals package**: The internals package (`sources/aiwb/__/`) should NEVER import from `..exceptions`. Base exceptions should cascade down, not up.

2. **Using multi-dot parent imports**: Never use `from ... import` or `from .... import` in regular modules. Use local imports or access through `__`.

3. **Forgetting to add exception import to top-level packages**: Each major package needs `from ..exceptions import *` in its `__.py` to make base exceptions available.

4. **String literals in exception raises**: Use semantic constructor parameters, not pre-formatted strings, to satisfy TRY003 linter requirements.

5. **Creating monolithic exception classes**: Split complex exceptions with multiple conditional logic paths into focused, specific exception classes.

## References

- See `.auxiliary/notes/exception-design-analysis.md` for detailed exception class specifications
- See `.auxiliary/instructions/practices-python.rst` for general Python coding practices
- All exception changes must pass: `hatch --env develop run ruff check --select TRY sources/aiwb/`
