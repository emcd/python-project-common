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
Rust Code Style
*******************************************************************************

This guide covers **Rust-specific formatting and visual presentation** of code.
For general formatting principles applicable to all languages, see the main :doc:`style`.
For guidance on code organization, patterns, and architectural decisions, see :doc:`practices-rust`.

Formatting Standards
===============================================================================

* Follow the standard Rust formatting conventions enforced by ``rustfmt``.
  The project's ``.rustfmt.toml`` configuration defines the specific formatting rules.

* Use ``cargo fmt`` to automatically format code according to project standards.

* Maximum line length follows the general project standard of 79 columns,
  which may be configured in ``.rustfmt.toml`` if different from Rust defaults.

Naming Conventions
===============================================================================

* Follow standard Rust naming conventions as defined in the Rust API Guidelines:

  - **Types, traits, enums**: ``PascalCase``
  - **Functions, variables, modules**: ``snake_case``  
  - **Constants, statics**: ``SCREAMING_SNAKE_CASE``
  - **Macros**: ``snake_case`` (by convention, though not enforced)

* Apply project nomenclature guidelines from :doc:`nomenclature` when naming
  types, functions, and variables.

Documentation
===============================================================================

* Use standard Rust documentation comments (``///`` for items, ``//!`` for modules).

* Write documentation in narrative mood (third person) consistent with Python
  docstring conventions in the project.

  **✅ Prefer:**

  .. code-block:: rust

      /// Validates the configuration data.
      /// 
      /// Returns the validated configuration or an error if validation fails.
      pub fn validate_configuration(config: &Config) -> Result<Config, ConfigError> {
          // implementation
      }

  **❌ Avoid:**

  .. code-block:: rust

      /// Validate the configuration data.
      pub fn validate_configuration(config: &Config) -> Result<Config, ConfigError> {
          // implementation  
      }

Future Expansion
===============================================================================

.. todo::

   Expand this guide with comprehensive coverage including:
   
   - Import organization and module structure
   - Trait implementation patterns  
   - Macro definition and usage formatting
   - Async/await formatting patterns
   - Complex type alias formatting
   - Pattern matching formatting
   - Struct and enum definition formatting