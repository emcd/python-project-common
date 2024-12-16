

.. towncrier release notes start

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

Fixes
-----

- Properly specify template directory.


Copier Template 1.0.1 (2024-12-08)
==================================

Fixes
-----

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
