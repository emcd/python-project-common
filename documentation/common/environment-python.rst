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
Environment (Python)
*******************************************************************************

This guide provides Python-specific environment setup guidance for projects
using the Python template toolchain. For shared baseline setup, see
:doc:`environment`.

Tooling
===============================================================================

1. Ensure that you have installed either
   `pipx <https://pipx.pypa.io/stable/>`_ or
   `uv <https://github.com/astral-sh/uv/blob/main/README.md>`_ for managing
   Python tools.

   .. note::

      If installing Pipx via ``pip``, use your system Python rather than a
      mutable global version managed by Asdf, Mise, or Pyenv. This reduces the
      risk that subsequent global version changes break ``pipx``.

2. Ensure that you have installed
   `Copier <https://copier.readthedocs.io/en/stable/>`_ and
   `Hatch <https://github.com/pypa/hatch/blob/master/README.md>`_.

   If using Pipx:
   ::

        pipx install copier hatch

   If using uv:
   ::

        uv tool install copier
        uv tool install hatch

Git Hooks
===============================================================================

Install Git pre-commit and pre-push hooks with the Python development
environment:
::

    hatch --env develop run pre-commit install --config .auxiliary/configuration/pre-commit.yaml

Refreshing Environments
===============================================================================

Remove and rebuild Hatch virtual environments after dependency or interpreter
changes:
::

    hatch env prune

Interpreter
===============================================================================

Run Python inside the development environment:
::

    hatch --env develop run python

Shell
===============================================================================

Open a shell inside the development environment:
::

    hatch --env develop shell
