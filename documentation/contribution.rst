.. vim: set filetype=rst fileencoding=utf-8:
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


:tocdepth: 3


*******************************************************************************
Contribution
*******************************************************************************

Contribution to this project is welcome! However, it must follow the :doc:`code
of conduct <common/conduct>` for the project.


Ways to Contribute
===============================================================================

* File bug reports and feature requests in the `issue tracker
  <https://github.com/emcd/python-project-common/issues>`_. (Please try
  to avoid duplicate issues.)

* Fork the repository and submit `pull requests
  <https://github.com/emcd/python-project-common/pulls>`_ to improve the
  source code or documentation. Pull requests should follow the development
  guidance and standards below.


Development
===============================================================================

Architecture
-------------------------------------------------------------------------------

* The :doc:`capability specifications <specifications/index>` provide a good
  starting point to understand the requirements and motivations for the project.
  These should be reviewed and updated through the Openspec workflow when making
  changes that affect product functionality or user experience.

* The :doc:`system architecture overview <architecture/summary>` should be
  reviewed to understand the structure and operational patterns of the project.
  Major changes to the architecture should be reflected in this document.

* Document significant architectural decisions using Architectural Decision
  Records (ADRs) in the ``architecture/decisions/`` directory. See the
  :doc:`architecture documentation guide <common/architecture>` for ADR format
  and best practices.

* Document technical design specifications for Python interfaces, module
  organization, and implementation patterns in :doc:`design documents
  <architecture/designs/index>` to guide implementation efforts.

Guidance and Standards
-------------------------------------------------------------------------------

* Follow the :doc:`development environment preparation and management
  instructions <common/environment>` to ensure consistency with maintainer
  development environments and CI workflows.

* Configure Git commit signing as required for all contributions. See the
  :doc:`environment setup guide <common/environment>` for configuration
  details.

* Adhere to the :doc:`development practices <common/practices>`, :doc:`code
  style <common/style>`, and :doc:`testing guidelines <common/tests>` to
  improve the probability of pull request acceptance. You may wish to use an
  LLM to assist with this, if the standards seem too onerous or specific.

* Also consider the :doc:`nomenclature advice <common/nomenclature>` for
  consistency and to improve the probability of pull request acceptance.

* Run validation commands before submitting contributions. See the
  :doc:`validation guide <common/validation>` for available commands and
  workflow. (If you installed the Git pre-commit and pre-push hooks during
  environment setup, then they will run the validations for you.)

* Prepare changelog fragments according to the :doc:`releases guide
  <common/releases>` as appropriate.

* Although unncessary for non-maintainer contributions, additional background
  can be found in the :doc:`maintenance guide <common/maintenance>`.

* For shared documentation under ``documentation/common``, follow the stable
  anchor contract in :doc:`ADR 003
  <architecture/decisions/003-common-doc-anchor-contract>`. Treat anchor IDs as
  part of the docs major-line compatibility contract (for example, ``docs-2``).

Artificial Intelligence
-------------------------------------------------------------------------------

* Contributions, which are co-authored by large language models (LLMs), are
  welcome, provided that they adhere to the project guidance and standards
  above and are, otherwise, of good quality.

* A more compact representation of the above guidance and standards, plus some
  other advice for these models, can be found in
  ``.auxiliary/configuration/conventions.md``. You may link to this file from a
  ``AGENTS.md``, ``CLAUDE.md``, ``GEMINI.md``, ``CONVENTIONS.md``, etc... file
  in the root of the project. These files are ignored by Git as we do not wish
  to pollute the root of the project with them in the upstream repository.

Resources
-------------------------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   Code of Conduct <common/conduct>
   specifications/index
   architecture/index
   devapi
   Environment Guide <common/environment>
   Practices Guide <common/practices>
   Code Style Guide <common/style>
   Testing Guide <common/tests>
   Nomenclature Guide <common/nomenclature>
   Germanic Nomenclature Guide <common/nomenclature-germanic>
   Validation Guide <common/validation>
   Release Guide <common/releases>
   Maintenance Guide <common/maintenance>
   Architecture Guide <common/architecture>
   Requirements Guide <common/requirements>

.. Language-specific guides stay in a hidden toctree so Sphinx includes them
   in the site graph without adding renderer-specific navigation glue to the
   portable common Markdown sources.
.. toctree::
   :hidden:

   Python Environment Guide <common/environment-python>
   Python Development Guide <common/practices-python>
   Rust Development Guide <common/practices-rust>
   TOML Configuration Practices <common/practices-toml>
   Python Testing Guide <common/tests-python>
   Python Validation Guide <common/validation-python>
   Python Release Guide <common/releases-python>
