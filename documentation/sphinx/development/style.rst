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

  - **Vertical Compactness**: Function definitions, loop bodies, and condition
    bodies, which consist of a single statement and which are sufficiently
    short, should be placed on the same line as the statement that introduces
    the body. Blank lines should not be used to group statements within a
    function body. If you need to group statements within a function body, then
    perhaps the function should be refactored. Function bodies should not be
    longer than thirty lines. I.e., one should not have to scroll to read a
    function.

* Pull requests, which attempt to enforce the Python ``black`` style or any
  style other than the project code style, will be rejected.





Specific Preferences
===============================================================================

Collections
-------------------------------------------------------------------------------

For short collections, keep them on one line::

    points = [ ( 1, 2 ), ( 3, 4 ), ( 5, 6 ) ]

    config = { 'name': 'example', 'value': 42 }

For longer collections, split elements across lines::

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


Imports
-------------------------------------------------------------------------------

Prefer function-level imports over module-level imports to prevent module
namespace pollution and make functions more relocatable::

    def process_data( raw_data: bytes ) -> dict:
        from collections import defaultdict
        from itertools import groupby
        from .utils import decode_packet
        # Function implementation...

When imports must appear at the module level, follow the grouping conventions
from :pep:`8`::

    from __future__ import annotations

    import collections.abc as cabc
    import types
    from dataclasses import dataclass
    from typing import Optional

    import typing_extensions as typx
    from third_party import ThirdPartyClass

    from .submodule import LocalClass

For multi-line imports, use parentheses with hanging indent. Add a trailing
comma to force one-per-line format for very long import lists::

    from third_party.submodule import (
        FirstClass, SecondClass, ThirdClass )

    from third_party.other import (
        ALongClassName,
        AnotherLongClassName,
        YetAnotherLongClassName,
    )


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


Strings
-------------------------------------------------------------------------------

Use single quotes for string literals unless using f-strings, ``.format( )``
method, or exception and logging messages::

    name = 'example'
    path = 'C:\\Program Files\\Example'

    message = f"Processing {name} at {path}"
    formatted = "Value: {:.2f}".format( value )

    raise ValueError( "Invalid configuration value" )
    logger.error( "Failed to process item" )


Automation
===============================================================================

The project includes configurations for ``isort`` and ``yapf`` in
``pyproject.toml``. While these tools help maintain consistent formatting,
they do not perfectly match all style guidelines. In cases where automatic
formatting produces suboptimal results, manual formatting according to this
guide takes precedence.

Cases where manual intervention may be needed:

* Complex function definitions with mixed positional and nominative arguments
* Multi-line method chains
* Nested data structures with mixed single-line and multi-line sections

When in doubt, optimize for readability while staying within the general
principles outlined in this guide.