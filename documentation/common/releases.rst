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

Pre-Release Quality Check
-------------------------------------------------------------------------------

Run local quality assurance before any release process::

    git status && git pull origin master
    hatch --env develop run linters
    hatch --env develop run testers
    hatch --env develop run docsgen

Also, ensure that at least one news fragment exists under
``.auxiliary/data/towncrier``.

Initial Release Candidate
-------------------------------------------------------------------------------

1. **Branch Setup**: Checkout ``master`` branch and ensure it's up to date::

        git checkout master
        git pull origin master

2. **Create Release Branch**: Checkout new release branch::

        git checkout -b release-<major>.<minor>

3. **Version Bump**: Bump alpha to release candidate and commit::

        hatch version rc
        git commit -am "Version: $(hatch version)"

4. **Tag Release Candidate**::

        git tag -m "Release candidate v$(hatch version)." v$(hatch version)

5. **Push Branch and Tag**: Push release branch and tag to upstream::

        git push -u origin release-<major>.<minor>
        git push --tags

6. **Setup Next Development Cycle**: Return to ``master`` and prepare for next
   version::

        git checkout master
        hatch version minor,alpha
        git commit -am "Version: $(hatch version)"
        git tag -m "Start development for v$(hatch version | sed 's/a[0-9]*$//')." i$(hatch version | sed 's/a[0-9]*$//')
        git push origin master --tags

Final Release
-------------------------------------------------------------------------------

1. **Branch Setup**: Checkout and update the release branch::

        git checkout release-<major>.<minor>
        git pull origin release-<major>.<minor>

2. **Version Finalization**: Bump release candidate to final release::

        hatch version release
        git commit -am "Version: $(hatch version)"

3. **Changelog Generation**: Run Towncrier to build final changelog::

        hatch --env develop run towncrier build --keep --version $(hatch version)
        git commit -am "Update changelog for v$(hatch version) release."

4. **Release Tag**: Create signed release tag::

        git tag -m "Release v$(hatch version): <brief-description>." v$(hatch version)

5. **Push Release**: Push release branch and tag to upstream::

        git push origin release-<major>.<minor>
        git push --tags

6. **Monitor Release**: Wait for the release workflow to complete successfully.
   Check the GitHub Actions tab to monitor progress.

7. **Post-Release Cleanup**: Clean up news fragments and push::

        git rm .auxiliary/data/towncrier/*.rst
        git commit -m "Clean up news fragments."
        git push origin release-<major>.<minor>

8. **Master Integration**: Cherry-pick release commits back to ``master``::

        git checkout master
        git pull origin master
        git cherry-pick <changelog-commit-hash>
        git cherry-pick <cleanup-commit-hash>
        git push origin master

   Use ``git log --oneline`` on the release branch to identify commit hashes.

Postrelease Patch
-------------------------------------------------------------------------------

1. **Branch Setup**: Checkout and update the release branch::

        git checkout release-<major>.<minor>
        git pull origin release-<major>.<minor>

2. **Patch Development**: Develop and test patch against branch.
   Add Towncrier entry and commit changes.

3. **Pre-Patch Validation**: Run quality checks to catch issues early::

        hatch --env develop run linters

   **Important**: Fix any linting errors before proceeding.

4. **Version Bump**: Bump to patch version and commit::

        hatch version patch
        git commit -am "Version: $(hatch version)"

5. **Changelog Generation**: Run Towncrier to build patch changelog::

        hatch --env develop run towncrier build --keep --version $(hatch version)
        git commit -am "Update changelog for v$(hatch version) patch release."

6. **Patch Tag**: Create signed patch tag::

        git tag -m "Release v$(hatch version) patch: <brief-description>." v$(hatch version)

7. **Push Patch**: Push release branch and tag to upstream::

        git push origin release-<major>.<minor>
        git push --tags

8. **Monitor Release**: Wait for the release workflow to complete successfully.
   Check the GitHub Actions tab to monitor progress.

9. **Post-Release Cleanup**: Clean up news fragments and push::

        git rm .auxiliary/data/towncrier/*.rst
        git commit -m "Clean up news fragments."
        git push origin release-<major>.<minor>

10. **Master Integration**: Cherry-pick patch commits back to ``master``::

        git checkout master
        git pull origin master
        git cherry-pick <patch-commit-hash>
        git cherry-pick <changelog-commit-hash>
        git cherry-pick <cleanup-commit-hash>
        git push origin master

    Use ``git log --oneline`` on the release branch to identify commit hashes.
    Resolve any conflicts as necessary during cherry-picking.

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
