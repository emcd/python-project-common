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
Code Style
*******************************************************************************

This guide covers **formatting and visual presentation** of code. For guidance
on code organization, patterns, and architectural decisions, see :doc:`practices`.

For comprehensive language-specific development guidance (including formatting), see:

* :doc:`practices-python` - Python development guide with formatting standards
* :doc:`practices-rust` - Rust development guide with formatting standards  
* :doc:`practices-toml` - TOML configuration guide with formatting standards

This document provides general principles applicable to all languages.

General
===============================================================================

Lines and Spaces
-------------------------------------------------------------------------------

* Use spaces between identifiers and other tokens. Modern writing systems use
  this convention, which emerged around the 7th century of the Common Era, to
  improve readability. Computer code can generally be written this way too...
  also to improve readability.

* No more than 79 columns for code lines. (Borrowed from the Python :pep:`8`
  guidelines.) Consider the following:

  - Will long lines display well on laptop screens? (Might not be hooked up to
    a larger monitor while flying or in a meeting.)

  - Will long lines display well in side-by-side code panes with enlarged font
    sizes? (Enlarged font sizes are used to reduce eye strain and allow people
    to code without visual correction.)

Vertical Compactness
-------------------------------------------------------------------------------

* Loop bodies, condition bodies, and exception handlers, which consist of a
  single statement and which are sufficiently short, should be placed on the
  same line as the statement that introduces the body.

  **❌ Avoid:**

  .. code-block:: python

      if not data:
          return None

      for item in items:
          process( item )

      try:
          value = risky_operation( )
      except ValueError:
          return default_value

  **✅ Prefer:**

  .. code-block:: python

      if not data: return None

      for item in items: process( item )

      try: value = risky_operation( )
      except ValueError: return default_value

* Blank lines should not be used to group statements within a function body. If
  you need to group statements within a function body, then perhaps the
  function should be refactored. Similarly, avoid obvious comments. Only
  include comments which explain subtle nuances or reference external
  documentation for additional context.

  **❌ Avoid:**

  .. code-block:: python

      def complex_process(data: __.cabc.Mapping[ str, __.typx.Any ] ) -> dict[ str, __.typx.Any ]:
          # First phase - validation
          if not data: raise ValueError( "No data." )
          validated = validate_data( data )

          # Second phase - processing
          processed = transform_data( validated )
          cleaned = clean_data( processed )

          # Final phase - output
          result = format_output( cleaned )
          return result

  **✅ Prefer:**

  .. code-block:: python

      def complex_process(
          data: __.cabc.Mapping[ str, __.typx.Any ]
      ) -> dict[ str, __.typx.Any ]:
          if not data: raise ValueError( "No data." )
          validated = validate_data( data )
          processed = transform_data( validated )
          cleaned = clean_data( processed )
          result = format_output( cleaned )
          return result

* Function bodies should not be longer than thirty (30) lines. I.e., one should
  not have to scroll to read a function.


Language-Specific Development Guides
===============================================================================

For comprehensive development guidance including formatting standards:

* :doc:`practices-python` - Python development guide 
* :doc:`practices-rust` - Rust development guide
* :doc:`practices-toml` - TOML configuration guide


Automation
===============================================================================

* Currently, there are no tools which can automatically enforce compliance with
  the above style guidance. However, if you politely ask an LLM, which is good
  at instruction following, to make your code conform to the guidance, results
  will generally be good. If you are familiar with ``isort`` and ``yapf``, you
  can also look at :doc:`python-autoformat` for approximate formatter
  configurations for these tools.

* Cases where manual intervention may be needed:

  - Multi-line chains of method invocations. (Fluent programming.)
  - Function declarations with mixed positional and nominative arguments.
  - Nested data structures with mixed single-line and multi-line sections.

* When in doubt, optimize for readability while staying within the general
  principles outlined in this guide.
