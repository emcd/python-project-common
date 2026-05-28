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
Copier Template Release Notes
*******************************************************************************


These release notes summarize changes to the Copier template and generated
projects.


Copier Template 1.58
====================

Removals
--------

- Remove PyPy 3.10 from generated project support because current releases of
  common dependencies such as ``cryptography`` no longer reliably provide or
  build PyPy 3.10 support.

Enhancements
------------

- Convert shared common documentation to Markdown with explicit anchors while
  preserving generated project links through the Sphinx assembly layer.
- Split and refine shared architecture, practices, tests, releases,
  environment, and validation guidance.
- Fix the generated ``pipx`` installation URL.
- Skip generated PyPI and GitHub release publication when the Git tag version
  does not match the built package version.
- Ensure the template validation workflow installs ``emcd-vibe-linter`` via
  ``pipx``.


Copier Template 1.57.1 (2025-12-07)
====================================

Repairs
-------

- Do not add ``emcd-vibe-linter`` to generated development environments, to
  avoid dependency cycles.
- Apply a cosmetic repair to generated standard imports.


Copier Template 1.57 (2025-12-04)
==================================

Enhancements
------------

- Ignore ``.auxiliary/pocs`` in generated Git hooks.


Copier Template 1.56 (2025-12-03)
==================================

Enhancements
------------

- Integrate OpenSpec specifications and designs into generated Sphinx
  documentation.


Copier Template 1.55 (2025-12-03)
==================================

Enhancements
------------

- Configure ``myst-parser`` support for generated Sphinx documentation.
- Integrate ``emcd-vibe-linter`` into generated project validation.
- Use the distribution name, rather than package name, when configuring Sphinx
  ``linkcheck`` to ignore unpublished PyPI package links.


Copier Template 1.54.1 (2025-11-29)
====================================

Repairs
-------

- Emulate isolated Hatch build environments for generated package builds after
  upstream Hatch behavior changed.

Enhancements
------------

- Add Detextive and Librovore to the README template's related-projects list.


Copier Template 1.54 (2025-11-04)
==================================

Enhancements
------------

- Enhance foundational package injection with immutable exceptions and common
  dependencies.


Copier Template 1.53 (2025-11-03)
==================================

Enhancements
------------

- Move ``vulture`` out of the generated ``linters`` script and into the Git
  pre-push hook.


Copier Template 1.52 (2025-10-28)
==================================

Removals
--------

- Remove coder-agent-related entries from the generated top-level
  ``.gitignore``.


Copier Template 1.51 (2025-10-24)
==================================

Removals
--------

- Remove generated agent configuration now managed by ``agents-common``.

Enhancements
------------

- Add CPython 3.14 and PyPy 3.11 to generated project version options.


Copier Template 1.50 (2025-10-21)
==================================

Enhancements
------------

- Use ``emcd-appcore[cli]`` rather than direct ``tyro`` dependencies for
  generated CLI support.
- Switch generated executable release workflows from ``macos-13`` to
  ``macos-15-intel``.


Copier Template 1.49 (2025-09-06)
==================================

Enhancements
------------

- Add Opencode template integration for backup agentic coding.
- Update generated Claude Code provider wrappers.


Copier Template 1.48 (2025-09-04)
==================================

Enhancements
------------

- Add argument hints to generated release commands.
- Simplify generated Claude Code tool permissions and remove the Ruff MCP
  server from generated configuration.


Copier Template 1.47.2 (2025-09-02)
====================================

Repairs
-------

- Streamline generated Claude commands and remove stale references.


Copier Template 1.47.1 (2025-09-02)
====================================

Repairs
-------

- Update generated command references for language-specific practices guides.


Copier Template 1.47 (2025-09-02)
==================================

Enhancements
------------

- Optimize generated Claude Code commands around reference-first documentation.
- Refactor generated common guidance into language-specific style, practices,
  and nomenclature guides.


Copier Template 1.46.2 (2025-08-28)
====================================

Repairs
-------

- Fix the generated ``vulture`` ignore entry for decorated functions.


Copier Template 1.46.1 (2025-08-28)
====================================

Repairs
-------

- Fix a generated Claude command name.


Copier Template 1.46 (2025-08-28)
==================================

Enhancements
------------

- Upgrade generated Claude GitHub Actions integration and MCP setup.
- Add generated ``claude-ds`` script structure.
- Rename the README template's ``More Flair`` section to ``Additional
  Indicia`` and remove the IMDB link.


Copier Template 1.45 (2025-08-26)
==================================

Enhancements
------------

- Add 30-minute Bash timeout settings for generated Claude Code configuration.
- Generate ``vulturefood.py`` from a Jinja template and conditionally include
  Omnierror entries.
- Lower generated ``vulture`` confidence threshold and add a whitelist file.


Copier Template 1.44 (2025-08-22)
==================================

Enhancements
------------

- Update generated project state from its own template without additional
  distinct template behavior.


Copier Template 1.43 (2025-08-17)
==================================

Enhancements
------------

- Add Librovore MCP server integration to generated projects.


Copier Template 1.42.1 (2025-08-16)
====================================

Repairs
-------

- Add the missing ``--diff`` option to generated ``isort`` validation.


Copier Template 1.42 (2025-08-15)
==================================

Enhancements
------------

- Add generated Git hooks that prevent commits when linters or tests fail.
- Add generated ``isort`` configuration and skip all ``__init__`` modules.
- Improve generated Python type-annotation agent definitions.


Copier Template 1.41 (2025-08-14)
==================================

Enhancements
------------

- Add generated dead-code detection support with ``vulture``.
- Add generated Copier-update and technical-debt review commands.
- Refactor generated test architecture around the ``__.py`` pattern.
- Remove generated requests to use the ``text-editor`` MCP server.


Copier Template 1.40 (2025-08-10)
==================================

Enhancements
------------

- Add testplan architecture and rename generated test commands for
  language-specific workflows.
- Improve generated consultation triggers and command-index maintenance.


Copier Template 1.39 (2025-08-09)
==================================

Enhancements
------------

- Improve generated meta commands for creating and updating Claude Code
  commands.
- Improve generated architecture and Python design command guidance.


Copier Template 1.38 (2025-08-07)
==================================

Enhancements
------------

- Clarify generated ``python-conformer`` agent scope for Python-only changes.


Copier Template 1.37 (2025-08-07)
==================================

Enhancements
------------

- Add specialized generated slash commands for comprehensive project workflows.


Copier Template 1.36 (2025-08-07)
==================================

Enhancements
------------

- Add architecture and requirements documentation framework to generated
  projects.
- Add generated filesystem organization patterns.
- Remove stale practices-guide references from generated inquiry commands.


Copier Template 1.35 (2025-08-05)
==================================

Enhancements
------------

- Improve generated Claude Code configuration efficiency.


Copier Template 1.34 (2025-08-05)
==================================

Enhancements
------------

- Add local documentation system support and improve generated command
  formatting.
- Add generated inquiry command and MCP-server research guidance.
- Avoid timeouts for slow documentation sites in generated documentation
  workflows.


Copier Template 1.33 (2025-07-26)
==================================

Enhancements
------------

- Improve generated Claude Code hooks and guidance.
- Split generated test development commands into planning and implementation
  phases.
- Improve workflow monitoring guidance to prevent false assumptions.


Copier Template 1.32 (2025-07-22)
==================================

Enhancements
------------

- Rename generated Claude commands to use a common prefix.
- Update generated command URLs to the ``docs-1`` documentation tag.
- Refine generated practices and style guidance.
- Add generated Claude Code pre-tool hooks for Python command checking and
  post-tool linter runs.

Repairs
-------

- Remove dangerous pre-flight command argument expansions from generated
  release-final guidance.


Copier Template 1.31 (2025-07-16)
==================================

Repairs
-------

- Deduplicate generated Git hook test runs on push.
- Ensure generated slow-test scripts parse on Windows.


Copier Template 1.30 (2025-07-15)
==================================

Enhancements
------------

- Improve generated Git hook performance.

Repairs
-------

- Revert an invalid generated ``release-final`` simplification that assumed
  persistent shell environments across command executions.


Copier Template 1.29.1 (2025-07-12)
====================================

Repairs
-------

- Template release included no distinct generated-project behavior beyond
  release metadata synchronization.


Copier Template 1.29 (2025-07-11)
==================================

Enhancements
------------

- Add generated slash commands for systematic release-note generation and test
  writing.
- Improve generated patch-release and final-release command guidance.


Copier Template 1.28 (2025-07-10)
==================================

Enhancements
------------

- Enhance shared release and testing guidance consumed by generated projects.


Copier Template 1.27 (2025-07-04)
==================================

Enhancements
------------

- Improve generated Claude release workflow commands.
- Ensure generated Claude configuration maintains working directory context.
- Use the production website publication mode from generated release workflows.


Copier Template 1.26 (2025-07-03)
==================================

Enhancements
------------

- Add a Contribution section to generated README files and update
  documentation URLs.


Copier Template 1.25 (2025-07-03)
==================================

Enhancements
------------

- Add a standardized Installation section to generated README files.
- Add generated Claude Code slash commands for automated releases.


Copier Template 1.24 (2025-06-29)
==================================

Enhancements
------------

- Add project-local scratch space for generated projects.


Copier Template 1.23 (2025-06-29)
==================================

Enhancements
------------

- Expand generated AI conventions, MCP server guidance, and AI-related project
  configuration.


Copier Template 1.22 (2025-06-14)
==================================

Repairs
-------

- Remove ``emcd-projects`` from generated development dependencies to avoid
  dependency cycles.
- Account for GitHub Windows runners cloning onto either ``C:`` or ``D:`` in
  generated coverage path configuration.
- Appease newer Clippy behavior in generated Rust-extension projects.
- Fix spacing in generated executable documentation.


Copier Template 1.21 (2025-06-05)
==================================

Enhancements
------------

- Remove ``from __future__ import annotations`` from generated internal imports
  and clean up generated docstrings.


Copier Template 1.20.2 (2025-06-05)
====================================

Enhancements
------------

- Surface the generated ``nomina`` module in development API documentation.


Copier Template 1.20.1 (2025-06-02)
====================================

Repairs
-------

- Fix generated Claude workflow allowed-tools formatting.
- Ensure the generated Claude workflow references the cross-repository workflow
  through the floating workflow tag.


Copier Template 1.20 (2025-05-29)
==================================

Enhancements
------------

- Switch generated GitHub workflow templates to floating version tags.


Copier Template 1.19.2 (2025-05-29)
====================================

Repairs
-------

- Add missing ``attestations`` permission to generated release workflows.


Copier Template 1.19.1 (2025-05-29)
====================================

Repairs
-------

- Grant the correct token permissions to generated Claude workflows.


Copier Template 1.19 (2025-05-27)
==================================

Enhancements
------------

- Replace generated Sigstore signature generation with GitHub artifact
  attestations.
- Drop ``:no-members:`` from generated package ``automodule`` directives.


Copier Template 1.18 (2025-05-27)
==================================

Enhancements
------------

- Add generated AI guidance and Claude PR assistant workflow support.
- Factor generated Claude workflow configuration into project-specific and
  cross-repository portions.
- Add README template entries for additional related projects.
- Backport documentation configuration from downstream projects.
- Split generated names and type aliases out of internal imports modules.

Removals
--------

- Remove injection of docstring utilities and immutables now that replacement
  packages are available.


Copier Template 1.17.1 (2025-04-30)
====================================

Repairs
-------

- Properly interpret TOML line continuations for generated multi-line commands
  on Windows.


Copier Template 1.17 (2025-04-30)
==================================

Enhancements
------------

- Split generated test execution from coverage reporting.
- Add Sphinx doctests to generated coverage reporting.
- Add manually dispatched template validation workflow support.
- Clean up generated internals subpackages.


Copier Template 1.16 (2025-04-10)
==================================

Enhancements
------------

- Add related-projects section to generated README files.
- Declare equivalent GitHub Actions runner coverage paths in generated
  coverage configuration.

Removals
--------

- Remove Semgrep from generated linters to reduce validation latency.


Copier Template 1.15 (2025-04-08)
==================================

Enhancements
------------

- Consolidate generated Python linters into Ruff.
- Update generated ``pre-commit`` configuration.
- Simplify generated Towncrier categories and release guidance.


Copier Template 1.14 (2025-04-08)
==================================

Enhancements
------------

- Update generated development dependencies.

Repairs
-------

- Add missing ``tomli`` import to generated project manifest support.


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
