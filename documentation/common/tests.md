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

<a id="tests"></a>
# Tests

This guide defines language-neutral testing expectations and patterns.
For Python-specific commands and examples, see the
[Python testing guide](tests-python.md).

<a id="core-testing-principles"></a>
## Core Testing Principles

- Test observable behavior through public contracts, not private structure.
- Prefer dependency injection and explicit interfaces over global state
  mutation.
- Keep tests deterministic and isolated from external mutable systems.
- Design tests to run quickly in normal development loops.
- Target comprehensive line and branch coverage where practical.
- Align tests with capability contracts so they remain stable when internal
  organization changes.

<a id="public-contracts-and-internal-visibility"></a>
## Public Contracts and Internal Visibility

Prefer tests that exercise the same surface callers use in production:

- Call public APIs, CLI entry points, library exports, and other observable
  interfaces.
- Assert on return values, errors, side effects, and externally visible
  state rather than private helpers or module layout.
- When behavior is hard to reach through the public surface, treat that as a
  design signal first. Introduce a narrow dependency-injection seam or
  reconsider the boundary before reaching for test-only access.

Do not distort the product API for coverage:

- Do not widen internal visibility, export test-only helpers, or add
  documentation-hidden public escape hatches merely so tests can reach
  implementation details.
- Do not restructure modules solely to make private names importable from
  external test packages when a cleaner seam would preserve the intended
  boundary.

Narrow exceptions remain valid:

- Genuinely private algorithms may need focused unit tests when no public
  path exercises the same behavior and widening the API would leak
  implementation surface.
- Such exceptions should stay small, local, and justified. Prefer a clean
  injection point over permanent visibility changes.
- Language-specific overlays describe how to express these exceptions
  without turning them into a convenience default. See the
  [Rust development guide](practices-rust.md#testing) for Rust
  `#[cfg(test)]` policy.

<a id="anti-patterns-to-avoid"></a>
## Anti-Patterns to Avoid

- **Testing against live external services**: Use test doubles for network,
  cloud, and other remote dependencies.
- **Over-mocking internal logic**: Excessive mocking can hide real
  integration and contract failures.
- **API distortion for tests**: Widening visibility or exporting test-only
  helpers solely to reach internals couples tests to private structure and
  grows unintended public surface.
- **Hidden global coupling**: Tests should not rely on implicit ordering,
  process-global state, or residue from previous tests.
- **Broad exception suppression**: Avoid swallowing failures in tests. Keep
  assertions specific and explicit.

<a id="test-organization"></a>
## Test Organization

Use a predictable test layout with clear ownership and purpose:

```text
tests/
├── README.md          # Project-specific conventions and numbering notes
├── data/              # Fixtures, snapshots, mock payloads
├── unit/              # Fast unit tests around public contracts
├── integration/       # Multi-component and boundary tests
└── smoke/             # High-value, end-to-end sanity checks
```

Recommendations:

- Group tests by public capability rather than private source structure where
  possible.
- Keep naming stable and descriptive.
- If your project uses numbered test naming, document the numbering scheme in
  `tests/README.md` and keep it current.

<a id="test-data-and-fixtures"></a>
## Test Data and Fixtures

- Store reusable fixtures under `tests/data/` with topic-based subdirectories.
- Prefer minimal fixtures scoped to the test purpose.
- Keep snapshot and artifact fixtures reviewable and intentionally versioned.
- Use generated data for high-cardinality cases when static fixtures become
  difficult to maintain.

<a id="validation-workflow"></a>
## Validation Workflow

1. During development, run the fastest relevant tests continuously.
2. Before commit, run language-specific quality checks and targeted test suites.
3. Before pull request, run the comprehensive project validation suite.

Use stack-specific overlays for command wrappers and tooling conventions.

<a id="coverage-strategy"></a>
## Coverage Strategy

- Treat coverage as a quality signal, not a substitute for thoughtful test
  design.
- Cover normal behavior, error behavior, and boundary behavior.
- Use exclusion pragmas only as a last resort and document why they are needed.

<a id="troubleshooting-approach"></a>
## Troubleshooting Approach

When tests are hard to write or unstable:

1. Reassess interface boundaries and dependency injection points.
2. Replace implicit dependencies with explicit constructor/function parameters.
3. Reduce fixture complexity and isolate the failing scenario.
4. Prefer small, composable tests over broad multi-concern tests.
5. Capture the rationale for unavoidable compromises in `tests/README.md`.

<a id="language-specific-overlays"></a>
## Language-Specific Overlays

- [Python testing guide](tests-python.md) - Python-specific test patterns and
  commands.
- [Rust development guide](practices-rust.md#testing) - Rust test layout and
  `#[cfg(test)]` boundaries.
