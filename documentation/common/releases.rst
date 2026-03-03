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

This guide defines language-neutral release expectations and lifecycle
checkpoints. For Python-specific release commands and changelog mechanics, see
:doc:`releases-python`.

The project follows `semantic versioning <https://semver.org/>`_ for release
versioning.

Release Lifecycle
===============================================================================

Plan releases as explicit phases:

1. **Preparation**: Confirm branch hygiene, quality gates, and pending release
   notes.
2. **Candidate**: Produce a release candidate and validate artifacts.
3. **Finalization**: Promote candidate to final release and publish.
4. **Follow-Up**: Clean up release metadata and merge release-only changes back
   into the main development line.

Pre-Release Quality Gate
===============================================================================

Before creating or promoting a release candidate:

* Ensure the branch is current and clean.
* Run the project's full validation workflow.
* Confirm release notes/changelog entries are complete.
* Confirm automation credentials and publishing workflows are healthy.

Branching and Tagging
===============================================================================

* Use a stable branching convention for release and patch flows.
* Apply consistent annotated tags for release versions.
* Keep tag names and branch names machine-friendly and predictable.
* Record release metadata in commit history to support traceability.

Patch Releases
===============================================================================

For post-release fixes:

1. Branch from the supported release line.
2. Apply and validate the patch.
3. Update release notes/changelog metadata.
4. Tag and publish the patch release.
5. Integrate patch-only commits back to the primary development branch.

Changelog Discipline
===============================================================================

* Maintain release notes as part of normal development.
* Keep entries concise and user-centered.
* Describe what changed and why it matters.
* Acknowledge contributors where appropriate.

A changelog entry should generally:

* Start with a capital letter.
* End with a period.
* Use present-tense imperative/subjunctive phrasing in the lead sentence.
* Avoid implementation-only details unless user impact requires them.

Post-Release Checklist
===============================================================================

After publication:

* Verify release automation completion and artifact availability.
* Clean up temporary release-only metadata.
* Synchronize release branch deltas back to the main branch.
* Update internal tracking for the next development cycle.

Language-Specific Overlays
===============================================================================

* :doc:`releases-python` - Python-specific release commands and changelog
  workflow.
