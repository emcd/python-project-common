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
Filesystem Organization
*******************************************************************************

This document describes the specific filesystem organization for the project,
showing how the standard organizational patterns are implemented for this
project's configuration. For the underlying principles and rationale behind
these patterns, see :doc:`../common/architecture`.

Project Structure
===============================================================================

Root Directory Organization
-------------------------------------------------------------------------------

The project implements the standard filesystem organization:

.. code-block::

    python-project-common/
    ├── LICENSE.txt              # Project license
    ├── README.rst               # Project overview and quick start
    ├── pyproject.toml           # Python packaging and tool configuration
    ├── documentation/           # Sphinx documentation source
    ├── sources/                 # All source code
    ├── tests/                   # Test suites
    ├── template/                # Copier template for project generation
    ├── .github/                 # GitHub Actions workflows
    ├── data/                    # Redistributable data resources
    └── .auxiliary/              # Development workspace

Source Code Organization
===============================================================================

Package Structure
-------------------------------------------------------------------------------

The main Python package follows the standard ``sources/`` directory pattern:

.. code-block::

    sources/
    └── emcdproj/                    # Main Python package
        ├── __/                      # Centralized import hub
        │   ├── __init__.py          # Re-exports core utilities
        │   ├── imports.py           # External library imports
        │   └── nomina.py            # emcd-projects-specific naming constants
        ├── __init__.py              # Package entry point
        ├── py.typed                 # Type checking marker
        ├── __main__.py              # CLI entry point for `python -m emcdproj`
        ├── cli.py                   # Command-line interface implementation
        ├── exceptions.py            # Package exception hierarchy
        ├── filesystem.py            # File system operations
        ├── interfaces.py            # Common interface definitions
        ├── template.py              # Template processing utilities
        ├── website.py               # Static website generation
        └── _typedecls/              # Type declaration stubs
            └── __builtins__.pyi     # Built-in type stubs

All package modules use the standard ``__`` import pattern as documented
in the common architecture guide.

Template System Organization
===============================================================================

Copier Template Structure
-------------------------------------------------------------------------------

The template system provides the scaffolding for new projects:

.. code-block::

    template/
    ├── copier.yaml                  # Template configuration and prompts
    ├── documentation/               # Documentation templates
    │   ├── architecture/            # Architecture documentation templates
    │   └── common/                  # Common documentation patterns
    ├── sources/                     # Source code templates
    ├── tests/                       # Test templates
    ├── .github/                     # GitHub Actions workflow templates
    └── .auxiliary/                  # Development workspace templates

This template structure mirrors the generated project structure while providing
Jinja2 templating for customization based on user selections.

Component Integration
===============================================================================

CLI Implementation
-------------------------------------------------------------------------------

The command-line interface is organized for maintainability:

.. code-block::

    emcdproj/
    ├── __main__.py      # Entry point: `python -m emcdproj`
    └── cli.py           # CLI implementation and argument parsing

This separation allows the CLI logic to be imported and tested independently
while following Python's standard module execution pattern.

GitHub Actions Integration
-------------------------------------------------------------------------------

Reusable workflows are organized by function:

.. code-block::

    .github/workflows/
    ├── core--initializer.yaml       # Project-specific workflow setup
    ├── tester.yaml                  # Main testing workflow
    ├── releaser.yaml                # Release automation workflow
    ├── validate-template.yaml       # Template validation workflow
    ├── claude.yaml                  # Claude Code integration workflow
    └── xrepo--*.yaml               # Cross-repository reusable workflows
        ├── xrepo--claude.yaml       # Claude workflow for external use
        ├── xrepo--documenter.yaml   # Documentation generation
        ├── xrepo--packager.yaml     # Package building and publishing
        ├── xrepo--reporter.yaml     # Coverage and reporting
        └── xrepo--tester.yaml       # Cross-platform testing

The ``xrepo--`` prefixed workflows are designed for use by external projects,
while core workflows are specific to the python-project-common repository.

Exception Organization
-------------------------------------------------------------------------------

Package-wide exceptions are centralized in ``sources/emcdproj/exceptions.py``
following the standard hierarchy patterns documented in the :doc:`../common/practices`.

Development Workspace Integration
-------------------------------------------------------------------------------

The ``.auxiliary/`` directory provides development-specific organization:

.. code-block::

    .auxiliary/
    ├── configuration/               # Development tool configurations
    │   ├── claude/                  # Claude Code configurations
    │   │   ├── agents/              # Specialized agent definitions
    │   │   └── commands/            # Custom slash commands
    │   └── conventions.md           # Development conventions and guidelines
    ├── instructions/                # Local copies of development guidelines
    ├── notes/                       # Development notes and TODO items
    └── scribbles/                   # Temporary development files

This workspace supports advanced development workflows including Claude Code
integration, specialized agents, and custom development tooling.

Architecture Evolution
===============================================================================

This filesystem organization provides a foundation that can evolve as the project grows:

**Template Extension**: New template features can be added by extending the ``template/`` structure while maintaining compatibility with existing projects.

**Workflow Enhancement**: Additional reusable workflows can be created following the ``xrepo--`` naming pattern for external consumption.

**Package Growth**: The main ``emcdproj`` package can grow through additional modules or subpackages while maintaining the centralized import pattern.

**Documentation Evolution**: The documentation structure supports both common patterns (shared across projects) and project-specific architecture documentation.

For questions about organizational principles, subpackage patterns, or testing strategies, refer to the comprehensive common documentation:

* :doc:`../common/architecture` - Architecture Patterns
* :doc:`../common/practices` - Development Practices
* :doc:`../common/tests` - Test Development Guidelines
