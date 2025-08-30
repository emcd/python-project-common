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
Rust Development Practices
*******************************************************************************

This guide covers **Rust-specific code organization, patterns, and architectural decisions**.
For general guidance applicable to all languages, see the main :doc:`practices`.
For guidance on code formatting and visual presentation, see the :doc:`style-rust`.

Module Organization
===============================================================================

* Follow standard Rust module organization patterns:

  - ``src/lib.rs`` or ``src/main.rs`` as the crate root
  - Use ``src/module.rs`` files with ``src/module/`` directories for submodules
  - Organize related functionality into logical modules
  - Re-export important items at appropriate levels using ``pub use``

* Apply project nomenclature guidelines from :doc:`nomenclature` when naming
  modules, following Rust's ``snake_case`` convention for module names.


Documentation
===============================================================================

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