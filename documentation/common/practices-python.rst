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
Python Development Guide
*******************************************************************************

This guide covers **comprehensive Python development guidance including code organization, 
patterns, architectural decisions, and formatting standards**. For general guidance 
applicable to all languages, see the main :doc:`practices`.

.. _comprehensive-example:

Comprehensive Example: Data Processing
===============================================================================

The following before/after example demonstrates multiple Python best practices 
in one cohesive implementation. Individual sections throughout this document 
reference specific aspects of this example.

**❌ Before - Multiple violations:**

.. code-block:: python

    from typing import Dict, List, Any, Optional
    from pathlib import Path
    import json

    class DataProcessor:
        def __init__(self, config_file):
            # Missing type annotations
            with open(config_file) as f:
                self.config = json.load(f)  # Mutable, exposed
        
        def process_user_data(self, users, filters=None, options={}):
            # Narrow types, mutable defaults, missing annotations
            try:
                # Overly broad try block
                results = {}
                for user in users:
                    if filters:
                        if self.validate_user(user, filters):
                            processed = self.transform_user(user, options)
                            results[user['id']] = processed
                    else:
                        processed = self.transform_user(user, options) 
                        results[user['id']] = processed
                return results  # Mutable return
            except:
                # Generic exception handling
                return {}

**✅ After - Best practices applied:**

.. code-block:: python

    from json import loads as _json_loads

    from . import __

    # Type aliases for reused complex types
    Location: __.typx.TypeAlias = str | __.pathlib.Path
    ProcessorOptions: __.typx.TypeAlias = __.immut.Dictionary[ str, __.typx.Any ]
    UserRecord: __.typx.TypeAlias = __.cabc.Mapping[ str, __.typx.Any ]

    FilterFunction: __.typx.TypeAlias = __.cabc.Callable[ [ UserRecord ], bool ]

    # Exception hierarchy (would typically be in mypackage.exceptions module)
    class UserValidationInvalidity( __.Omnierror, ValueError ):
        ''' User data validation invalidity. '''

    class ConfigurationAbsence( __.Omnierror, FileNotFoundError ):
        ''' Configuration file absence. '''

    # Private constants and defaults  
    _OPTIONS_DEFAULT = __.immut.Dictionary( )

    class DataProcessor( __.immut.DataclassObject ):
        ''' Processes user data with configurable validation and transformation. '''
        
        configuration: ProcessorOptions
        
        @classmethod
        def from_configuration_file( cls, location: Location ) -> __.typx.Self:
            ''' Creates processor from configuration file. '''
            file = __.pathlib.Path( location )
            try: content = file.read_text( )
            except ( OSError, IOError ) as exception:
                raise ConfigurationAbsence( 
                    f"Cannot read configuration: {location}" ) from exception
            try: configuration = _json_loads( content )
            except ValueError as exception:
                raise ConfigurationAbsence( 
                    f"Invalid JSON configuration: {location}" ) from exception
            return cls( configuration = __.immut.Dictionary( configuration ) )
        
        def process_user_data(
            self,
            users: __.cabc.Sequence[ UserRecord ],
            filters: __.Absential[ __.cabc.Sequence[ FilterFunction ] ] = __.absent,
            options: ProcessorOptions = _OPTIONS_DEFAULT,
        ) -> __.immut.Dictionary[ str, UserRecord ]:
            ''' Processes user data with optional filtering and custom options. '''
            filters = ( ) if __.is_absent( filters ) else filters
            results = { }
            for user in users:
                try: identifier = user[ 'identifier' ]
                except KeyError as exception:
                    raise UserValidationInvalidity( 
                        "User missing requisite 'identifier' field." ) from exception
                if not all( filter( user ) for filter in filters ):
                    continue
                processed = self._transform_user( user, options )
                results[ identifier ] = processed
            return __.immut.Dictionary( results )
        
        def _transform_user( self, user: UserRecord, options: ProcessorOptions ) -> UserRecord:
            ''' Transforms user record according to configuration and options. '''
            return __.immut.Dictionary( user )

Module Organization
===============================================================================

* Organize module contents in the following order to improve readability and
  maintainability:

  1. **Imports**: See import organization section below.
  2. **Common type aliases**: ``TypeAlias`` declarations used throughout the
     module.
  3. **Private variables and functions**:
     
     a. **Private constants**: Configuration defaults, validation constants
     b. **Private functions**: Used as defaults for public functions or to initialize caches/registries
     c. **Private caches and registries**: Module-level mutable containers
     
     Group each subcategory semantically, sort lexicographically within groups.
  4. **Public interfaces**:
     
     a. **Public classes**: Sorted lexicographically
     b. **Public functions**: Sorted lexicographically
  5. **All other private functions**: Implementation helpers, sorted lexicographically.

  The :ref:`DataProcessor example <comprehensive-example>` demonstrates proper module
  organization: imports first, then type aliases (``Location``, ``UserRecord``, etc.),
  followed by exception classes, private constants (``_OPTIONS_DEFAULT``), and finally 
  the public ``DataProcessor`` class with its methods properly ordered.

* Group private constants and initialization functions semantically (configuration, 
  validation, formatting, etc.) but sort within each semantic group lexicographically.

* Type aliases which depend on a class defined in the module should appear
  immediately after the class on which they depend.

Imports
===============================================================================

Import Organization
-------------------------------------------------------------------------------

* Follow PEP 8 import grouping conventions:

  1. ``__future__`` imports
  2. Standard library imports  
  3. Third-party imports
  4. First-party (relative) imports

Visual Formatting
-------------------------------------------------------------------------------

* For import sequences that will not fit on one line, use parentheses with
  hanging indent.

  **✅ Prefer:**

  .. code-block:: python

      from third_party.submodule import (
          FirstClass, SecondClass, ThirdClass )

* For import sequences that will not fit on two lines, list them one per line
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

Namespace Management
-------------------------------------------------------------------------------

* Avoid ancillary imports into a module namespace. Use ``__`` subpackage for
  common imports or private module-level aliases for specialized imports.

* Never use ``__all__`` to advertise the public API of a module. Name anything,
  which should not be part of this API, with a private name starting with ``_``.

  The :ref:`DataProcessor example <comprehensive-example>` demonstrates clean namespace
  management: ``_json_loads`` as a private alias for performance-critical imports and
  ``from . import __`` for accessing common project utilities without namespace pollution.

Type Annotations
===============================================================================

* Add type annotations for all function arguments, class attributes, and return
  values. Use Python 3.10+ union syntax with ``|`` for simple unions,
  ``__.typx.Union`` for complex multi-line unions, and ``TypeAlias`` for
  reused complex types.

  See the comprehensive :ref:`DataProcessor example <comprehensive-example>` above which demonstrates
  proper type annotation patterns including ``TypeAlias`` declarations for reused types like
  ``Location``, ``UserRecord``, and ``FilterFunction``.

Visual Formatting
-------------------------------------------------------------------------------

* Type annotations follow the same spacing rules as other code constructs - one
  space after opening delimiters and one space before closing delimiters.

  **✅ Prefer:**

  .. code-block:: python

      def process(
          items: __.cabc.Sequence[ __.cabc.Mapping[ str, int ] ]
      ) -> dict[ str, bool ]: pass
      
      ComplexType: __.typx.TypeAlias = __.typx.Union[
          dict[ str, __.typx.Any ],
          list[ str ],
      ]

  **❌ Avoid:**

  .. code-block:: python

      # Wrong: inconsistent bracket spacing in type annotations
      def process( items: __.cabc.Sequence[__.cabc.Mapping[str, int]] ) -> dict[str, bool]: pass

Semantic Usage
-------------------------------------------------------------------------------

* Prefer ``__.Absential`` over ``__.typx.Optional`` for optional function
  arguments when ``None`` has semantic meaning distinct from "not provided".
  This is especially valuable for update operations where ``None`` means
  "remove/clear" and absence means "leave unchanged".

  **❌ Standard approach:**

  .. code-block:: python

      def update_user_profile(
          user_id: int,
          display_name: __.typx.Optional[ str ] = None,
          avatar_url: __.typx.Optional[ str ] = None
      ) -> None:
          # Problem: Cannot distinguish "don't change" from "clear field"
          if display_name is not None:
              # Both "clear name" and "set name" end up here
              database.update( user_id, display_name = display_name )

  **✅ Better with Absence package:**

  .. code-block:: python

      def update_user_profile(
          user_id: int,
          display_name: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
          avatar_url: __.Absential[ __.typx.Optional[ str ] ] = __.absent,
      ) -> None:
          # Clear distinction between three states
          if not __.is_absent( display_name ):
              if display_name is None:
                  database.clear_field( user_id, 'display_name' )  # Remove field
              else:
                  database.update( user_id, display_name = display_name )  # Set value
          # If absent: leave field unchanged

* Use PEP 593 ``Annotated`` to encapsulate parameter and return value
  documentation via ``dynadoc`` annotations: ``__.ddoc.Doc``,
  ``__.ddoc.Raises``.

  **❌ Avoid:**

  .. code-block:: python

      # Parameter documentation in docstring
      def calculate_distance( lat1, lon1, lat2, lon2 ):
          """Calculate distance between two points.

          Args:
              lat1: Latitude of first point in degrees
              lon1: Longitude of first point in degrees
              lat2: Latitude of second point in degrees
              lon2: Longitude of second point in degrees

          Returns:
              Distance in kilometers
          """
          pass

  **✅ Prefer:**

  .. code-block:: python

      from . import __

      def calculate_distance(
          lat1: __.typx.Annotated[
              float, __.ddoc.Doc( "Latitude of first point in degrees." ) ],
          long1: __.typx.Annotated[
              float, __.ddoc.Doc( "Longitude of first point in degrees." ) ],
          lat2: __.typx.Annotated[
              float, __.ddoc.Doc( "Latitude of second point in degrees." ) ],
          long2: __.typx.Annotated[
              float, __.ddoc.Doc( "Longitude of second point in degrees." ) ],
      ) -> __.typx.Annotated[
          float,
          __.ddoc.Doc( "Distance in kilometers." ),
          __.ddoc.Raises( ValueError, "If coordinates are invalid." ),
      ]:
          ''' Calculates distance between two geographic points. '''
          pass

Function Signatures
===============================================================================

Type Principles
-------------------------------------------------------------------------------

* Accept wide types (abstract base classes) for public function parameters;
  return narrow types (concrete types) from all functions.

  The :ref:`DataProcessor example <comprehensive-example>` demonstrates this principle:
  ``process_user_data`` accepts wide parameter types (``__.cabc.Sequence[ UserRecord ]``
  for maximum caller flexibility) while returning a narrow, specific type 
  (``__.immut.Dictionary[ str, UserRecord ]``) that provides clear guarantees.

Visual Formatting
-------------------------------------------------------------------------------

* Keep all arguments on one line if they fit within the line limit.

  **✅ Prefer:**

  .. code-block:: python

      def simple_function( arg1: int, arg2: str = 'default' ) -> bool:
          return True

* Use spaces around ``=`` for keyword/nominative arguments.

  **✅ Prefer:**

  .. code-block:: python

      def some_function( magic: int = 42 ) -> int: pass
      result = process( data, timeout = 30 )

  **❌ Avoid:**

  .. code-block:: python

      def some_function(magic=42): pass
      result = process(data, timeout=30)

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

Immutability
===============================================================================

* Prefer immutable data structures over mutable ones when internal mutability
  is not required. Use ``tuple`` instead of ``list``, ``frozenset`` instead
  of ``set``, and immutable classes from ``__.immut`` (frigid) and
  ``__.accret`` (accretive) libraries.

  The :ref:`DataProcessor example <comprehensive-example>` demonstrates immutability principles:
  the class inherits from ``__.immut.DataclassObject``, uses ``_OPTIONS_DEFAULT`` as an
  immutable default, and returns ``__.immut.Dictionary`` objects to prevent accidental 
  mutation of results.

* When mutable data structures are genuinely needed (e.g., performance-critical
  code, interfacing with mutable APIs), clearly document the mutability
  requirement and consider using the ``Mutable`` variants of ``__.accret`` and
  ``__.immut`` classes.


Exceptional Conditions
===============================================================================

* Create a package exception hierarchy by subclassing from ``Omniexception``
  and ``Omnierror`` base classes. This allows callers to catch all
  package-specific exceptions generically if desired.

  The :ref:`DataProcessor example <comprehensive-example>` demonstrates proper exception
  hierarchy with ``UserValidationInvalidity`` and ``ConfigurationAbsence`` inheriting
  from ``__.Omnierror`` and appropriate built-in exception types.

* Follow established exception naming conventions from the :doc:`nomenclature
  document <nomenclature>`. Use patterns like ``<Noun><OperationVerb>Failure``,
  ``<Noun>Absence``, ``<Noun>Invalidity``, ``<Noun>Empty``, etc.

* Limit ``try`` block scope to contain only the statement(s) that can raise
  exceptions. In rare cases, a ``with`` suite may be included. Avoid wrapping
  entire loop bodies or function bodies in ``try`` blocks when possible.

  The :ref:`DataProcessor example <comprehensive-example>` demonstrates narrow try blocks:
  each ``try`` statement isolates only the specific operation that can fail 
  (``user['identifier']``, ``file.read_text()``, ``_json_loads(content)``) enabling 
  precise error handling and proper exception chaining.

* Never swallow exceptions. Either chain a ``__cause__`` with a ``from``
  original exception or raise a new exception with original exception as the
  ``__context__``. Or properly handle the exception.

  **❌ Avoid:**

  These examples show two common anti-patterns: completely swallowing exceptions
  (which loses debugging information) and raising new exceptions without chaining
  (which loses the original context).

  .. code-block:: python

      def risky_operation( ):
          try: dangerous_call( )
          except Exception:
              pass

      def risky_operation( ):
          try: dangerous_call( )
          except ValueError:
              raise RuntimeError( "Operation failed." )

  **✅ Prefer:**

  These examples show proper exception handling: explicit chaining preserves
  the original exception context, while proper handling provides fallback
  behavior without losing debugging information.

  .. code-block:: python

      def risky_operation( ):
          try: dangerous_call( )
          except ValueError as exc:
              raise OperateFailure( operation_context ) from exc

      def risky_operation( ):
          try: dangerous_call( )
          except ValueError as exc:
              logger.warning( f"Dangerous call failed: {exc}." )
              return fallback_result( )

Documentation
===============================================================================

Content Standards
-------------------------------------------------------------------------------

* Documentation must be written as Sphinx reStructuredText. The docstrings for
  functions must not include parameter or return type documentation. Parameter
  and return type documentation is handled via PEP 727 annotations. Pull
  requests, which include Markdown documentation or which attempt to provide
  function docstrings in the style of Google, NumPy, Sphinx, etc..., will be
  rejected.

* Function docstrings should use narrative mood (third person) rather than
  imperative mood (second person). The docstring describes what the function
  does, not what the caller should do.

Visual Formatting
-------------------------------------------------------------------------------

* Use triple single-quotes for all docstrings with proper spacing.

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

  **❌ Avoid:**

  .. code-block:: python

      def validate_config( config: __.cabc.Mapping[ str, __.typx.Any ] ) -> __.cabc.Mapping[ str, __.typx.Any ]:
          ''' Validate the configuration dictionary. '''  # Imperative mood

      def process_data( data: __.cabc.Sequence[ __.typx.Any ] ) -> dict[ str, __.typx.Any ]:
          ''' Process the input data and return results. '''  # Mixed - starts imperative

  **✅ Prefer:**

  .. code-block:: python

      def validate_config(
          config: __.cabc.Mapping[ str, __.typx.Any ]
      ) -> __.cabc.Mapping[ str, __.typx.Any ]:
          ''' Validates the configuration dictionary. '''  # Narrative mood

      def process_data(
          data: __.cabc.Sequence[ __.typx.Any ]
      ) -> dict[ str, __.typx.Any ]:
          ''' Processes input data and returns results. '''  # Narrative mood

Formatting Standards
===============================================================================

Lines and Spaces
-------------------------------------------------------------------------------

* One space after opening delimiters ( ``(``, ``[``, ``{`` ) and one space
  before closing delimiters ( ``)``, ``]``, ``}`` ), *except* inside of
  f-strings and strings to which ``.format`` is applied.

  **✅ Prefer:**

  .. code-block:: python

      func( arg1, arg2 )
      data = [ 1, 2, 3 ]
      config = { 'key': 'value' }

      # Exception: f-strings and .format
      message = f"Hello {name}."
      template = "Value: {value}".format( value = 42 )

  **❌ Avoid:**

  .. code-block:: python

      func(arg1, arg2)
      data = [1, 2, 3]
      config = {"key": "value"}

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

Line Continuation
-------------------------------------------------------------------------------

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

  **❌ Avoid:**

  .. code-block:: python

      # Using backslash continuation
      result = very_long_object_name.first_method_call( ) \
               .second_method_call( ) \
               .final_method_call( )

      # Operators at end of line being split
      total = (
          first_long_value * second_long_value +
          third_long_value * fourth_long_value )

Function Invocations
-------------------------------------------------------------------------------

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

  **❌ Avoid:**

  .. code-block:: python

      # Unnecessary trailing comma in function call
      result = process_data(
          input_file,
          output_file,
          strict = True, )

Strings
-------------------------------------------------------------------------------

* Use single quotes for plain data strings unless they contain single quotes.
  Use double quotes for f-strings, ``.format`` strings, exception messages,
  and log messages.

* Exception messages and log messages should end with periods for consistency
  and proper sentence structure.

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
  with the ``.format`` method for these cases.

  **✅ Prefer:**

  .. code-block:: python

      "Values: {values}".format( values = ', '.join( values ) )

  **❌ Avoid:**

  .. code-block:: python

      f"Values: {', '.join(values)}"

Quality Assurance
===============================================================================

* Run project-specific quality commands to ensure code meets standards. Use the
  provided hatch environments for consistency.

  .. code-block:: shell

      hatch --env develop run linters    # Runs all configured linters
      hatch --env develop run testers    # Runs full test suite
      hatch --env develop run docsgen    # Generates documentation

* Linter suppressions must be reviewed critically. Address underlying design
  problems rather than masking them with suppressions.

**Acceptable Suppressions:**

* ``noqa: PLR0913`` may be used for CLI or service APIs with many parameters,
  but data transfer objects should be considered in most other cases.
* ``noqa: S*`` may be used for properly constrained and vetted subprocess
  executions or Internet content retrievals.

**Unacceptable Suppressions (require investigation):**

* ``type: ignore`` must not be used except in extremely rare circumstances.
  Such suppressions usually indicate missing third-party dependencies or type
  stubs, inappropriate type variables, or bad inheritance patterns.
* ``__.typx.cast`` should not be used except in extremely rare circumstances.
  Such casts suppress normal type checking and usually indicate the same
  problems as ``type: ignore``.
* Tryceratops complaints must not be suppressed with ``noqa`` pragmas.
* Most other ``noqa`` suppressions require compelling justification.

* If third-party typing stubs are missing, then ensure that the third-party
  package has been included in ``pyproject.toml`` and rebuild the Hatch
  environment with ``hatch env prune``. If they are still missing after that,
  then generate them with:

  .. code-block:: shell

      hatch --env develop run pyright --createsub somepackage

  Then, fill out the stubs you need to satisfy Pyright and comment out or
  discard the remainder.