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

This guide provides language-neutral environment preparation guidance. For
Python-specific setup and commands, see :doc:`environment-python`.

Initial Installation
===============================================================================

1. Ensure that you have installed `Git LFS <https://git-lfs.com/>`_.

2. Clone your fork of the repository.

3. Install Git LFS hooks in the repository:
   ::

        git lfs install

4. Install language- and stack-specific tooling required by the project. The
   exact tools vary by repository and should be documented in project-specific
   overlays (for example, :doc:`environment-python`).

5. Install Git pre-commit and pre-push hooks using the workflow documented by
   the project.

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

1. Pull the latest changes:
   ::

        git pull

2. Refresh local development environments and tool caches according to the
   stack-specific guidance for the project.

Language-Specific Overlays
===============================================================================

* :doc:`environment-python` - Python tooling and Hatch workflow.
