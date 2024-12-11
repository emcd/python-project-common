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
Development Guide
*******************************************************************************

Initial Installation
===============================================================================

1. Ensure that you have installed `Git LFS <https://git-lfs.com/>`_.

2. Clone your fork of the repository.

3. Install Git LFS Git hooks in this repository:
   ::

        git lfs install

4. Ensure that you have installed `Pipx <https://pipx.pypa.io/stable/>`_.
   (If installing via ``pip``, you will want to use your system Python rather
   than the current global Python provided by Asdf, Mise, Pyenv, etc....)

5. Ensure that you have installed
   `Copier <https://copier.readthedocs.io/en/stable/>`_ and
   `Hatch <https://github.com/pypa/hatch/blob/master/README.md>`_ via Pipx:
   ::

        pipx install copier hatch

6. Install Git pre-commit and pre-push hooks:
   ::

        hatch --env develop run pre-commit install --config .auxiliary/configuration/pre-commit.yaml

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

Guidelines
===============================================================================

* Be sure to install the Git hooks, as mentioned in the ``Installation``
  section. This will save you turnaround time from pull request validation
  failures.

* Maintain or improve the current level of code coverage. Even if code coverage
  is at 100%, consider cases which are not explicitly tested.

* Allow natural and expected Python exceptions to pass through the application
  programming interface boundary. Raise an exception from the library for any
  failure condition that arises from the use of the provided features that are
  part of the interfaces of the underlying Python object types or functions.

* Never swallow exceptions. Either chain a ``__cause__`` with a ``from``
  original exception or raise a new exception with original exception as the
  ``__context__``.

* Avoid ancillary imports into a module namespace. Instead, place common
  imports into the `__` base module or import at the function level. This
  avoids pollution of the module namespace, which should only have public
  attributes which relate to the interface that it is providing. This also
  makes functions more relocatable, since they carry their dependencies with
  them rather than rely on imports within the module which houses them.

* Documentation must be written as Sphinx reStructuredText. The docstrings for
  functions must not include parameter or return type documentation. Parameter
  and return type documentation is handled via :pep:`727` annotations. Pull
  requests, which include Markdown documentation or which attempt to provide
  function docstrings in the style of Google, NumPy, Sphinx, etc..., will be
  rejected.

* Respect the existing code style. Pull requests, which attempt to enforce
  the ``black`` style  or another style, will be rejected. A summary of the
  style is:

  - **Spacing**: Use spaces between identifiers and other tokens. Modern
    writing systems use this convention, which emerged around the 7th century
    of the Common Era, to improve readability. Computer code can generally be
    written this way too... also to improve readability.

  - **Line Width**: Follow :pep:`8` on this: no more than 79 columns for code
    lines. Consider how long lines affect display on laptops or side-by-side
    code panes with enlarged font sizes. (Enlarged font sizes are used to
    reduce eye strain and allow people to code without visual correction.)

  - **Vertical Compactness**: Function definitions, loop bodies, and condition
    bodies, which consist of a single statement and which are sufficiently
    short, should be placed on the same line as the statement that introduces
    the body. Blank lines should not be used to group statements within a
    function body. If you need to group statements within a function body, then
    perhaps the function should be refactored. Function bodies should not be
    longer than thirty lines. I.e., one should not have to scroll to read a
    function.

* Use long option names, whenever possible, in command line examples.


Release Process
===============================================================================

Initial Release Candidate
-------------------------------------------------------------------------------

1. Checkout ``master`` branch.

2. Pull from upstream to ensure all changes have been synced.

3. Checkout new release branch: ``release-<major>.<minor>``.

4. Bump alpha to release candidate. Commit.
   ::

        hatch --env develop version rc

5. Tag.
   ::

        git tag v${rc_version}

6. Push release branch and tag to upstream with tracking enabled.

7. Checkout ``master`` branch.

8. Bump alpha to next minor version on ``master`` branch. Commit.
   ::

        hatch --env develop version minor,alpha

9. Tag start of development for next release.
    ::

        git tag i${next_release_version}

Release
-------------------------------------------------------------------------------

1. Checkout release branch.

2. Bump release candidate to release. Commit.
   ::

        hatch --env develop version release

3. Run Towncrier. Commit.
   ::

        hatch --env develop run towncrier build --keep --version ${release_version}

4. Tag.
   ::

        git tag v${release_version}

5. Push release branch and tag to upstream.

6. Wait for the release workflow to complete successfully.

7. Clean up news fragments to prevent recycling in future releases. Commit.
   ::

        git rm documentation/towncrier/*.rst
        git commit -m "Clean up news fragments."

8. Push cleanup commit to upstream.

9. Cherry-pick Towncrier commits back to ``master`` branch.

Postrelease Patch
-------------------------------------------------------------------------------

1. Checkout release branch.

2. Develop and test patch against branch. Add Towncrier entry. Commit.

3. Bump release to patch or increment patch number. Commit.
   ::

        hatch --env develop version patch

4. Run Towncrier. Commit.
   ::

        hatch --env develop run towncrier build --keep --version ${patch_version}

5. Tag.
   ::

        git tag v${patch_version}

6. Push release branch and tag to upstream.

7. Wait for the release workflow to complete successfully.

8. Clean up news fragments to prevent recycling in future releases. Commit.
   ::

        git rm documentation/towncrier/*.rst
        git commit -m "Clean up news fragments."

9. Push cleanup commit to upstream.

10. Cherry-pick patch and Towncrier commits back to ``master`` branch,
    resolving conflicts as necessary.


Copier Updates
===============================================================================

The project was created from a Copier template. To update from the template:

1. Ensure the working directory is clean (commit or stash changes).

2. Run the update command:
   ::

        copier update --answers-file .auxiliary/configuration/copier-answers.yaml

.. note:: The update process preserves your answers from the previous template
          generation. You can override specific answers using the ``--data``
          option with the update command.