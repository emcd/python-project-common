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
Tests
*******************************************************************************

This guide defines language-neutral testing expectations and patterns.
For Python-specific commands and examples, see :doc:`tests-python`.

Core Testing Principles
===============================================================================

* Test observable behavior, not implementation details.
* Prefer dependency injection and explicit interfaces over global state
  mutation.
* Keep tests deterministic and isolated from external mutable systems.
* Design tests to run quickly in normal development loops.
* Target comprehensive line and branch coverage where practical.

Anti-Patterns to Avoid
===============================================================================

* **Testing against live external services**: Use test doubles for network,
  cloud, and other remote dependencies.
* **Over-mocking internal logic**: Excessive mocking can hide real
  integration and contract failures.
* **Hidden global coupling**: Tests should not rely on implicit ordering,
  process-global state, or residue from previous tests.
* **Broad exception suppression**: Avoid swallowing failures in tests. Keep
  assertions specific and explicit.

Test Organization
===============================================================================

Use a predictable test layout with clear ownership and purpose:

::

    tests/
    ├── README.md          # Project-specific conventions and numbering notes
    ├── data/              # Fixtures, snapshots, mock payloads
    ├── unit/              # Fast unit tests around public contracts
    ├── integration/       # Multi-component and boundary tests
    └── smoke/             # High-value, end-to-end sanity checks

Recommendations:

* Group tests by public capability rather than private source structure where
  possible.
* Keep naming stable and descriptive.
* If your project uses numbered test naming, document the numbering scheme in
  ``tests/README.md`` and keep it current.

Test Data and Fixtures
===============================================================================

* Store reusable fixtures under ``tests/data/`` with topic-based
  subdirectories.
* Prefer minimal fixtures scoped to the test purpose.
* Keep snapshot and artifact fixtures reviewable and intentionally versioned.
* Use generated data for high-cardinality cases when static fixtures become
  difficult to maintain.

Validation Workflow
===============================================================================

1. During development, run the fastest relevant tests continuously.
2. Before commit, run language-specific quality checks and targeted test suites.
3. Before pull request, run the comprehensive project validation suite.

Use stack-specific overlays for command wrappers and tooling conventions.

Coverage Strategy
===============================================================================

* Treat coverage as a quality signal, not a substitute for thoughtful test
  design.
* Cover normal behavior, error behavior, and boundary behavior.
* Use exclusion pragmas only as a last resort and document why they are needed.

Troubleshooting Approach
===============================================================================

When tests are hard to write or unstable:

1. Reassess interface boundaries and dependency injection points.
2. Replace implicit dependencies with explicit constructor/function parameters.
3. Reduce fixture complexity and isolate the failing scenario.
4. Prefer small, composable tests over broad multi-concern tests.
5. Capture the rationale for unavoidable compromises in ``tests/README.md``.

Language-Specific Overlays
===============================================================================

* :doc:`tests-python` - Python-specific test patterns and commands.

.. toctree::
   :hidden:

   tests-python
