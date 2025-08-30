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
Python Development Practices
*******************************************************************************

This guide covers **Python-specific code organization, patterns, and architectural decisions**.
For general guidance applicable to all languages, see the main :doc:`practices`.
For guidance on code formatting and visual presentation, see the :doc:`style-python`.

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

  **✅ Example structure:**

  .. code-block:: python

      # 1. Imports
      import requests as _requests

      from . import __

      # 2. Common type aliases
      ProcessorFunction: __.typx.TypeAlias = __.cabc.Callable[ [ str ], str ]
      UserData: __.typx.TypeAlias = __.cabc.Mapping[ str, str | int ]

      # 3a. Private constants
      _TIMEOUT_DEFAULT = 30.0
      _RETRIES_DEFAULT = 3

      # 3a. Validation constants  
      _REQUISITE_ATTRIBUTES = frozenset( [ 'name', 'email' ] )

      # 3b. Private initialization functions
      def _provide_default_http_headers( ) -> dict[ str, str ]:
          return { 'User-Agent': 'MyApp/1.0' }

      # 4a. Public classes
      class UserProcessor:
          ''' Processes user data with configurable options. '''

      # 4b. Public functions
      def process_data( data: UserData ) -> str: pass

      def validate_user( user: UserData ) -> UserData: pass

      # 5. Other private functions
      def _format_error_message( error: str ) -> str: pass
      def _sanitize_data( data: str ) -> str: pass

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

* For visual formatting of multi-line imports, use parentheses with proper indentation.

Namespace Management
-------------------------------------------------------------------------------

* Avoid ancillary imports into a module namespace. Use ``__`` subpackage for
  common imports or private module-level aliases for specialized imports.

* Never use ``__all__`` to advertise the public API of a module. Name anything,
  which should not be part of this API, with a private name starting with ``_``.

  **❌ Avoid - namespace pollution:**

  .. code-block:: python

      from pathlib import Path
      from typing import Any, Dict, List
      # Module now exposes Path, Any, Dict, List publicly

  **✅ Prefer - private aliases and __ subpackage:**

  .. code-block:: python

      from json import loads as _json_loads  # Performance-critical imports
      
      import aiofiles as _aiofiles           # Specialized libraries
      
      from . import __                       # Common project imports

Type Annotations
===============================================================================

* Add type annotations for all function arguments, class attributes, and return
  values. Use Python 3.10+ union syntax with ``|`` for simple unions,
  ``__.typx.Union`` for complex multi-line unions, and ``TypeAlias`` for
  reused complex types.

  **❌ Avoid - missing annotations and type repetition:**

  .. code-block:: python

      # Missing type annotations
      def process_data( items, callback=None ):
          return [ str( item ) for item in items ]

      # Repeating complex types without TypeAlias
      def process_user( user: dict[ str, str | int | list[ str ] ] ) -> dict[ str, str | int | list[ str ] ]: pass
      def validate_user( user: dict[ str, str | int | list[ str ] ] ) -> dict[ str, str | int | list[ str ] ]: pass

  **✅ Prefer - comprehensive type annotations with aliases:**

  .. code-block:: python

      from . import __

      # TypeAlias for reused complex types
      UserRecord: __.typx.TypeAlias = dict[ str, str | int | list[ str ] ]

      # Multi-line unions for very complex types
      ComplexHandler: __.typx.TypeAlias = __.typx.Union[
          __.cabc.Callable[ [ UserRecord ], str ],
          __.cabc.Callable[ [ UserRecord, dict[ str, __.typx.Any ] ], str ],
          tuple[ str, __.cabc.Callable[ [ UserRecord ], bool ] ],
      ]

      def process_data(
          items: __.cabc.Sequence[ str | int ],
          callback: __.Absential[
              __.cabc.Callable[ [ str | int ], str ]
          ] = __.absent,
      ) -> list[ str ]:
          results = [ ]
          for item in items:
              if not __.is_absent( callback ): result = callback( item )
              else: result = str( item )
              results.append( result )
          return results

      def process_user( user: UserRecord ) -> UserRecord: pass
      def validate_user( user: UserRecord ) -> UserRecord: pass

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

* Accept wide types (abstract base classes) for public function parameters;
  return narrow types (concrete types) from all functions.

  **❌ Avoid - narrow parameters, wide returns:**

  This approach restricts callers to specific types, limiting flexibility.
  The parameters only accept specific concrete types (immutable dicts, lists)
  while the return type is vague, offering no guarantees about what will be returned.

  .. code-block:: python

      def merge_configurations(
          base: __.immut.Dictionary[ str, str ],
          override: list[ tuple[ str, str ] ]
      ) -> __.cabc.Mapping[ str, str ]:
          result = dict( base )
          for key, value in override:
              result[ key ] = value
          return result

      def calculate_average( numbers: list[ float ] ) -> float:
          return sum( numbers ) / len( numbers )

  **✅ Prefer - wide parameters, narrow returns:**

  This approach accepts any compatible mapping or sequence types, maximizing flexibility
  for callers, while returning specific immutable types that provide clear guarantees.

  .. code-block:: python

      def merge_configurations(
          base: __.cabc.Mapping[ str, str ],
          override: __.cabc.Sequence[ tuple[ str, str ] ]
      ) -> __.immut.Dictionary[ str, str ]:
          result = dict( base )
          for key, value in override:
              result[ key ] = value
          return __.immut.Dictionary( result )

      def calculate_average( numbers: __.cabc.Sequence[ float ] ) -> float:
          ''' Calculates average of numeric sequence. '''
          return sum( numbers ) / len( numbers )

  The ``calculate_average`` function now properly advertises its compatibility with any sequence type through its type signature.

      def find_common_elements(
          set1: __.cabc.Set[ str ], set2: __.cabc.Set[ str ]
      ) -> frozenset[ str ]:
          ''' Finds common elements as immutable set. '''
          return frozenset( set1 & set2 )

      _OPTIONS_DEFAULT = __.immut.Dictionary( )
      def process_items(
          items: __.cabc.Sequence[ str ],
          filters: __.cabc.Sequence[ str ] = ( ),
          options: __.cabc.Mapping[ str, __.typx.Any ] = _OPTIONS_DEFAULT
      ) -> tuple[ str, ... ]:
          ''' Processes items with optional filters and configuration. '''
          return tuple( item for item in items if all(
              f( item ) for f in filters ) )

  This implementation preserves the wide/narrow principle: accepts any sequence types
  for flexibility, uses an empty tuple as the default (immutable), and returns a
  specific tuple type.

Immutability
===============================================================================

* Prefer immutable data structures over mutable ones when internal mutability
  is not required. Use ``tuple`` instead of ``list``, ``frozenset`` instead
  of ``set``, and immutable classes from ``__.immut`` (frigid) and
  ``__.accret`` (accretive) libraries.

  **❌ Avoid:**

  .. code-block:: python

      # Mutable data structures when immutability would suffice
      def calculate_statistics( data: __.cabc.Sequence[ int ] ) -> dict[ str, float ]:
          results = { }
          results[ 'mean' ] = sum( data ) / len( data )
          results[ 'max' ] = max( data )
          results[ 'min' ] = min( data )
          return results

      # Using mutable containers for configuration
      class DatabaseConfig:
          def __init__( self, hosts: __.cabc.Sequence[ str ], options: __.cabc.Mapping[ str, str ] ):
              self.hosts = hosts  # Sequence can be modified externally
              self.options = options  # Mapping can be modified externally

  **✅ Prefer:**

  Use immutable data structures that provide clear contracts and prevent accidental mutation.

  .. code-block:: python

      def calculate_statistics(
          data: __.cabc.Sequence[ int ]
      ) -> __.immut.Dictionary[ str, float ]:
          return __.immut.Dictionary(
              mean = sum( data ) / len( data ),
              maximum = max( data ),
              minimum = min( data ) )

  Use immutable containers for configuration objects to prevent external modification:

  .. code-block:: python

      class DatabaseConfig( __.immut.DataclassObject ):
          hosts: tuple[ str, ... ]
          options: __.immut.Dictionary[ str, str ]

  For cases requiring growth-only behavior (like plugin registries), use accretive containers.
  These allow additions but prevent overwriting or removal:

  .. code-block:: python

      plugin_registry = __.accret.Dictionary[ str, __.cabc.Callable ]( )
      plugin_registry[ 'json_formatter' ] = JsonFormatter
      plugin_registry[ 'auth_middleware' ] = AuthMiddleware

* When mutable data structures are genuinely needed (e.g., performance-critical
  code, interfacing with mutable APIs), clearly document the mutability
  requirement and consider using the ``Mutable`` variants of ``__.accret`` and
  ``__.immut`` classes.


Exceptional Conditions
===============================================================================

* Create a package exception hierarchy by subclassing from ``Omniexception``
  and ``Omnierror`` base classes. This allows callers to catch all
  package-specific exceptions generically if desired.

  **✅ Prefer:**

  .. code-block:: python

      from . import __

      class Omniexception( __.immut.Object, BaseException ):
          ''' Base for all exceptions raised by package API. '''

      class Omnierror( Omniexception, Exception ):
          ''' Base for error exceptions raised by package API. '''

      # Specific exceptions inherit from appropriate base
      class DataAbsence( Omnierror, AssertionError ):
          ''' Unexpected data absence. '''

          def __init__( self, source: str, label: str ):
              super( ).__init__(
                  f"Necessary data with label '{label}' "
                  f"is missing from {source}." )

  Usage: Callers can catch all package exceptions.

  .. code-block:: python

      try: result = package_operation( )
      except Omnierror as exc:
          logger.error( f"Package operation failed: {exc}." )
          # Handle all package errors generically

* Follow established exception naming conventions from the :doc:`nomenclature
  document <nomenclature>`. Use patterns like ``<Noun><OperationVerb>Failure``,
  ``<Noun>Absence``, ``<Noun>Invalidity``, ``<Noun>Empty``, etc.

* Limit ``try`` block scope to contain only the statement(s) that can raise
  exceptions. In rare cases, a ``with`` suite may be included. Avoid wrapping
  entire loop bodies or function bodies in ``try`` blocks when possible.

  **❌ Avoid - overly broad try blocks:**

  This example wraps too much code in the try block, making error handling imprecise.
  The ``validate_item`` function can raise exceptions, but the broad try block 
  loses information about which specific item failed.

  .. code-block:: python

      def process_items( items: __.cabc.Sequence[ str ] ) -> list[ dict ]:
          try:
              results = [ ]
              for item in items:
                  validated = validate_item( item )
                  processed = expensive_computation( validated )
                  formatted = format_result( processed )
                  results.append( formatted )
              return results
          except ValidationError:
              return [ ]

  **✅ Prefer - narrow scope with precise error handling:**

  This approach isolates only the risky statement in the try block, providing
  precise error handling for each item individually.

  .. code-block:: python

      def process_items( items: __.cabc.Sequence[ str ] ) -> list[ dict ]:
          results = [ ]
          for item in items:
              try: validated = validate_item( item )
              except ValidationError:
                  logger.warning( f"Skipping invalid item: {item}." )
                  continue
              processed = expensive_computation( validated )
              formatted = format_result( processed )
              results.append( formatted )
          return results

      def save_data(
          data: __.cabc.Mapping[ str, __.typx.Any ], filename: str
        ) -> None:
          try:
              with open( filename, 'w' ) as f:
                  serialize( data, f )
          except OSError as exc:
              raise SaveFailure( filename ) from exc

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

* Documentation must be written as Sphinx reStructuredText. The docstrings for
  functions must not include parameter or return type documentation. Parameter
  and return type documentation is handled via PEP 727 annotations. Pull
  requests, which include Markdown documentation or which attempt to provide
  function docstrings in the style of Google, NumPy, Sphinx, etc..., will be
  rejected.

* Function docstrings should use narrative mood (third person) rather than
  imperative mood (second person). The docstring describes what the function
  does, not what the caller should do.

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