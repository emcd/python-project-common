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
Validation (Python)
*******************************************************************************

This guide provides Python-specific validation commands for projects using
Hatch environments. For shared validation expectations, see
:doc:`validation`.

Commands
===============================================================================

Run validation commands with:
``hatch --env develop run <command>``.

**linters**
  Runs code quality checks including Ruff linting, Pyright type checking, and
  optional language-specific linting configured by the project.

**pytest**
  Runs quick tests for rapid development feedback.

**testers**
  Runs the full test suite with coverage reporting. Coverage artifacts are
  typically written under ``.auxiliary/artifacts/coverage-pytest/``.

**packagers**
  Builds distribution packages using Hatch. Projects with executable outputs
  may also run PyInstaller in this stage.

**docsgen**
  Builds project documentation and link checks. Artifacts are typically written
  under ``.auxiliary/artifacts/sphinx-html/``.

**make-all**
  Runs the full quality sequence (linters, testers, packagers, docsgen).

Workflow
===============================================================================

1. **During Development**: Use ``pytest`` for quick feedback.
2. **Before Committing**: Run ``linters`` to catch quality and type issues.
3. **Before Pull Requests**: Run ``make-all`` for comprehensive validation.

All required validation commands must pass before contributions can be
accepted. If Git hooks are installed, they will run part of this workflow
automatically.
