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
Practices
*******************************************************************************

This guide covers **code organization, patterns, and architectural decisions**.
For guidance on code formatting and visual presentation, see the :doc:`style`.

General
===============================================================================

Documentation
-------------------------------------------------------------------------------

Command Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Use long option names, whenever possible, in command line examples. Readers,
  who are unfamiliar with a command, should not have to look up the meanings of
  single-character option names.

  **❌ Avoid:**

  .. code-block:: shell

      git log -n 5 --oneline
      docker run -d -p 8080:80 -v /data:/app/data nginx

  **✅ Prefer:**

  .. code-block:: shell

      git log --max-count=5 --oneline
      docker run --detach --publish 8080:80 --volume /data:/app/data nginx

* Write for readers who may be unfamiliar with the tools being demonstrated.
  Provide context and explanation for complex command sequences.

Quality Assurance
-------------------------------------------------------------------------------

* Be sure to install the Git hooks, as mentioned in the :doc:`environment`
  section. This will save you turnaround time from pull request validation
  failures.

* Consider maintaining or improving code coverage when practical. Even if code
  coverage is at 100%, consider cases which are not explicitly tested.

Python
===============================================================================

Module Organization
-------------------------------------------------------------------------------

* Organize module contents in the following order to improve readability and
  maintainability:

  1. **Imports**: See section on imports organization below and in
     the :doc:`style`.
  2. **Common type aliases**: ``TypeAlias`` declarations used throughout the
     module.
  3. **Private variables and functions**: Used as defaults for public
     interfaces, grouped semantically, sorted lexicographically within groups.
  4. **Public classes and functions**: Classes before functions. Sorted
     lexicographically.
  5. **All other private functions**: Sorted lexicographically.

  **✅ Example structure:**

  .. code-block:: python

      # 1. Imports
      import requests as _requests

      from . import __

      # 2. Common type aliases
      ProcessorFunction: __.typx.TypeAlias = __.cabc.Callable[ [ str ], str ]
      UserData: __.typx.TypeAlias = dict[ str, str | int ]

      # 3. Private variables/functions for defaults (grouped semantically)
      # Configuration defaults
      _DEFAULT_TIMEOUT = 30.0
      _DEFAULT_RETRIES = 3

      # Validation defaults
      _REQUIRED_FIELDS = frozenset( [ 'name', 'email' ] )

      def _build_default_headers( ) -> dict[ str, str ]:
          return { 'User-Agent': 'MyApp/1.0' }

      # 4. Public classes and functions (alphabetical)
      class UserProcessor:
          ''' Processes user data with configurable options. '''

      def process_data( data: UserData ) -> str: pass

      def validate_user( user: UserData ) -> UserData: pass

      # 5. Other private functions (alphabetical)
      def _format_error_message( error: str ) -> str: pass
      def _sanitize_input( data: str ) -> str: pass

* Group private defaults semantically (configuration, validation, formatting,
  etc.) but sort within each semantic group lexicographically.

* Type aliases which depend on a class defined in the module should appear
  immediately after the class on which they depend.

Imports
-------------------------------------------------------------------------------

* Avoid ancillary imports into a module namespace. Use ``__`` subpackage for
  common imports or private module-level aliases for specialized imports.
  Choose import strategies based on usage patterns and performance needs.

  **❌ Avoid - namespace pollution and duplicate imports:**

  .. code-block:: python

      import json

      from collections.abc import Mapping
      from pathlib import Path
      from typing import Any, Dict, List, Union

      # Module now exposes Path, Any, Dict, List, Union, Mapping, json publicly
      # These are not part of the public interface of the module.

  **✅ Prefer - organized imports with performance considerations:**

  .. code-block:: python

      # Direct imports when performance is a consideration
      from json import loads as _json_loads

      # Private aliases for specialized libraries
      # (to avoid function-level duplicates)
      import aiofiles as _aiofiles

      # Use __ subpackage for common imports
      from . import __

* Never use ``__all__`` to advertise the public API of a module. Name anything,
  which should not be part of this API, with a private name starting with ``_``.

Type Annotations
-------------------------------------------------------------------------------

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
          lon1: __.typx.Annotated[
              float, __.ddoc.Doc( "Longitude of first point in degrees." ) ],
          lat2: __.typx.Annotated[
              float, __.ddoc.Doc( "Latitude of second point in degrees." ) ],
          lon2: __.typx.Annotated[
              float, __.ddoc.Doc( "Longitude of second point in degrees." ) ],
      ) -> __.typx.Annotated[
          float,
          __.ddoc.Doc( "Distance in kilometers." ),
          __.ddoc.Raises( ValueError, "If coordinates are invalid." ),
      ]:
          ''' Calculates distance between two geographic points. '''
          pass

Function Signatures
-------------------------------------------------------------------------------

* Accept wide types (abstract base classes) for public function parameters;
  return narrow types (concrete types) from all functions.

  **❌ Avoid - narrow parameters, wide returns:**

  .. code-block:: python

      # Restricts callers to specific types
      def merge_configs(
          base: __.immut.Dictionary[ str, str ],  # Only accepts immutable dicts
          override: list[ tuple[ str, str ] ]     # Only accepts lists
      ) -> __.cabc.Mapping[ str, str ]:           # Vague return promise
          result = dict( base )
          for key, value in override:
              result[ key ] = value
          return result  # Could return any mapping type

      def calculate_average( numbers: list[ float ] ) -> float:
          return sum( numbers ) / len( numbers )  # Rejects tuples, arrays, etc.

  **✅ Prefer - wide parameters, narrow returns:**

  .. code-block:: python

      # Accept any mapping/sequence, return specific immutable types
      def merge_configs(
          base: __.cabc.Mapping[ str, str ],      # Accept any mapping
          override: __.cabc.Sequence[ tuple[ str, str ] ]  # Accept any sequence
      ) -> __.immut.Dictionary[ str, str ]:       # Promise specific immutable type
          result = dict( base )
          for key, value in override:
              result[ key ] = value
          return __.immut.Dictionary( result )

      def calculate_average( numbers: __.cabc.Sequence[ float ] ) -> float:
          ''' Calculates average of numeric sequence. '''
          return sum( numbers ) / len( numbers )  # Works with lists, tuples, arrays

      def find_common_elements(
          set1: __.cabc.Set[ str ], set2: __.cabc.Set[ str ]
      ) -> frozenset[ str ]:
          ''' Finds common elements as immutable set. '''
          return frozenset( set1 & set2 )

      _OPTIONS_DEFAULT = __.immut.Dictionary( )
      def process_items(
          items: __.cabc.Sequence[ str ],
          filters: __.cabc.Sequence[ str ] = ( ),  # Empty tuple default
          options: __.cabc.Mapping[ str, __.typx.Any ] = _OPTIONS_DEFAULT
      ) -> tuple[ str, ... ]:
          ''' Processes items with optional filters and configuration. '''
          # Implementation preserves wide/narrow principle
          return tuple( item for item in items if all(
              f( item ) for f in filters ) )

Immutability
-------------------------------------------------------------------------------

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

  .. code-block:: python

      # Immutable data structures
      def calculate_statistics(
          data: __.cabc.Sequence[ int ]
      ) -> __.immut.Dictionary[ str, float ]:
          return __.immut.Dictionary(
              mean = sum( data ) / len( data ),
              maximum = max( data ),
              minimum = min( data ) )

      # Using immutable containers for configuration
      class DatabaseConfig( __.immut.DataclassObject ):
          hosts: tuple[ str, ... ]
          options: __.immut.Dictionary[ str, str ]

      # For cases requiring growth-only behavior - plugin registry
      plugin_registry = __.accret.Dictionary[ str, __.cabc.Callable ]( )
      plugin_registry[ 'json_formatter' ] = JsonFormatter
      plugin_registry[ 'auth_middleware' ] = AuthMiddleware
      # plugin_registry[ 'json_formatter' ] = NewFormatter  # Would raise - cannot overwrite

* When mutable data structures are genuinely needed (e.g., performance-critical
  code, interfacing with mutable APIs), clearly document the mutability
  requirement and consider using the ``Mutable`` variants of ``__.accret`` and
  ``__.immut`` classes.


Exceptional Conditions
-------------------------------------------------------------------------------

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
          logger.error( f"Package operation failed: {exc}" )
          # Handle all package errors generically

* Follow established exception naming conventions from the :doc:`nomenclature
  document <nomenclature>`. Use patterns like ``<Noun><OperationVerb>Failure``,
  ``<Noun>Absence``, ``<Noun>Invalidity``, ``<Noun>Empty``, etc.

* Limit ``try`` block scope to contain only the statement(s) that can raise
  exceptions. In rare cases, a ``with`` suite may be included. Avoid wrapping
  entire loop bodies or function bodies in ``try`` blocks when possible.

  **❌ Avoid - overly broad try blocks:**

  .. code-block:: python

      def process_items( items: __.cabc.Sequence[ str ] ) -> list[ dict ]:
          try:
              results = [ ]
              for item in items:
                  validated = validate_item( item )  # Can raise
                  processed = expensive_computation( validated )
                  formatted = format_result( processed )
                  results.append( formatted )
              return results
          except ValidationError:
              return [ ]  # Loses information about which item failed

  **✅ Prefer - narrow scope with precise error handling:**

  .. code-block:: python

      def process_items( items: __.cabc.Sequence[ str ] ) -> list[ dict ]:
          results = [ ]
          for item in items:
              try: validated = validate_item( item )  # Only risky statement
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

  .. code-block:: python

      # Swallows exception completely
      def risky_operation( ):
          try: dangerous_call( )
          except Exception:
              pass  # Silent failure loses debugging information

      # Loses original context
      def risky_operation( ):
          try: dangerous_call( )
          except ValueError:
              raise RuntimeError( "Operation failed" )  # No connection to original

  **✅ Prefer:**

  .. code-block:: python

      # Explicit chaining with 'from'
      def risky_operation( ):
          try: dangerous_call( )
          except ValueError as exc:
              raise OperateFailure( operation_context ) from exc

      # Proper handling (not swallowing)
      def risky_operation( ):
          try: dangerous_call( )
          except ValueError as exc:
              logger.warning( f"Dangerous call failed: {exc}." )
              return fallback_result( )  # Proper recovery

Documentation
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
-------------------------------------------------------------------------------

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


Rust
===============================================================================

Quality Assurance
-------------------------------------------------------------------------------

* Ensure ``cargo check`` and ``cargo clippy`` give clean reports.

  .. code-block:: shell

      # Run these commands before submitting code
      cargo check                        # Fast compilation check
      cargo clippy                       # Linting and suggestions
      cargo clippy -- -D warnings       # Treat clippy warnings as errors

* Ensure ``cargo test`` passes.

  .. code-block:: shell

      cargo test                         # Run all tests
      cargo test --doc                   # Run documentation tests
      cargo test --release              # Test optimized builds

.. todo::

   Expand Rust practices sections with import organization, error handling,
   type usage patterns, and documentation standards similar to Python section.
