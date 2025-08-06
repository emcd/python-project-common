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
Architecture Documentation
*******************************************************************************

This guide covers architectural documentation practices, including
architectural decision records (ADRs) and design documentation standards.

Architectural Decision Records
===============================================================================

Architectural Decision Records (ADRs) document the significant architectural
decisions made during the project lifecycle. They capture the context,
reasoning, and consequences of decisions to provide future teams with the
rationale behind architectural choices.

Purpose and Benefits
-------------------------------------------------------------------------------

* **Historical context**: Preserve the reasoning behind architectural decisions
  for future reference and team onboarding.

* **Decision accountability**: Create a clear record of who made decisions and
  under what circumstances.

* **Alternative exploration**: Document what was considered but not chosen,
  providing valuable context for future architectural reviews.

* **Change management**: Track the evolution of architectural decisions over
  time through status updates and supersession.

ADR Format
-------------------------------------------------------------------------------

Use the following format for all architectural decision records:

.. code-block:: rst

    *******************************************************************************
    [Number]. [Title]
    *******************************************************************************

    Status
    ===============================================================================

    [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

    Context
    ===============================================================================

    [Describe the forces at play, constraints, and business/technical situation
    that led to this decision. What problem are we trying to solve? What are the
    key requirements and limitations?]

    Decision
    ===============================================================================

    [State the decision clearly and concisely. This should be the response to the
    forces described in the Context section.]

    Alternatives
    ===============================================================================

    [Document what other options were considered and why each was rejected. This
    provides valuable context for future decisions and shows that alternatives
    were properly evaluated.]

    Consequences
    ===============================================================================

    [Describe the positive, negative, and neutral consequences of this decision.
    Be honest about trade-offs and potential risks. Include impacts on:
    - Performance
    - Maintainability
    - Team productivity
    - System complexity
    - Future flexibility]

ADR Lifecycle Management
-------------------------------------------------------------------------------

**Numbering Convention**

* Use sequential numbering: ``001-initial-architecture.rst``,
  ``002-database-selection.rst``, etc.
* Zero-pad numbers to three digits for consistent sorting.
* Use lowercase, hyphenated filenames.

**Status Workflow**

* **Proposed**: Decision is under consideration and review.
* **Accepted**: Decision has been approved and is being implemented.
* **Deprecated**: Decision is no longer relevant but kept for historical context.
* **Superseded**: Decision has been replaced by a newer ADR (reference the
  superseding ADR number).

**Immutability Principle**

* Once an ADR is accepted, do not edit its content.
* If circumstances change, create a new ADR that supersedes the previous one.
* This preserves the historical decision context and reasoning.

Best Practices
-------------------------------------------------------------------------------

**Context Documentation**

* Focus on forces and constraints that drove the decision.
* Include relevant business context, technical limitations, etc....
* Avoid implementation details - focus on the decision-making environment.

**Clear Decision Statements**

* State decisions unambiguously.
* Avoid hedging language like "might" or "could".
* Be specific about what will be done.

**Comprehensive Alternatives**

* Document all seriously considered alternatives.
* Explain why each alternative was rejected with specific reasons.
* Include "do nothing" as an alternative when relevant.

**Honest Consequences**

* Document both positive and negative consequences.
* Include trade-offs and potential risks.
* Consider long-term implications, not just immediate benefits.

Standard Filesystem Organization Patterns
===============================================================================

This section documents the standard filesystem organization patterns used
across all projects in the template system. These patterns provide consistency,
maintainability, and clear separation of concerns.

Root Directory Organization Principles
-------------------------------------------------------------------------------

**Single Sources Directory Pattern**

All source code resides in a unified ``sources/`` directory, separate from
other project artifacts:

* **Clear separation**: Source code is distinctly separated from documentation,
  tests, and configuration files
* **Build process clarity**: Build tools can target the entire source tree
  without ambiguity
* **Mixed-language support**: Multiple languages can coexist with appropriate
  subdirectories

**Top-level Structure Standards**

Essential project files remain at the top level for immediate visibility:

* ``LICENSE.txt``, ``README.rst``, ``pyproject.toml`` provide project overview
* ``documentation/`` contains all documentation source
* ``tests/`` mirrors source structure for test organization
* ``.auxiliary/`` provides development workspace (excluded from distributions)

The `__` Subpackage Pattern
-------------------------------------------------------------------------------

The double underscore (``__``) subpackage serves as a centralized import hub,
providing consistent namespace management across all project modules.

**Core Concept**

Each Python package includes a ``__`` subdirectory containing:

* ``__init__.py``: Re-exports commonly used imports
* ``imports.py``: Raw imports from external libraries
* ``nomina.py``: Project-specific naming constants and conventions

**Primary Benefits**

**Namespace Management:**
- Prevents pollution of individual module namespaces
- Provides consistent access to common dependencies
- Reduces import statement duplication and maintenance overhead

**Performance Optimization:**
- Centralizes import costs to package initialization time
- Enables strategic use of direct imports for performance-critical code
- Supports lazy loading patterns where beneficial

**Maintenance Efficiency:**
- Changes to common imports propagate automatically to all modules
- Clear separation between common and module-specific imports
- Reduces cognitive load when reading module code

**Usage Pattern**

All modules use the same import pattern regardless of package depth:

.. code-block:: python

    # In any module at any package level
    from . import __

    # Usage throughout the module
    def process_data( items: __.cabc.Sequence[ str ] ) -> __.immut.Dictionary:
        ''' Processes sequence items into immutable dictionary. '''
        return __.immut.Dictionary( processed = True, count = len( items ) )

**Cascading Import Hierarchy**

When projects grow to include subpackages, the pattern extends naturally:

**Hierarchical Inheritance:**
- Each subpackage maintains its own ``__.py`` file
- Subpackages inherit all parent imports with ``from ..__ import *``
- Each level adds specialized imports without duplicating parent imports
- Deep subpackages have access to all imports in their hierarchy

**Consistent Interface:**
- All modules use identical ``from . import __`` regardless of package depth
- New subpackages require minimal import configuration
- Subpackages automatically inherit all parent functionality

**Import Resolution Chain:**
- Nested imports resolve through the hierarchy: ``nested/__.py`` → ``parent/__.py`` → ``root/__/imports.py``
- Each level adds to the namespace without overriding parent imports
- Provides natural import scoping based on package hierarchy

**Naming Rationale**

The double underscore naming convention:

* Short and distinctive to minimize visual noise in import statements
* Uses Python's existing convention for special/internal names
* Easily distinguishable from regular module names
* Consistent across all project modules

**Subpackage Implementation Pattern**

When projects grow to include subpackages, each implements the cascading pattern:

.. code-block:: python

    # package/subpackage/__.py
    ''' Internal imports for subpackage functionality. '''

    # ruff: noqa: F403,F401

    # Additional specialized imports as needed
    import specialized_library

    from ..__ import *  # Inherit all parent imports
    from ..exceptions import *  # Package exceptions (if available)

All subpackage modules maintain the consistent interface:

.. code-block:: python

    # package/subpackage/module.py
    from . import __

    def specialized_function(
        data: __.cabc.Sequence[ __.typx.Any ]
    ) -> __.immut.Dictionary:
        ''' Processes specialized data using inherited imports. '''
        return __.immut.Dictionary( processed = True, specialized = True )

Tests Organization
-------------------------------------------------------------------------------

The test structure follows what is documented in the `tests guide
<https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/tests.rst>`_.

Data Resources Organization
-------------------------------------------------------------------------------

The ``data/`` directory contains resources which are intended to be distributed
with the package. These can include configuration templates, webapp icons,
etc....

Development Workspace
-------------------------------------------------------------------------------

Development-specific files are organized in `.auxiliary/`:

.. code-block::

    .auxiliary/
    ├── notes/                       # Development notes and TODO items
    ├── scribbles/                   # Temporary development files
    └── instructions/                # Local development guide copies

This workspace is excluded from package distributions but provides session
continuity for development tools and local documentation storage.

Architecture Documentation Beyond ADRs
===============================================================================

System Summary
-------------------------------------------------------------------------------

The system summary (``architecture/summary.rst``) should provide a high-level
overview of the system architecture including:

* **Major components**: Key system modules, services, or subsystems.
* **Component relationships**: How components interact and depend on each other.
* **Data flow**: Major data paths through the system.
* **Deployment architecture**: How components are distributed and deployed.
* **Key architectural patterns**: Major patterns employed (MVC, microservices,
  event-driven, etc.).

Filesystem Documentation
-------------------------------------------------------------------------------

The filesystem documentation (``architecture/filesystem.rst``) implements the
standard patterns documented above for the specific project configuration:

* **Project-specific structure**: Shows actual package names and
  feature-specific organization
* **Integration patterns**: Shows how optional components (CLI, Rust
  extensions, etc.) integrate with the standard structure

Design Documents
-------------------------------------------------------------------------------

Detailed design documents (under ``architecture/designs/``) capture
implementation-level specifications:

* **Interface specifications**: API contracts, service interfaces, module APIs.
* **Data schemas**: Database schemas, message formats, configuration structures.
* **Algorithm specifications**: Detailed algorithmic approaches for complex
  processing.
* **Protocol definitions**: Communication protocols between components.

**Design Document Guidelines**

* Reference the architectural decisions that informed the design.
* Include enough detail for implementation without over-specifying.
* Use diagrams and examples to illustrate complex concepts.
* Version design documents when significant changes occur.
