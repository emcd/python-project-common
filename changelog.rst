

.. towncrier release notes start


Copier Template 1.8.1 (2025-01-11)
==================================

Bugfixes
--------

- Add missing 'recursive' option to Pylint invocation in Git pre-push hook.


Copier Template 1.8 (2025-01-11)
================================

Features
--------

- Add option to inject base exceptions for package.
- Add 'recursive' option to Pylint invocation for better module discovery.

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
