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
Practices
*******************************************************************************

This guide covers language-neutral code organization, design patterns, and
architectural principles. For formatting and visual presentation guidance, see
:doc:`style`.

General Principles
===============================================================================

Documentation Standards
-------------------------------------------------------------------------------

Command Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Use long option names, whenever possible, in command line examples. Readers,
  who are unfamiliar with a command, should not have to look up the meanings of
  single-character option names.

  **❌ Avoid:**

  .. code-block:: shell

      git log -n 5 --oneline
      docker run -d -p 8080:80 -v /data:/app/data nginx

  **✅ Prefer:**

  .. code-block:: shell

      git log --max-count=5 --oneline
      docker run --detach --publish 8080:80 --volume /data:/app/data nginx

* Write for readers who may be unfamiliar with the tools being demonstrated.
  Provide context and explanation for complex command sequences.

Quality Assurance
-------------------------------------------------------------------------------

* Install project Git hooks as described in :doc:`environment` to reduce
  turnaround from avoidable validation failures.

* Run the validation workflow documented in :doc:`validation` before opening
  pull requests.

* Consider maintaining or improving code coverage when practical. Even if code
  coverage is already high, continue adding tests for unaddressed behavioral
  paths.

Architectural Principles
-------------------------------------------------------------------------------

* **Robustness Principle (Postel's Law)**: Be conservative in what you emit and
  liberal in what you accept.
* **Immutability First**: Prefer immutable structures when internal mutability
  is not required.
* **Dependency Injection**: Prefer explicit dependencies with sensible defaults
  over hidden globals.
* **Exception Chaining**: Never silently swallow exceptions; chain or handle
  them explicitly with context.

Language-Specific Overlays
===============================================================================

* :doc:`practices-python` - Python-specific development patterns.
* :doc:`practices-rust` - Rust-specific development patterns.
* :doc:`practices-toml` - TOML-specific configuration patterns.
* :doc:`environment-python` - Python tooling and environment workflow.
* :doc:`validation-python` - Python validation command wrappers.
* :doc:`tests-python` - Python testing patterns and commands.
* :doc:`releases-python` - Python release workflow and changelog mechanics.

.. toctree::
   :hidden:

   practices-python
   practices-rust
   practices-toml
