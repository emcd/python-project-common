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
Releases
*******************************************************************************

The project follows `semantic versioning <https://semver.org/>`_ for releases.

Release Process
===============================================================================

Initial Release Candidate
-------------------------------------------------------------------------------

1. Checkout ``master`` branch.

2. Pull from upstream to ensure all changes have been synced.

3. Checkout new release branch: ``release-<major>.<minor>``.

4. Bump alpha to release candidate. Commit.
   ::

        hatch version rc

5. Tag.
   ::

        git tag v${rc_version}

6. Push release branch and tag to upstream with tracking enabled.

7. Checkout ``master`` branch.

8. Bump alpha to next minor version on ``master`` branch. Commit.
   ::

        hatch version minor,alpha

9. Tag start of development for next release.
    ::

        git tag i${next_release_version}

Release
-------------------------------------------------------------------------------

1. Checkout release branch.

2. Bump release candidate to release. Commit.
   ::

        hatch version release

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

        git rm .auxiliary/data/towncrier/*.rst
        git commit -m "Clean up news fragments."

8. Push cleanup commit to upstream.

9. Cherry-pick Towncrier commits back to ``master`` branch.

Postrelease Patch
-------------------------------------------------------------------------------

1. Checkout release branch.

2. Develop and test patch against branch. Add Towncrier entry. Commit.

3. Bump release to patch or increment patch number. Commit.
   ::

        hatch version patch

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

        git rm .auxiliary/data/towncrier/*.rst
        git commit -m "Clean up news fragments."

9. Push cleanup commit to upstream.

10. Cherry-pick patch and Towncrier commits back to ``master`` branch,
    resolving conflicts as necessary.

Changelog Entries
===============================================================================

The project uses `Towncrier <https://towncrier.readthedocs.io/en/stable/>`_ to
manage its changelog. When making changes that should be noted in the
changelog, add a file ("fragment") to the ``.auxiliary/data/towncrier``
directory with of ``<issue_number>.<type>.rst``, for changes with a Github
issue, or ``+<title>.<type>.rst``, for changes without an associated issue
number.

The entries will be collected and organized when a release is made, as
described in the release process sections above.

Available Types
-------------------------------------------------------------------------------

* ``enhance``: features and other improvements (documentation, platform
  support, etc...)
* ``notify``: deprecations and other notices
* ``remove``: removals of feature or platform support
* ``repair``: bug fixes

Format
-------------------------------------------------------------------------------

The file should contain a concise description of the change written in present
tense. For example:

.. code-block:: rst
   :caption: .auxiliary/data/towncrier/+immutable-modules.enhance.rst

   Add support for immutable module reclassification.

The description should:

* Start with a capital letter.
* End with a period.
* For multi-component or multi-faceted projects, a topic followed by colon may
  be used to introduce the content. (E.g., "Github Actions: ", "Copier
  Template: ").
* Use present tense verbs in the imperative/subjunctive mood (e.g., "Add",
  "Fix", "Update") or simple noun phrases (e.g., "Support for <x>") in the
  introductory sentence.
* If explanatory content is necessary, then it may be provided in the
  indicative mood using whatever verb tense is most natural to provide
  historical context or other rationale.
* Focus on the what and why, not the how.
* Be understandable by users, not just developers.
* Acknowledge contributors.

Examples
-------------------------------------------------------------------------------

Enhance:
    .. code-block:: rst
       :caption: .auxiliary/data/towncrier/457.enhance.rst

       Improve release process documentation with Towncrier details.

Enhance:
    .. code-block:: rst
       :caption: .auxiliary/data/towncrier/458.enhance.rst

       Add recursive module reclassification support.

Enhance:
    .. code-block:: rst
       :caption: .auxiliary/data/towncrier/459.enhance.rst

       Support for Python 3.13.

Notice:
    .. code-block:: rst
       :caption: .auxiliary/data/towncrier/+exceptions.notify.rst

       Deprecate ``OvergeneralException``. Package now raises more specific
       exceptions.

Remove:
    .. code-block:: rst
       :caption: .auxiliary/data/towncrier/460.remove.rst

       Remove deprecated ``make_immutable`` function.

Repair:
    .. code-block:: rst
       :caption: .auxiliary/data/towncrier/456.repair.rst

       Fix attribute visibility in immutable modules.
