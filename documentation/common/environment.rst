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
Environment
*******************************************************************************

Initial Installation
===============================================================================

Commands
-------------------------------------------------------------------------------

1. Ensure that you have installed `Git LFS <https://git-lfs.com/>`_.

2. Clone your fork of the repository.

3. Install Git LFS Git hooks in this repository:
   ::

        git lfs install

4. Ensure that you have installed either `pipx <https://pipx.pypa.io/stable/>`_
   or `uv <https://github.com/astral-sh/uv/blob/main/README.md>`_ for managing
   Python tools.

   .. note::

      If installing Pipx via ``pip``, you will want to use your system Python
      rather than the current global Python provided by Asdf, Mise, Pyenv,
      etc.... This is to ensure that a change of global version does not break
      ``pipx`` later.

5. Ensure that you have installed
   `Copier <https://copier.readthedocs.io/en/stable/>`_ and
   `Hatch <https://github.com/pypa/hatch/blob/master/README.md>`_.

   If using Pipx:
   ::

        pipx install copier hatch

   If using uv:
   ::

        uv tool install copier
        uv tool install hatch

6. Install Git pre-commit and pre-push hooks:
   ::

        hatch --env develop run pre-commit install --config .auxiliary/configuration/pre-commit.yaml

Git Commit Signatures
-------------------------------------------------------------------------------

Git commit signatures are required for all contributions to maintain code
integrity and authenticity.

1. Configure Git commit signing by following the `GitHub commit signing guide
   <https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits>`_.

2. If you choose to use SSH keys for Git commit signing, you may want to set up
   local verification of SSH signatures. See the `GitLab documentation on local
   verification <https://docs.gitlab.com/user/project/repository/signed_commits/ssh/#verify-commits-locally>`_
   for configuration details (this applies to GitHub repositories as well).

Installation Updates
===============================================================================

1. Run:
   ::

        git pull

2. Remove the Hatch virtual environments:
   ::

        hatch env prune

Python Interpreter
===============================================================================

1. Run:
   ::

        hatch --env develop run python

Shell
===============================================================================

1. Run:
   ::

        hatch --env develop shell
