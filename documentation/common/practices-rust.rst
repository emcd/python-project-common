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
Rust Development Guide
*******************************************************************************

This guide covers **comprehensive Rust development guidance including code organization, 
patterns, architectural decisions, and formatting standards**. For general guidance 
applicable to all languages, see the main :doc:`practices`.

Module Organization
===============================================================================

* Follow standard Rust module organization patterns:

  - ``src/lib.rs`` or ``src/main.rs`` as the crate root
  - Use ``src/module.rs`` files with ``src/module/`` directories for submodules
  - Organize related functionality into logical modules
  - Re-export important items at appropriate levels using ``pub use``

* Apply project nomenclature guidelines from :doc:`nomenclature` when naming
  modules, following Rust's ``snake_case`` convention for module names.

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

Content Standards
-------------------------------------------------------------------------------

* Write documentation comments in narrative mood (third person) consistent with
  project documentation standards.

* Use standard Rust documentation patterns:

  - ``///`` for public API documentation
  - ``//!`` for module-level documentation
  - Include examples in documentation when helpful

* Document error conditions using the standard ``# Errors`` section:

  .. code-block:: rust

      /// Validates user configuration.
      ///
      /// # Errors
      ///
      /// Returns `CrateError::Validation` if the configuration is invalid.
      pub fn validate_config(config: &Config) -> Result<(), CrateError> {
          // implementation
      }

Visual Formatting
-------------------------------------------------------------------------------

* Use standard Rust documentation comments (``///`` for items, ``//!`` for modules).

* Write documentation in narrative mood (third person) consistent with project
  documentation conventions.

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

Formatting Standards
===============================================================================

* Follow the standard Rust formatting conventions enforced by ``rustfmt``.
  The project's ``.rustfmt.toml`` configuration defines the specific formatting rules.

* Use ``cargo fmt`` to automatically format code according to project standards.

* Maximum line length follows the general project standard of 79 columns,
  which may be configured in ``.rustfmt.toml`` if different from Rust defaults.

Future Development
===============================================================================

.. todo::

   Expand Rust practices with comprehensive coverage including:
   
   - Error handling patterns and hierarchies
   - Type design (wide/narrow principle, newtype patterns)
   - Immutability and ownership best practices
   - Async/await patterns and best practices
   - Trait design and implementation guidelines  
   - Macro definition patterns
   - FFI and unsafe code guidelines
   - Performance optimization patterns
   - Testing strategies and patterns
   - Concurrent programming patterns