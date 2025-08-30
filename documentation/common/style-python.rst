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
Python Code Style
*******************************************************************************

This guide covers **Python-specific formatting and visual presentation** of code. 
For general formatting principles applicable to all languages, see the main :doc:`style`.
For guidance on code organization, patterns, and architectural decisions, see :doc:`practices-python`.

Lines and Spaces
===============================================================================

* One space after opening delimiters ( ``(``, ``[``, ``{`` ) and one space
  before closing delimiters ( ``)``, ``]``, ``}`` ), *except* inside of
  f-strings and strings to which ``.format`` is applied.

  **✅ Prefer:**

  .. code-block:: python

      func( arg1, arg2 )
      data = [ 1, 2, 3 ]
      config = { 'key': 'value' }

      # Type annotations follow the same spacing rules
      def process(
          items: __.cabc.Sequence[ __.cabc.Mapping[ str, int ] ]
      ) -> dict[ str, bool ]: pass
      ComplexType: __.typx.TypeAlias = __.typx.Union[
          dict[ str, __.typx.Any ],
          list[ str ],
      ]

      # Exception: f-strings and .format
      message = f"Hello {name}."
      template = "Value: {value}".format( value = 42 )

  **❌ Avoid:**

  .. code-block:: python

      func(arg1, arg2)
      data = [1, 2, 3]
      config = {"key": "value"}

      # Wrong: inconsistent bracket spacing in type annotations
      def process( items: __.cabc.Sequence[__.cabc.Mapping[str, int]] ) -> dict[str, bool]: pass

      # Wrong: spaces in f-strings
      message = f"Hello { name }."

* Empty collection literals have a single space between delimiters, ``( )``,
  ``[ ]``, ``{ }``. This includes function definitions and invocations with no
  arguments.

  **✅ Prefer:**

  .. code-block:: python

      empty_list = [ ]
      empty_dict = { }

      def no_args_function( ) -> None: pass
      result = some_function( )

  **❌ Avoid:**

  .. code-block:: python

      empty_list = []
      empty_dict = {}

      def no_args_function(): pass
      result = some_function()

* A space on each side of ``=`` for keyword/nominative arguments.

  **✅ Prefer:**

  .. code-block:: python

      def some_function( magic: int = 42 ) -> int: pass

      result = process( data, timeout = 30 )

  **❌ Avoid:**

  .. code-block:: python

      def some_function(magic=42): pass

      result = process(data, timeout=30)

Vertical Compactness
===============================================================================

Function and Class Definitions
-------------------------------------------------------------------------------

* Keep all arguments on one line if they fit within the line limit.

  **✅ Prefer:**

  .. code-block:: python

      def simple_function( arg1: int, arg2: str = 'default' ) -> bool:
          return True

* When arguments must be split across lines, prefer to group positional and
  keyword arguments.

  **✅ Prefer:**

  .. code-block:: python

      def medium_function(
          first_pos: str, second_pos: int, third_pos: bool,
          first_named: str = 'default', second_named: str = 'other'
      ) -> None: pass

* When grouping would overflow a line, place each argument on its own line.

  **✅ Prefer:**

  .. code-block:: python

      def complex_function(
          first_very_long_positional_argument: __.cabc.Mapping[ str, int ],
          second_very_long_positional_argument: __.cabc.Sequence[ str ],
          first_named_arg: str = 'some very long default value',
          second_named_arg: str = 'another long default value',
      ) -> None: pass

* For multi-line return type annotations using ``Annotated``, place the closing
  bracket and colon on the final line.

  **✅ Prefer:**

  .. code-block:: python

      def complex_function(
          data: UserData
      ) -> __.typx.Annotated[
          ProcessedData,
          __.ddoc.Doc( "Processed user data with validation." ),
          __.ddoc.Raises( ValueError, "If data validation fails." ),
      ]:
          ''' Process user data with comprehensive validation. '''
          pass

* When a single-line form would overflow, always go to a three-or-more-line form
  with the arguments on indented lines between the first and last lines. There
  is no two-line form.

  **✅ Prefer:**

  .. code-block:: python

      def semicomplex_function(
          argument_1: int, argument_2: int, argument_3: str
      ) -> bool: return True

  **❌ Avoid:**

  .. code-block:: python

      def semicomplex_function( argument_1: int, argument_2: int, argument_3: str
      ) -> bool: return True

Collections
-------------------------------------------------------------------------------

* For short collections, keep them on one line.

  **✅ Prefer:**

  .. code-block:: python

      points = [ ( 1, 2 ), ( 3, 4 ), ( 5, 6 ) ]

      config = { 'name': 'example', 'value': 42 }

* For longer collections, split elements one per line with a trailing comma
  after the last element.

  **✅ Prefer:**

  .. code-block:: python

      matrix = [
          [ 1, 2, 3, 4 ],
          [ 5, 6, 7, 8 ],
          [ 9, 10, 11, 12 ],
      ]

      settings = {
          'name': 'example',
          'description': 'A longer example that needs multiple lines',
          'values': [ 1, 2, 3, 4, 5 ],
          'nested': {
              'key1': 'value1',
              'key2': 'value2',
          },
      }

Docstrings
===============================================================================

* Use triple single-quotes for all docstrings with narrative mood (third
  person). The docstring describes what the function does, not what the caller
  should do.

* For single-line docstrings, include one space after the opening quotes and
  before the closing quotes.

  **✅ Prefer:**

  .. code-block:: python

      def example_function( ) -> str:
          ''' An example function. '''

  **❌ Avoid:**

  .. code-block:: python

      def example_function( ):
          """An example function."""

      def example_function( ):
          '''An example function.'''

* For multi-line docstrings, include a newline after the heading and before the
  closing quotes. Indent continuation lines to match the opening quotes. Place
  the closing triple quotes on their own line for multi-line docstrings,
  indented to match the opening quotes.

  **✅ Prefer:**

  .. code-block:: python

      class ExampleClass:
          ''' An example class.

              This class demonstrates proper docstring formatting
              with multiple lines of documentation.
          '''

  **❌ Avoid:**

  .. code-block:: python

      class ExampleClass:
          """An example class.

          This class demonstrates proper docstring formatting
          with multiple lines of documentation.
          """

      class ExampleClass:
          """An example class.

          This class demonstrates proper docstring formatting
          with multiple lines of documentation."""

Imports
===============================================================================

* Follow PEP 8 import grouping conventions with proper visual formatting:

  - imports from ``__future__``
  - stdlib imports
  - imports from stdlib modules
  - third-party imports
  - imports from third-party modules
  - first-party (relative) imports
  - imports from first-party (relative) modules

* For import sequences, which will not fit on one line, use parentheses with
  hanging indent.

  **✅ Prefer:**

  .. code-block:: python

      from third_party.submodule import (
          FirstClass, SecondClass, ThirdClass )

* For import sequences, which will not fit on two lines, list them one per line
  with a trailing comma after each one and the closing parentheses dedented on a
  separate line.

  **✅ Prefer:**

  .. code-block:: python

      from third_party.other import (
          ALongClassName,
          AnotherLongClassName,
          YetAnotherLongClassName,
      )

* Imports within a sequence should be sorted lexicographically with uppercase
  letters coming before lowercase ones (i.e., classes and type aliases before
  functions). Import aliases are relevant to this ordering rather than the
  imports which they alias.

Line Continuation
===============================================================================

* Use parentheses for line continuation. Split at natural points such as dots,
  operators, or after commas. Keep the closing parenthesis on the same line as
  the last element unless the collection has a trailing comma.

* For operator splits, place the operator at the beginning of the split-off
  line, not at the end of the line being split.

  **✅ Prefer:**

  .. code-block:: python

      # Dot operator splits
      result = (
          very_long_object_name.first_method_call( )
          .second_method_call( )
          .final_method_call( ) )

      # Operator splits - operators at beginning of continuation lines
      total = (
          first_long_value * second_long_value
          + third_long_value * fourth_long_value
          - adjustment_factor )

      # Array subscript splits
      element = (
          very_long_array_name[ first_complex_index ]
          [ second_complex_index ]
          [ 'nested_key' ] )

      # List/dict comprehension splits
      squares = [
          value * value
          for value in range( 100 )
          if is_valid( value ) ]

      # Multi-line conditional statements
      if (      is_valid_input( data, strict = True )
            and process_ready( )
            and not maintenance_mode
      ): process( data )

  **❌ Avoid:**

  .. code-block:: python

      # Using backslash continuation
      result = very_long_object_name.first_method_call( ) \
               .second_method_call( ) \
               .final_method_call( )

      # Breaking at unnatural points
      result = very_long_object_name.first_method_call( ).second_method_call(
          ).final_method_call( )

      # Operators at end of line being split
      total = (
          first_long_value * second_long_value +
          third_long_value * fourth_long_value )

Function Invocations
===============================================================================

* For function invocations, generally omit trailing commas after the final
  argument, keeping the closing parenthesis on the same line as the final
  argument.

  **✅ Prefer:**

  .. code-block:: python

      # Single line invocations
      result = process_data( input_file, output_file, strict = True )

      # Multi-line invocations without trailing comma
      result = complex_processing_function(
          very_long_input_parameter,
          another_long_parameter,
          final_parameter = computed_value )

      # Collections still use trailing commas when split
      data = {
          'key1': 'value1',
          'key2': 'value2',  # trailing comma here is good
      }

  **❌ Avoid:**

  .. code-block:: python

      # Unnecessary trailing comma in function call
      result = process_data(
          input_file,
          output_file,
          strict = True, )

      # Closing parenthesis on separate line for function calls
      result = complex_function(
          parameter1,
          parameter2
      )

Multi-line Construct Rules
===============================================================================

* **Function invocations and class instantiations** should place the closing
  ``)`` on the same line as the last argument.

* **Comprehensions and generator expressions** should place the closing
  delimiter on the same line as the last statement.

* **Parenthetical groupings** should place the closing delimiter on the same
  line as the last statement.

* **All other multi-line constructs** (function signatures, annotations, lists,
  dictionaries, etc.) must place the closing delimiter on a separate line
  following the last item and must dedent the closing delimiter to match the
  opening line indentation.

* **Trailing comma rule**: If a closing delimiter is not on the same line as
  the last item in a multi-line construct, then the last item must be followed
  by a trailing comma. The last argument of a function invocation must not be
  followed by a trailing comma.

  **✅ Prefer:**

  .. code-block:: python

      # Function calls: closing ) on same line, no trailing comma
      result = process_data(
          input_file, output_file, strict = True )

      # Comprehensions: closing delimiter on same line
      squares = [ x**2 for x in range( 10 ) if x % 2 == 0 ]

      # Lists/dicts: closing delimiter on separate line, trailing comma
      data = {
          'key1': 'value1',
          'key2': 'value2',
      }

  **❌ Avoid:**

  .. code-block:: python

      # Wrong: trailing comma in function call
      result = process_data(
          input_file, output_file, strict = True, )

      # Wrong: closing delimiter on separate line for function call
      result = process_data(
          input_file, output_file
      )

Strings
===============================================================================

* Use single quotes for plain data strings unless they contain single quotes.
  Use double quotes for f-strings, ``.format`` strings, exception messages,
  and log messages.

* Exception messages and log messages should end with periods for consistency
  and proper sentence structure. Sentence fragments, which end in a colon,
  followed by a value, do not need to end with a period.

  **✅ Prefer:**

  .. code-block:: python

      name = 'example'
      path = 'C:\\Program Files\\Example'

      message = f"Processing {name} at {path}."
      count = "Number of items: {count}".format( count = len( items ) )

      raise ValueError( "Invalid configuration value." )
      logger.error( "Failed to process item." )

  **❌ Avoid:**

  .. code-block:: python

      name = "example"
      path = "C:\\Program Files\\Example"

      message = f'Processing {name} at {path}'
      count = "Number of items: {len(items)}"

      raise ValueError( 'Invalid configuration value' )
      logger.error( 'Failed to process item' )

* Do not use function calls or subscripts inside of f-string expressions. These
  can be opaque to some linters and syntax highlighters. Instead, use strings
  with the ``.format`` method for these cases, where the function calls or
  subscripts are performed on the arguments to ``.format``.

  **✅ Prefer:**

  .. code-block:: python

      "Values: {values}".format( values = ', '.join( values ) )

  **❌ Avoid:**

  .. code-block:: python

      f"Values: {', '.join(values)}"