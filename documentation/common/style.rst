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

* Respect the project code style.

* A summary of the project code style is:

  - **Spacing**: Use spaces between identifiers and other tokens. Modern
    writing systems use this convention, which emerged around the 7th century
    of the Common Era, to improve readability. Computer code can generally be
    written this way too... also to improve readability.

  - **Line Width**: Follow :pep:`8` on this: no more than 79 columns for code
    lines. Consider how long lines affect display on laptops or side-by-side
    code panes with enlarged font sizes. (Enlarged font sizes are used to
    reduce eye strain and allow people to code without visual correction.)

  - **Vertical Compactness**.

    - Function definitions, loop bodies, and condition bodies, which
      consist of a single statement and which are sufficiently short,
      should be placed on the same line as the statement that introduces
      the body.

    - Blank lines should not be used to group statements within a function
      body. If you need to group statements within a function body, then
      perhaps the function should be refactored.

    - Function bodies should not be longer than thirty lines. I.e., one
      should not have to scroll to read a function.

* Pull requests, which attempt to enforce the Python ``black`` style or any
  style other than the project code style, will be rejected.

.. todo:: Rust Guidance


Specific Preferences
===============================================================================

Class and Function Definitions
-------------------------------------------------------------------------------

Keep all arguments on one line if they fit within the line limit::

    def simple_function( arg1: int, arg2: str = 'default' ) -> bool:
        return True

When arguments must be split across lines, prefer to group positional and
nominative arguments::

    def medium_function(
        first_pos, second_pos, third_pos,
        first_named = 'default', second_named = 'other'
    ) -> None: pass

When grouping would overflow a line, place each argument on its own line::

    def complex_function(
        first_very_long_positional_argument: dict,
        second_very_long_positional_argument: list,
        first_named_arg = 'some very long default value',
        second_named_arg = 'another long default value',
    ) -> None: pass

For single-line function bodies, especially ``pass``, keep them on the same
line as the definition when possible::

    def simple_operation( value: int ) -> int: return value * 2

    def stub_function( data: bytes ) -> None: pass

When a single-line form would overflow, always go to the a three-or-more-line
form with the arguments on indented lines between the first and last lines.
There is no two-line form. I.e., do this::

    def semicomplex_function(
        argument_1: int, argument_2: int, argument_3: str
    ) -> bool: return True

and *not* this::

    def semicomplex_function( argument_1: int, argument_2: int, argument_3: str
    ) -> bool: return True


Collections
-------------------------------------------------------------------------------

For short collections, keep them on one line::

    points = [ ( 1, 2 ), ( 3, 4 ), ( 5, 6 ) ]

    config = { 'name': 'example', 'value': 42 }

For longer collections, split elements one per line with a trailing comma after
the last element::

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
-------------------------------------------------------------------------------

* Use triple single-quotes for all docstrings.

* For single-line docstrings, include one space after the opening quotes and
  before the closing quotes:

  .. code-block:: python

      def example_function( ):
          ''' An example function. '''

* For multi-line docstrings, include a newline after the heading and
  before the closing quotes. Indent continuation lines to match the opening
  quotes:

  .. code-block:: python

      class ExampleClass:
          ''' An example class.

              This class demonstrates proper docstring formatting
              with multiple lines of documentation.
          '''

* Place the closing triple quotes on their own line for multi-line docstrings,
  indented to match the opening quotes.


Imports
-------------------------------------------------------------------------------

The project has an internals subpackage, `__`, which contains all common
third-party imports. If your desired import is in this subpackage, then you can
import this subpackage near the top of the module under development; e.g.::

    from . import __

If the internals subpackage does not have your desired import, consider whether
it is a common third-party import, which is likely to be used in other modules
in the future, or whether it is something specialized. If it is a common
third-party import, then add it to the imports in the internals subpackage,
using an abbreviated alias if the name is long. (E.g., ``cabc`` as an alias for
``collections.abc``.)

If your desired import is specialized for the current module, then consider how
widely it will be used within the module. If only one or two functions will
need it and they are not performance-critical, then consider importing from
within the function bodies. (Function-level imports reduce module namespace
pollution and make functions more relocatable since their requisite imports
will move with them.) Otherwise, import at the top of the module, aliasing the
import so that it is private and will not pollute the public API of the module.

Example of function-level imports::

    def process_data( raw_data: bytes ) -> dict:
        from tomli_w import dumps
        from .utils import decode_packet
        # Function implementation...

Example of private module-level import aliases::

    import aiofiles as _aiofiles

    from . import exceptions as _exceptions

.. note::

   The above advice does *not* apply to modules in a test suite. As test
   modules are not intended to expose public APIs, feel free to follow the
   common practice of placing public imports at the tops of those modules.

Follow the import grouping conventions from :pep:`8`::

    # __future__ from imports

    # standard library imports

    # standard library from imports

    # third-party imports

    # third-party from imports

    # first-party relative imports

    # first-party relative from imports

For import sequences, which will not fit on one line, use parentheses with
hanging indent::

    from third_party.submodule import (
        FirstClass, SecondClass, ThirdClass )

For import sequences, which will not fit on two lines, list them one per line
with a trailing comma after each one and the closing parentheses dedented on a
separate line::

    from third_party.other import (
        ALongClassName,
        AnotherLongClassName,
        YetAnotherLongClassName,
    )

Imports within a sequence should be sorted lexicographically with uppercase
letters coming before lowercase ones (i.e., classes and type aliases before
functions). Import aliases are relevant to this ordering rather than the
imports which they alias.


Line Continuation
-------------------------------------------------------------------------------

Use parentheses for line continuation. Split at natural points such as dots,
operators, or after commas. Keep the closing parenthesis on the same line as
the last element unless the collection has a trailing comma::

    # Dot operator splits
    result = (
        very_long_object_name.first_method_call( )
        .second_method_call( )
        .final_method_call( ) )

    # Operator splits
    total = (
        first_long_value * second_long_value
        + third_long_value * fourth_long_value )

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
    if (  validate_input( data, strict = True )
          and process_ready( )
    ): process( data )


Single-Line Statements
-------------------------------------------------------------------------------

Keep simple control flow statements on one line when they contain a single
simple action::

    if not data: return None
    while more_items: process_next( )
    try: value = next( iterator )
    except StopIteration: return

    for item in items: yield item
    with lock: do_work( )

Similarly, keep simple class and function definitions on one line when their
body consists only of ``pass``::

    class EmptyMixin: pass

    def not_implemented_yet( data: bytes ) -> None: pass

However, if the definition includes type annotations or multiple base classes
that would make the line too long, use normal multi-line formatting::

    class SimpleContainer(
        Generic[ _T ],
        cabc.Collection,
        metaclass = ImmutableClass
    ): pass


Spaces
-------------------------------------------------------------------------------

One space after opening delimiters (``(``, ``[``, ``{``) and one space before
closing delimiters (``)``, ``]``, ``}``), *except* inside of f-strings and
strings to which ``.format`` is applied.

Empty collection literals have a single space between delimiters, ``( )``, ``[
]``, ``{ }``. This includes function definitions and invocations with no
arguments.

A space on each side of ``=`` for nominative/keyword arguments::

    def some_function( magic = 42 ): pass

and *not*::

    def some_function(magic=42): pass

Strings
-------------------------------------------------------------------------------

Use single quotes for string literals unless using f-strings, ``.format``
method, or exception and logging messages::

    name = 'example'
    path = 'C:\\Program Files\\Example'

    message = f"Processing {name} at {path}"
    formatted = "Value: {:.2f}".format( value )

    raise ValueError( "Invalid configuration value" )
    logger.error( "Failed to process item" )

Do not use function calls or subscripts inside of f-string expressions. These
can be opaque to some linters and syntax highlighters. Instead, use strings
with the ``.format`` method for these cases, where the function calls or
subscripts are performed on the arguments to ``.format``. This::

    "Values: {values}".format( values = ', '.join( values ) )

and *not* this::

    f"Values: {', '.join( values )}"


Automation
===============================================================================

Current, there are no tools which can automatically enforce compliance with the
above style guidance. However, if you politely ask an LLM, which is good at
instruction following, to make your code conform to the guidance, results will
generally be good. If you are familiar with ``isort`` and ``yapf``, you can
also look :doc:`approximate formatter configurations <python-autoformat>` for
these tools.

Cases where manual intervention may be needed:

* Multi-line chains of method invocations. (Fluent programming.)
* Function declarations with mixed positional and nominative arguments.
* Nested data structures with mixed single-line and multi-line sections.

When in doubt, optimize for readability while staying within the general
principles outlined in this guide.
