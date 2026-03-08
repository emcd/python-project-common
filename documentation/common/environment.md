<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->

<a id="environment"></a>
# Environment

This guide provides language-neutral environment preparation guidance. For
Python-specific setup and commands, see the
[Python environment guide](environment-python.md).

<a id="initial-installation"></a>
## Initial Installation

1. Ensure that you have installed [Git LFS](https://git-lfs.com/).
2. Clone your fork of the repository.
3. Install Git LFS hooks in the repository:

   ```shell
   git lfs install
   ```

4. Install language- and stack-specific tooling required by the project. The
   exact tools vary by repository and should be documented in project-specific
   overlays (for example, the
   [Python environment guide](environment-python.md)).
5. Install Git pre-commit and pre-push hooks using the workflow documented by
   the project.

<a id="git-commit-signatures"></a>
### Git Commit Signatures

Git commit signatures are required for all contributions to maintain code
integrity and authenticity.

1. Configure Git commit signing by following the [GitHub commit signing guide](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits).
2. If you choose to use SSH keys for Git commit signing, you may want to set up
   local verification of SSH signatures. See the [GitLab documentation on local verification](https://docs.gitlab.com/user/project/repository/signed_commits/ssh/#verify-commits-locally)
   for configuration details (this applies to GitHub repositories as well).

<a id="installation-updates"></a>
## Installation Updates

1. Pull the latest changes:

   ```shell
   git pull
   ```

2. Refresh local development environments and tool caches according to the
   stack-specific guidance for the project.

<a id="language-specific-overlays"></a>
## Language-Specific Overlays

- [Python environment guide](environment-python.md) - Python tooling and Hatch
  workflow.
