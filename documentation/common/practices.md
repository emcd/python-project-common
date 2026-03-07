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

<a id="practices"></a>
# Practices

This guide covers language-neutral code organization, design patterns, and
architectural principles. For formatting and visual presentation guidance, see
the [code style guide](style.rst).

<a id="general-principles"></a>
## General Principles

<a id="documentation-standards"></a>
### Documentation Standards

<a id="command-examples"></a>
#### Command Examples

- Use long option names, whenever possible, in command line examples. Readers,
  who are unfamiliar with a command, should not have to look up the meanings of
  single-character option names.

  **❌ Avoid:**

  ```shell
  git log -n 5 --oneline
  docker run -d -p 8080:80 -v /data:/app/data nginx
  ```

  **✅ Prefer:**

  ```shell
  git log --max-count=5 --oneline
  docker run --detach --publish 8080:80 --volume /data:/app/data nginx
  ```

- Write for readers who may be unfamiliar with the tools being demonstrated.
  Provide context and explanation for complex command sequences.

<a id="quality-assurance"></a>
### Quality Assurance

- Install project Git hooks as described in the
  [environment guide](environment.md) to reduce turnaround from avoidable
  validation failures.

- Run the validation workflow documented in the
  [validation guide](validation.md) before opening pull requests.

- Consider maintaining or improving code coverage when practical. Even if code
  coverage is already high, continue adding tests for unaddressed behavioral
  paths.

<a id="architectural-principles"></a>
### Architectural Principles

- **Robustness Principle (Postel's Law)**: Be conservative in what you emit and
  liberal in what you accept.
- **Immutability First**: Prefer immutable structures when internal mutability
  is not required.
- **Dependency Injection**: Prefer explicit dependencies with sensible defaults
  over hidden globals.
- **Exception Chaining**: Never silently swallow exceptions; chain or handle
  them explicitly with context.

<a id="language-and-workflow-overlays"></a>
## Language And Workflow Overlays

Use language-specific practice guides when available:

- [Python development guide](practices-python.rst) - Python-specific development
  patterns.
- [Rust development guide](practices-rust.rst) - Rust-specific development
  patterns.
- [TOML configuration practices](practices-toml.rst) - TOML-specific
  configuration patterns.

Use workflow overlays only when they match your language/toolchain:

- [Python environment guide](environment-python.rst) - Python tooling and
  environment workflow.
- [Python validation guide](validation-python.rst) - Python validation command
  wrappers.
- [Python testing guide](tests-python.rst) - Python testing patterns and
  commands.
- [Python release guide](releases-python.rst) - Python release workflow and
  changelog mechanics.

Use the language-neutral core guides alongside language-specific overlays:
[environment guide](environment.md), [validation guide](validation.md),
[testing guide](tests.md), and [release guide](releases.md).
