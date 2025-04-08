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
Release Notes
*******************************************************************************

.. towncrier release notes start

Emcdproj 1.14 (2025-04-08)
==========================

Features
--------

- Ability to update static website with documentation and code coverage report
  for particular package version.


Copier Template 1.13 (2025-03-26)
==================================

Improvements
------------

- Move changelog into documentation directory, thereby clearing up the
  top-level directory more and simplifying documentation generation.


Copier Template 1.12 (2025-03-25)
==================================

Improvements
------------

- Major refactor of documentation: move Sphinx documentation up one level,
  shift Towncrier fragments storage to ``.auxiliary/data/towncrier``, and
  reference common documentation rather than generate copies of it in each
  repository.


Copier Template 1.11 (2025-03-23)
==================================

Bugfixes
--------

- Fixes to whitespace condensation to remove weird gaps when templates do not
  expand due to conditional logic.

Improvements
------------

- Tweaks to Pylint configuration.

- Ensure that Tryceratops does not run against ``tests`` directory.

Copier Template 1.10 (2025-02-23)
==================================

Bugfixes
--------

- EditorConfig: Ensure final newline, whenever possible

Features
--------

- Generation of CLI stub.

- Creation of standalone executables.

- Package data resources.

Improvements
------------

- Tweaks to Pylint and Pyright configuration.

- Ensure that Coverage only covers sources and not tests.

- Ensure that Pytest only looks for tests under ``tests`` and not ``sources``.


Copier Template 1.9 (2025-01-21)
==================================

Improvements
------------

- Tweaks to Pylint and Pyright configuration.


Copier Template 1.8.1 (2025-01-11)
==================================

Bugfixes
--------

- Add missing ``recursive`` option to Pylint invocation in Git pre-push hook.


Copier Template 1.8 (2025-01-11)
================================

Features
--------

- Add option to inject base exceptions for package.
- Add ``recursive`` option to Pylint invocation for better module discovery.

Copier Template 1.7 (2025-01-10)
================================

Features
--------

- Add detailed nomenclature guide for Python and Rust projects.
- Improve style guide with clarifications on whitespace and docstrings.
- Update Towncrier documentation link to stable version.


Copier Template 1.6 (2024-12-16)
================================

Features
--------

- Add Towncrier fragment documentation with examples.
- Control emission of Rust-specific sections in documentation.

Bugfixes
--------

- Add more Pylint ignores for test files.


Copier Template 1.5 (2024-12-15)
================================

Features
--------

- Add support for immutable modules in template packages, including class
  definitions and tests.


Copier Template 1.4 (2024-12-13)
================================

Features
--------

- Add code style validation and documentation for Python and Rust.
- Add development guide with detailed style and practices documentation.


Copier Template 1.3 (2024-12-12)
================================

Features
--------

- Add support for injecting common internals into foundational packages:
  - Docstring utilities
  - Immutable types
  - Base imports
- Add Pylint plugin for path-based check disabling.


Copier Template 1.2 (2024-12-11)
================================

Features
--------

- Add improved configuration options for Rust integration:
  - Configurable crate names
  - Configurable extension module names
- Change to GitHub-based badge for license.
- Add ``cargo-deny`` configuration for Rust dependencies.


Copier Template 1.1 (2024-12-10)
================================

Features
--------

- Version Github workflows by tag in Copier answers ``_commit`` field.


Copier Template 1.0.2 (2024-12-10)
==================================

Bugfixes
--------

- Properly specify template directory.


Copier Template 1.0.1 (2024-12-08)
==================================

Bugfixes
--------

- Fix assorted issues in template and workflows.


Copier Template 1.0 (2024-12-05)
================================

Features
--------

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
