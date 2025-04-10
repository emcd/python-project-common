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

:orphan:


*******************************************************************************
Release Notes
*******************************************************************************

.. towncrier release notes start


Copier Template 1.13 (2025-03-26)
==================================

Enhancements
------------

- Move changelog into documentation directory, thereby clearing up the
  top-level directory more and simplifying documentation generation.


Copier Template 1.12 (2025-03-25)
==================================

Enhancements
------------

- Major refactor of documentation: move Sphinx documentation up one level,
  shift Towncrier fragments storage to ``.auxiliary/data/towncrier``, and
  reference common documentation rather than generate copies of it in each
  repository.


Copier Template 1.11 (2025-03-23)
==================================

Repairs
-------

- Fixes to whitespace condensation to remove weird gaps when templates do not
  expand due to conditional logic.

Enhancements
------------

- Tweaks to Pylint configuration.
- Ensure that Tryceratops does not run against ``tests`` directory.


Copier Template 1.10 (2025-02-23)
==================================

Repairs
-------

- EditorConfig: Ensure final newline, whenever possible

Enhancements
------------

- Generation of CLI stub.
- Creation of standalone executables.
- Package data resources.
- Tweaks to Pylint and Pyright configuration.
- Ensure that Coverage only covers sources and not tests.
- Ensure that Pytest only looks for tests under ``tests`` and not ``sources``.


Copier Template 1.9 (2025-01-21)
==================================

Enhancements
------------

- Tweaks to Pylint and Pyright configuration.


Copier Template 1.8.1 (2025-01-11)
==================================

Repairs
-------

- Add missing ``recursive`` option to Pylint invocation in Git pre-push hook.


Copier Template 1.8 (2025-01-11)
================================

Enhancements
------------

- Add option to inject base exceptions for package.
- Add ``recursive`` option to Pylint invocation for better module discovery.

Copier Template 1.7 (2025-01-10)
================================

Enhancements
------------

- Add detailed nomenclature guide for Python and Rust projects.
- Improve style guide with clarifications on whitespace and docstrings.
- Update Towncrier documentation link to stable version.


Copier Template 1.6 (2024-12-16)
================================

Enhancements
------------

- Add Towncrier fragment documentation with examples.
- Control emission of Rust-specific sections in documentation.

Repairs
-------

- Add more Pylint ignores for test files.


Copier Template 1.5 (2024-12-15)
================================

Enhancements
------------

- Add support for immutable modules in template packages, including class
  definitions and tests.


Copier Template 1.4 (2024-12-13)
================================

Enhancements
------------

- Add code style validation and documentation for Python and Rust.
- Add development guide with detailed style and practices documentation.


Copier Template 1.3 (2024-12-12)
================================

Enhancements
------------

- Add support for injecting common internals into foundational packages:
  - Docstring utilities
  - Immutable types
  - Base imports
- Add Pylint plugin for path-based check disabling.


Copier Template 1.2 (2024-12-11)
================================

Enhancements
------------

- Add improved configuration options for Rust integration:
  - Configurable crate names
  - Configurable extension module names
- Change to GitHub-based badge for license.
- Add ``cargo-deny`` configuration for Rust dependencies.


Copier Template 1.1 (2024-12-10)
================================

Enhancements
------------

- Version Github workflows by tag in Copier answers ``_commit`` field.


Copier Template 1.0.2 (2024-12-10)
==================================

Repairs
-------

- Properly specify template directory.


Copier Template 1.0.1 (2024-12-08)
==================================

Repairs
-------

- Fix assorted issues in template and workflows.


Copier Template 1.0 (2024-12-05)
================================

Enhancements
------------

- Add Copier template with support for Python packages:
  - Modern Python packaging using Hatch
  - Sphinx documentation framework
  - Quality assurance tools configuration
  - Optional Rust extension support via PyO3/Maturin
- Add reusable GitHub Actions workflows and composite actions:
  - Cross-repository testing workflow
  - Documentation generation and publication
  - Package building and publication
  - Code quality reporting
