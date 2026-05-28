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

<a id="validation"></a>
# Validation

Code validation ensures quality, consistency, and correctness before submitting
contributions.

This guide defines language-neutral validation expectations. For Python command
wrappers and toolchain specifics, see the
[Python validation guide](validation-python.md).

<a id="validation-outcomes"></a>
## Validation Outcomes

Project validation should cover the following outcomes:

- **Code Quality**: Linting and static quality checks pass.
- **Static Analysis**: Type and semantic checks pass where configured.
- **Automated Tests**: Fast local tests and comprehensive suites both pass.
- **Documentation Quality**: Documentation builds cleanly, including configured
  link and doctest checks.
- **Packaging/Distribution**: Build and packaging steps pass for projects that
  publish artifacts.

<a id="workflow"></a>
## Workflow

1. **During Development**: Run the fastest test and lint checks available for
   quick feedback loops.
2. **Before Committing**: Run language-specific quality and type checks.
3. **Before Pull Requests**: Run the project's comprehensive validation suite,
   including packaging and documentation checks where applicable.

<a id="language-specific-overlays"></a>
## Language-Specific Overlays

- [Python validation guide](validation-python.md) - Python validation commands
  and workflow.

All required validation commands must pass before contributions can be accepted.
If Git pre-commit and pre-push hooks are installed for a project, they should
automatically enforce a portion of this workflow.
