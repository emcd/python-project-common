.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+


*******************************************************************************
002. Centralized Import Management via __ Subpackage Pattern
*******************************************************************************

Status
===============================================================================

Accepted

Context
===============================================================================

Python projects generated from this template need consistent import management across modules to address several challenges:

**Namespace Pollution**: Individual modules importing common dependencies directly leads to namespace pollution and makes module interfaces unclear.

**Import Duplication**: Common imports (collections.abc, immutable containers, type hints) are repeated across many modules, creating maintenance overhead.

**Performance Considerations**: Repeated import costs across modules can impact package initialization time.

**Maintenance Overhead**: Changes to common dependencies require updates across multiple modules.

**Code Readability**: Module code becomes cluttered with import statements rather than focusing on core functionality.

The template system must provide a scalable solution that works consistently across:
- Single-package projects
- Multi-package projects with subpackages  
- Projects with varying complexity levels
- Projects using different optional features (CLI, Rust extensions, etc.)

Decision
===============================================================================

Implement centralized import management using the double underscore (``__``) subpackage pattern:

**Core Implementation**:
- Every Python package includes a ``__`` subdirectory
- Contains ``__init__.py`` (re-exports), ``imports.py`` (raw imports), ``nomina.py`` (naming constants)
- All modules use identical ``from . import __`` import pattern

**Hierarchical Extension**:
- Subpackages implement cascading imports with ``from ..__ import *``
- Each level can add specialized imports without duplicating parent imports
- Maintains consistent interface regardless of package depth

**Template Integration**:
- Template system generates appropriate ``__`` structure based on project features
- Optional components (CLI, Rust, etc.) extend the import hierarchy as needed
- Standard imports are pre-configured for immediate development productivity

Alternatives
===============================================================================

**Direct Module Imports**
- Each module imports dependencies directly
- Rejected due to namespace pollution and maintenance overhead
- Would require updating every module when common dependencies change
- Creates inconsistent import patterns across project modules

**Package-Level __init__.py Imports**
- Central imports at package ``__init__.py`` level
- Rejected because it pollutes the main package namespace
- Makes it unclear which imports are part of the public API vs internal dependencies
- Doesn't scale well to multi-package projects

**Import Utility Module**
- Single ``imports.py`` or ``utils.py`` module with all dependencies
- Rejected because it creates a monolithic import module that becomes unwieldy
- Doesn't provide clear organization for different types of imports
- No natural extension pattern for subpackages

**Per-Module Import Files**
- Each module has an associated ``_imports.py`` file
- Rejected due to file proliferation and maintenance complexity
- Creates 2x file count for every functional module
- No clear inheritance pattern for shared imports

Consequences
===============================================================================

**Positive Consequences**

**Consistent Interface**: All modules use identical ``from . import __`` regardless of package depth or complexity, reducing cognitive load.

**Namespace Clarity**: Module namespaces contain only module-specific functionality, making interfaces clearer and more maintainable.

**Maintenance Efficiency**: Common import changes propagate automatically to all modules without requiring individual module updates.

**Performance Optimization**: Import costs are centralized to package initialization, enabling strategic optimization for performance-critical paths.

**Scalability**: Pattern extends naturally from simple single-package projects to complex multi-package hierarchies without changing the interface.

**Template Flexibility**: Template system can generate appropriate import structures based on selected features without affecting module code patterns.

**Negative Consequences**

**Learning Curve**: Developers unfamiliar with the pattern require education about the import hierarchy and naming conventions.

**Initial Setup Complexity**: Each package requires proper ``__`` subpackage setup, though this is handled by the template system.

**Import Resolution Indirection**: Imports go through an additional layer of indirection, though this is minimal performance impact.

**Debugging Complexity**: Import-related debugging requires understanding the cascading import hierarchy.

**Neutral Consequences**

**File Structure Overhead**: Each package contains additional ``__`` subdirectory structure, but this is consistent and predictable.

**IDE Integration**: Modern IDEs handle the import pattern well, providing proper autocompletion and navigation through the import hierarchy.

**Convention Enforcement**: Pattern requires discipline to maintain, but template system and documentation provide clear guidance.