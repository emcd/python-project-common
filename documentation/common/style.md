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

<a id="code-style"></a>
# Code Style

This guide covers language-neutral formatting and visual presentation
principles. For broader design and architecture guidance, see the
[practices guide](practices.md).

<a id="general"></a>
## General

<a id="lines-and-spaces"></a>
### Lines and Spaces

- Use spaces between identifiers and other tokens. Modern writing systems use this convention, which emerged around the 7th century of the Common Era, to improve readability. Computer code can generally be written this way too... also to improve readability.
- No more than 79 columns for code lines. (Borrowed from the Python [PEP 8](https://peps.python.org/pep-0008/)
  guidelines.) Consider the following:
  - Will long lines display well on laptop screens? (Might not be hooked up to a larger monitor while flying or in a meeting.)
  - Will long lines display well in side-by-side code panes with enlarged font sizes? (Enlarged font sizes are used to reduce eye strain and allow people to code without visual correction.)

<a id="vertical-compactness"></a>
### Vertical Compactness

- Loop bodies, condition bodies, and exception handlers, which consist of a single statement and which are sufficiently short, should be placed on the same line as the statement that introduces the body.

  **❌ Avoid:**

  ``` python
  if not data:
      return None

  for item in items:
      process( item )

  try:
      value = risky_operation( )
  except ValueError:
      return default_value
  ```

  **✅ Prefer:**

  ``` python
  if not data: return None

  for item in items: process( item )

  try: value = risky_operation( )
  except ValueError: return default_value
  ```

- Blank lines should not be used to group statements within a function body. If you need to group statements within a function body, then perhaps the function should be refactored. Similarly, avoid obvious comments. Only include comments which explain subtle nuances or reference external documentation for additional context.

  **❌ Avoid:**

  ``` python
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
  ```

  **✅ Prefer:**

  ``` python
  def complex_process(
      data: __.cabc.Mapping[ str, __.typx.Any ]
  ) -> dict[ str, __.typx.Any ]:
      if not data: raise ValueError( "No data." )
      validated = validate_data( data )
      processed = transform_data( validated )
      cleaned = clean_data( processed )
      result = format_output( cleaned )
      return result
  ```

- Function bodies should not be longer than thirty (30) lines. I.e., one should not have to scroll to read a function.

<a id="language-specific-overlays"></a>
## Language-Specific Overlays

- [Python development guide](practices-python.md) - Python formatting
  and style details.
- [Rust development guide](practices-rust.md) - Rust formatting and style
  details.
- [TOML configuration practices](practices-toml.md) - TOML formatting and
  style details.

<a id="automation"></a>
## Automation

- Use language-appropriate formatters and linters where available. These tools reduce routine style drift and let reviews focus on behavior and design.
- When automatic formatting support is incomplete, apply these conventions manually and keep formatting decisions consistent within each file.
- Cases where manual intervention may be needed:
  - Multi-line chains of method invocations. (Fluent programming.)
  - Function declarations with mixed positional and nominative arguments.
  - Nested data structures with mixed single-line and multi-line sections.
- When in doubt, optimize for readability while staying within the general principles outlined in this guide.
