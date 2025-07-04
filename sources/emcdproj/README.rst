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
                                 emcd-projects
*******************************************************************************

.. image:: https://img.shields.io/pypi/v/emcd-projects
   :alt: Package Version
   :target: https://pypi.org/project/emcd-projects/

.. image:: https://img.shields.io/pypi/status/emcd-projects
   :alt: PyPI - Status
   :target: https://pypi.org/project/emcd-projects/

.. image:: https://github.com/emcd/python-project-common/actions/workflows/tester.yaml/badge.svg?branch=master&event=push
   :alt: Tests Status
   :target: https://github.com/emcd/python-project-common/actions/workflows/tester.yaml

.. image:: https://emcd.github.io/python-project-common/coverage.svg
   :alt: Code Coverage Percentage
   :target: https://github.com/emcd/python-project-common/actions/workflows/tester.yaml

.. image:: https://img.shields.io/github/license/emcd/python-project-common
   :alt: Project License
   :target: https://github.com/emcd/python-project-common/blob/master/LICENSE.txt

.. image:: https://img.shields.io/pypi/pyversions/emcd-projects
   :alt: Python Versions
   :target: https://pypi.org/project/emcd-projects/

🛠️ Administration utilities for managing projects built from the
`emcd/python-project-common <https://github.com/emcd/python-project-common>`_
Copier template.

Installation 📦
===============================================================================

Method: Install Executable Script
-------------------------------------------------------------------------------

Install via the `uv <https://github.com/astral-sh/uv/blob/main/README.md>`_
``tool`` command:

::

    uv tool install emcd-projects

or, run directly with `uvx
<https://github.com/astral-sh/uv/blob/main/README.md>`_:

::

    uvx --from emcd-projects emcdproj

Or, install via `pipx <https://pipx.pypa.io/stable/installation/>`_:

::

    pipx install emcd-projects

Method: Install Python Package
-------------------------------------------------------------------------------

Install via `uv <https://github.com/astral-sh/uv/blob/main/README.md>`_ ``pip``
command:

::

    uv pip install emcd-projects

Or, install via ``pip``:

::

    pip install emcd-projects

Features
===============================================================================

🌐 **Static Website Maintenance**
   - Generates badges/shields based on test coverage.
   - Maintains index of versioned documentation and coverage reports.
   - No need for Codecov, ReadTheDocs, etc...; static site can be hosted
     anywhere which can deploy from a Git repo branch (GitHub Pages, etc...).

`More Flair <https://www.imdb.com/title/tt0151804/characters/nm0431918>`_
===============================================================================

.. image:: https://img.shields.io/github/last-commit/emcd/python-project-common
   :alt: GitHub last commit
   :target: https://github.com/emcd/python-project-common

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json
   :alt: Copier
   :target: https://github.com/copier-org/copier

.. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
   :alt: Hatch
   :target: https://github.com/pypa/hatch

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
   :alt: pre-commit
   :target: https://github.com/pre-commit/pre-commit

.. image:: https://microsoft.github.io/pyright/img/pyright_badge.svg
   :alt: Pyright
   :target: https://microsoft.github.io/pyright

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :alt: Ruff
   :target: https://github.com/astral-sh/ruff

.. image:: https://img.shields.io/pypi/implementation/emcd-projects
   :alt: PyPI - Implementation
   :target: https://pypi.org/project/emcd-projects/

.. image:: https://img.shields.io/pypi/wheel/emcd-projects
   :alt: PyPI - Wheel
   :target: https://pypi.org/project/emcd-projects/
