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
For guidance on code formatting and visual presentation, see :doc:`style`.

General
===============================================================================

Quality Assurance
-------------------------------------------------------------------------------

* Be sure to install the Git hooks, as mentioned in the :doc:`environment`
  section. This will save you turnaround time from pull request validation
  failures.

* Consider maintaining or improving code coverage when practical. Even if code
  coverage is at 100%, consider cases which are not explicitly tested.

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

Exceptional Conditions
-------------------------------------------------------------------------------

Python
===============================================================================

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
                  f"Necessary data with label '{label}' is missing from {source}." )

      class ConfigureFailure( Omnierror ):
          ''' Raised when configuration operation fails. '''

  Usage: Callers can catch all package exceptions.

  .. code-block:: python

      try: result = package_operation( )
      except Omnierror as exc:
          logger.error( f"Package operation failed: {exc}" )
          # Handle all package errors generically
      except Omniexception:
          # Handle non-error package exceptions (e.g., interruptions)
          pass

* Follow established exception naming conventions from :doc:`nomenclature`.
  Use patterns like ``<Noun><OperationVerb>Failure``, ``<Noun>Absence``,
  ``<Noun>Invalidity``, ``<Noun>Empty``, etc.

  **✅ Prefer:**

  .. code-block:: python

      # Operation failures
      class ConfigureFailure( Omnierror ):  # Not "ConfigurationError"
      class ProcessInterruption( Omniexception ):  # For interrupted operations
      class AttributeInvalidity( Omnierror ):  # For invalid states/data

      # State-based exceptions
      class FileAbsence( Omnierror, AssertionError ):  # For unexpected absense
      class DataEmpty( Omnierror, AssertionError ):  # For unexpectedly empty data

* Limit ``try`` block scope to contain only the statement(s) that can raise
  exceptions. In rare cases, a ``with`` suite may be included. Avoid wrapping
  entire loop bodies or function bodies in ``try`` blocks when possible.

  **❌ Avoid:**

  .. code-block:: python

      # Try block too broad - entire function wrapped
      def process_items( items: list[ str ] ) -> list[ dict ]:
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

      # Try block wrapping entire loop
      def process_items( items: list[ str ] ) -> list[ dict ]:
          results = [ ]
          try:
              for item in items:
                  validated = validate_item( item )  # Can raise
                  processed = expensive_computation( validated )
                  formatted = format_result( processed )
                  results.append( formatted )
          except ValidationError:
              pass  # Unclear which item caused the failure
          return results

  **✅ Prefer:**

  .. code-block:: python

      # Narrow try block around specific risky operation
      def process_items( items: list[ str ] ) -> list[ dict ]:
          results = [ ]
          for item in items:
              try: validated = validate_item( item )  # Only statement that raises
              except ValidationError:
                  logger.warning( f"Skipping invalid item: {item}." )
                  continue
              processed = expensive_computation( validated )
              formatted = format_result( processed )
              results.append( formatted )
          return results

  **✅ Also acceptable - try with context manager:**

  .. code-block:: python

      def save_data( data: dict, filename: str ) -> None:
          try:
              with open( filename, 'w' ) as f:  # Context manager may raise
                  json.dump( data, f )
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

Import Organization
-------------------------------------------------------------------------------

* Avoid ancillary imports into a module namespace. Instead, place common
  imports into the ``__`` package base or use private module-level aliases
  for specialized imports. This avoids pollution of the module namespace,
  which should only have public attributes which relate to the interface
  that it is providing.

* **Performance considerations**: Choose import strategies based on usage
  patterns:

  - **``__.module.attribute`` access**: Acceptable for most code, but avoid
    in hot path functions due to attribute lookup overhead.
  - **Private module-level aliases**: Use ``from __.module import attribute as
    _attribute`` in performance-critical modules.
  - **Function-level imports**: Generally avoid due to import overhead on
    each function call. Only use for specialized libraries needed by one or
    two non-performance-critical functions.

  **❌ Avoid:**

  .. code-block:: python

      # Pollutes module namespace
      from pathlib import Path
      from typing import Any, Dict, List, Optional
      from collections.abc import Mapping, Sequence
      import asyncio
      import json

      def process_file( path: Path ) -> Dict: pass
      def async_handler( data: List ) -> None: pass

      # Module now has Path, Any, Dict, List, Optional, Mapping, Sequence,
      # asyncio, json in its public namespace

  **✅ Prefer:**

  .. code-block:: python

      # Use __ subpackage for common imports
      from . import __

      def process_file( path: __.Path ) -> dict: pass
      def async_handler( data: list ) -> None: pass

  **✅ Also prefer - private aliases for specialized module-level imports:**

  .. code-block:: python

      import aiofiles as _aiofiles
      from specialized_lib import ComplexProcessor as _ComplexProcessor

      # For performance-critical code, prefer direct imports
      from __.pathlib import Path as _Path
      from __.json import loads as _json_loads

      async def process_async( filename: str ) -> None:
          async with _aiofiles.open( filename ) as f:
              processor = _ComplexProcessor( )
              # ...

      def hot_path_function( data: bytes ) -> dict:
          # Avoid __.json.loads in hot paths - use direct import
          return _json_loads( data.decode( ) )

      def parse_path( path_str: str ) -> dict:
          # Use direct import to avoid __.pathlib.Path overhead
          path = _Path( path_str )
          return { 'name': path.name, 'suffix': path.suffix }

* **Function portability considerations**: While function-level imports can
  make functions more relocatable since dependencies move with them, avoid
  duplicating the same import across multiple functions in the same module.
  Instead, use a private module-level alias.

  **❌ Avoid - duplicate function-level imports:**

  .. code-block:: python

      def process_toml_config( data: str ) -> dict:
          from tomli import loads  # Duplicated import
          return loads( data )

      def validate_toml_schema( data: str ) -> bool:
          from tomli import loads  # Same import repeated
          try:
              loads( data )
              return True
          except Exception:
              return False

  **✅ Prefer - single private alias:**

  .. code-block:: python

      from tomli import loads as _loads

      def process_toml_config( data: str ) -> dict:
          return _loads( data )

      def validate_toml_schema( data: str ) -> bool:
          try:
              _loads( data )
              return True
          except Exception:
              return False

* Reference common imports from the ``__`` subpackage when available. The
  ``__`` subpackage contains aliases for frequently used imports like ``cabc``
  for ``collections.abc``, ``typx`` for ``typing_extensions``, etc.

  **❌ Avoid:**

  .. code-block:: python

      # Direct import when __ provides it
      from typing import Any, Dict, List, Union
      from collections.abc import Mapping
      from typing_extensions import TypeAlias

      UserData: TypeAlias = Dict[ str, Union[ str, int ] ]

      def process( data: Mapping[ str, Any ] ) -> List[ str ]: pass

  **✅ Prefer:**

  .. code-block:: python

      # Use __ subpackage
      from . import __

      UserData: __.typx.TypeAlias = dict[ str, str | int ]

      def process( data: __.cabc.Mapping[ str, __.typx.Any ] ) -> list[ str ]: pass

* Never use ``__all__`` to advertise the public API of a module. Name anything,
  which should not be part of this API, with a private name starting with ``_``.

  **❌ Avoid:**

  .. code-block:: python

      # Using __all__ to control exports
      def helper1( ): pass
      def helper2( ): pass
      def _internal_func( ): pass

      __all__ = ['helper1', 'helper2']  # Fragile, easy to forget updates

      def public_function( ): pass
      # public_function not in __all__, but still publicly accessible

  **✅ Prefer:**

  .. code-block:: python

      # Private naming controls visibility
      def helper1( ): pass
      def helper2( ): pass
      def _internal_func( ): pass  # Clear intent, starts with underscore

      def public_function( ): pass
      def _private_function( ): pass  # Clear intent, starts with underscore

      # Public API is obvious: helper1, helper2, public_function
      # Private internals: _internal_func, _private_function

Type Annotations
-------------------------------------------------------------------------------

* Add type annotations for all function arguments, class attributes, and return
  values. Use Python 3.10+ union syntax with ``|`` for simple unions that fit
  on one line. For complex multi-line unions, use ``__.typx.Union``. For
  optional types, prefer ``__.typx.Optional`` over ``| None``.

  **❌ Avoid:**

  .. code-block:: python

      # Missing type annotations
      def process_data( items, callback=None ):
          results = []
          for item in items:
              if callback:
                  result = callback(item)
              else:
                  result = str(item)
              results.append(result)
          return results

  **✅ Prefer:**

  .. code-block:: python

      from . import __

      def process_data(
          items: list[ str | int ],
          callback: __.typx.Optional[ __.cabc.Callable[ [ str | int ], str ] ] = None
      ) -> list[ str ]:
          results = [ ]
          for item in items:
              if callback: result = callback( item )
              else: result = str( item )
              results.append( result )
          return results

  **✅ For complex multi-line unions:**

  .. code-block:: python

      ComplexType: __.typx.TypeAlias = __.typx.Union[
          dict[ str, __.typx.Any ],
          list[ dict[ str, str ] ],
          tuple[ int, str, bool ],
          __.cabc.Callable[ [ int ], str ],
      ]

* Prefer ``__.Absential`` over ``__.typx.Optional`` for optional function
  arguments when the ``absence`` package is available. This allows ``None``
  to be used as a meaningful value.

  **✅ Standard approach:**

  .. code-block:: python

      def process_config(
          data: dict[ str, __.typx.Any ],
          default_timeout: __.typx.Optional[ float ] = None
      ) -> dict[ str, __.typx.Any ]:
          timeout = default_timeout if default_timeout is not None else 30.0
          # ...

  **✅ Better with absence package:**

  .. code-block:: python

      def process_config(
          data: dict[ str, __.typx.Any ],
          default_timeout: __.Absential[ __.Optional[ float ] ] = __.absent
      ) -> dict[ str, __.typx.Any ]:
          timeout = default_timeout if not __.is_absent( default_timeout ) else 30.0
          # Now None can be a meaningful timeout value (infinite timeout)

* Use PEP 593 ``Annotated`` for parameter and return value documentation when
  docstrings are insufficient. Prefer ``__.ddoc.Doc`` if the ``dynadoc`` package
  is available, otherwise use ``__.typx.Doc``. Use space-padded annotation lists.

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

* Create ``TypeAlias`` declarations for complex type annotations that are reused
  or form part of the public API.

  **❌ Avoid:**

  .. code-block:: python

      # Repeating complex types
      def process_user( user: dict[ str, str | int | list[ str ] ] ) -> dict[ str, str | int | list[ str ] ]: pass
      def validate_user( user: dict[ str, str | int | list[ str ] ] ) -> bool: pass
      def store_user( user: dict[ str, str | int | list[ str ] ] ) -> None: pass

  **✅ Prefer:**

  .. code-block:: python

      from . import __

      # TypeAlias for reused complex types
      UserRecord: __.typx.TypeAlias = dict[ str, str | int | list[ str ] ]

      def process_user( user: UserRecord ) -> UserRecord: pass
      def validate_user( user: UserRecord ) -> bool: pass
      def store_user( user: UserRecord ) -> None: pass

  **✅ Also prefer - more specific type structure with TypedDict:**

  .. code-block:: python

      UserMetadata: __.typx.TypeAlias = dict[ str, __.typx.Any ]
      UserPermissions: __.typx.TypeAlias = list[ str ]

      class UserRecord( __.typx.TypedDict ):
          name: str
          age: int
          permissions: UserPermissions
          metadata: UserMetadata

Documentation Standards
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

      def validate_config( config: dict ) -> None:
          ''' Validate the configuration dictionary. '''  # Imperative mood

      def process_data( data: list ) -> dict:
          ''' Process the input data and return results. '''  # Mixed - starts imperative

  **✅ Prefer:**

  .. code-block:: python

      def validate_config( config: dict ) -> None:
          ''' Validates the configuration dictionary. '''  # Narrative mood

      def process_data( data: list ) -> dict:
          ''' Processes input data and returns results. '''  # Narrative mood

* Prefer PEP 727 annotations over docstring parameter sections. Use docstrings
  for high-level descriptions, usage patterns, and examples rather than
  parameter documentation.

  **❌ Avoid:**

  .. code-block:: python

      # Duplicating type info in docstring
      def merge_configs(
          base: dict[ str, __.typx.Any ],
          override: dict[ str, __.typx.Any ]
      ) -> dict[ str, __.typx.Any ]:
          """Merge two configuration dictionaries.

          Args:
              base: Base configuration dictionary
              override: Override configuration dictionary

          Returns:
              Merged configuration dictionary
          """
          pass

  **✅ Prefer:**

  .. code-block:: python

      def merge_configs(
          base: __.typx.Annotated[ dict[ str, __.typx.Any ], __.ddoc.Doc( "Base configuration." ) ],
          override: __.typx.Annotated[ dict[ str, __.typx.Any ], __.ddoc.Doc( "Override values." ) ]
      ) -> __.typx.Annotated[ dict[ str, __.typx.Any ], __.ddoc.Doc( "Merged configuration." ) ]:
          ''' Merges configuration dictionaries with override precedence.

              Override values take precedence over base values. Nested
              dictionaries are merged recursively.

              Example usage::

                  base = { 'host': 'localhost', 'port': 8080, 'debug': False }
                  override = { 'port': 9090, 'debug': True }
                  result = merge_configs( base, override )
                  # result: { 'host': 'localhost', 'port': 9090, 'debug': True }
          '''
          pass

Quality Assurance
-------------------------------------------------------------------------------

* Run project-specific quality commands to ensure code meets standards. Use the
  provided hatch environments for consistency.

  **❌ Avoid:**

  .. code-block:: shell

      # Ad-hoc linting commands
      flake8 src/
      mypy src/
      black --check src/

  **✅ Prefer:**

  .. code-block:: shell

      # Use project's hatch environment
      hatch --env develop run linters    # Runs all configured linters
      hatch --env develop run testers    # Runs full test suite
      hatch --env develop run docsgen    # Generates documentation

* Do not suppress linter warnings with ``noqa`` pragma comments without explicit
  approval. Address the underlying issues instead of silencing warnings.

  **❌ Avoid:**

  .. code-block:: python

      # Suppressing without fixing
      def complex_function( data ):  # noqa: ANN001
          result = eval(user_input)  # noqa: S307
          return result

  **✅ Prefer:**

  .. code-block:: python

      # Fix the underlying issues
      def complex_function( data: UserData ) -> ProcessedData:
          result = safe_evaluate( user_input )  # Use proper parser instead of eval
          return result

Immutability
-------------------------------------------------------------------------------

* Prefer immutable data structures over mutable ones when internal mutability
  is not required. Use ``tuple`` instead of ``list``, ``frozenset`` instead
  of ``set``, and immutable classes from ``__.immut`` (frigid) and
  ``__.accret`` (accretive) libraries.

  **❌ Avoid:**

  .. code-block:: python

      # Mutable data structures when immutability would suffice
      def calculate_statistics( data: list[ int ] ) -> dict[ str, float ]:
          results = { }
          results[ 'mean' ] = sum( data ) / len( data )
          results[ 'max' ] = max( data )
          results[ 'min' ] = min( data )
          return results

      # Using mutable containers for configuration
      class DatabaseConfig:
          def __init__( self, hosts: list[ str ], options: dict[ str, str ] ):
              self.hosts = hosts  # Mutable list can be modified externally
              self.options = options  # Mutable dict can be modified externally

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
      class DatabaseConfig( __.immut.Object ):
          hosts: tuple[ str, ... ]
          options: __.immut.Dictionary[ str, str ]

      # For cases requiring growth-only behavior
      event_log = __.accret.Dictionary( )  # Can add entries but not modify/remove existing ones
      event_log[ 'startup' ] = 'Application started at 2024-01-01T10:00:00Z'
      event_log[ 'user_login' ] = 'User admin logged in at 2024-01-01T10:05:00Z'
      # event_log[ 'startup' ] = 'new value'  # Would raise exception - cannot modify
      # del event_log[ 'startup' ]  # Would raise exception - cannot delete

* Use immutable base classes from the ``frigid`` library (aliased as
  ``__.immut``) for objects that should never change after creation. Use
  ``accretive`` library containers (aliased as ``__.accret``) for data
  structures that can grow by adding new entries but cannot modify or remove
  existing entries.

  **❌ Avoid:**

  .. code-block:: python

      # Standard mutable classes
      class UserProfile:
          def __init__( self, name: str, email: str ):
              self.name = name
              self.email = email  # Can be accidentally modified
              self.login_attempts = 0

          def record_login_attempt( self ):
              self.login_attempts += 1  # Violates immutability

  **✅ Prefer:**

  .. code-block:: python

      # Immutable object with frozen attributes
      class UserProfile( __.immut.Object ):
          name: str
          email: str

      # Accretive containers for grow-only data  
      login_attempts = __.accret.Dictionary[ str, str ]( )
      login_attempts[ '2024-01-01T10:05:00Z' ] = 'admin login successful'
      login_attempts[ '2024-01-01T10:06:00Z' ] = 'user login failed'
      # Can add new entries but cannot modify or delete existing ones
      
      user_sessions = __.accret.Namespace( )
      user_sessions.session_001 = 'active'
      user_sessions.session_002 = 'expired'
      # Can add new attributes but cannot modify existing ones

* When mutable data structures are genuinely needed (e.g., performance-critical
  code, interfacing with mutable APIs), clearly document the mutability
  requirement and consider using the ``Mutable`` variants of classes.

  **✅ Acceptable when required:**

  .. code-block:: python

      # Performance-critical accumulation
      def process_large_dataset( data: __.cabc.Iterable[ int ] ) -> list[ int ]:
          ''' Processes dataset using mutable list for performance.

              Uses mutable list internally for efficient appending during
              processing of potentially millions of items.
          '''
          results = [ ]  # Mutable for performance reasons
          for item in data:
              if is_valid( item ):
                  results.append( transform( item ) )
          return results

      # Mutable class when needed
      class Cache( __.immut.ObjectMutable ):
          ''' Cache with mutable internal state for performance. '''
          _cache: dict[ str, __.typx.Any ]  # Mutable for cache operations

Function Signatures
-------------------------------------------------------------------------------

* Accept wide types (abstract base classes) in function parameters but return
  narrow types (concrete immutable types). This follows the Liskov
  Substitution Principle and makes functions more flexible to call while
  providing specific guarantees to callers.

  **❌ Avoid:**

  .. code-block:: python

      # Narrow parameter types limit flexibility
      def merge_configs(
          base: __.immut.Dictionary[ str, str ],
          override: __.immut.Dictionary[ str, str ]
      ) -> dict[ str, str ]:
          result = dict( base )
          result.update( override )
          return result  # Returns mutable dict

      # Wide return types provide no guarantees
      def get_user_permissions( user_id: int ) -> __.cabc.Sequence[ str ]:
          permissions = fetch_permissions( user_id )
          return list( permissions )  # Could return mutable list

  **✅ Prefer:**

  .. code-block:: python

      # Wide parameter types, narrow return types
      def merge_configs(
          base: __.cabc.Mapping[ str, str ],  # Accept any mapping
          override: __.cabc.Mapping[ str, str ]  # Accept any mapping
      ) -> __.immut.Dictionary[ str, str ]:  # Return specific immutable type
          result = dict( base )
          result.update( override )
          return __.immut.Dictionary( result )

      def get_user_permissions( user_id: int ) -> tuple[ str, ... ]:
          ''' Gets user permissions as immutable tuple. '''
          permissions = fetch_permissions( user_id )
          return tuple( permissions )  # Immutable, specific type

* Use abstract collection types for parameters: ``__.cabc.Mapping``,
  ``__.cabc.Sequence``, ``__.cabc.Iterable``, ``__.cabc.Set``. Return
  concrete immutable types: ``tuple``, ``frozenset``, ``__.immut.Dictionary``.

  **❌ Avoid:**

  .. code-block:: python

      # Restricts callers unnecessarily
      def calculate_average( numbers: list[ float ] ) -> float:
          return sum( numbers ) / len( numbers )

      def find_common_elements(
          set1: set[ str ], set2: set[ str ]
      ) -> list[ str ]:
          common = set1 & set2
          return list( common )  # Mutable return type

  **✅ Prefer:**

  .. code-block:: python

      # Flexible parameters, specific returns
      def calculate_average( numbers: __.cabc.Sequence[ float ] ) -> float:
          ''' Calculates average of numeric sequence. '''
          return sum( numbers ) / len( numbers )

      def find_common_elements(
          set1: __.cabc.Set[ str ], set2: __.cabc.Set[ str ]
      ) -> frozenset[ str ]:
          ''' Finds common elements as immutable set. '''
          return frozenset( set1 & set2 )

* For optional parameters, prefer abstract types with concrete defaults that
  maintain the wide/narrow principle.

  **✅ Prefer:**

  .. code-block:: python

      def process_items(
          items: __.cabc.Sequence[ str ],
          filters: __.cabc.Sequence[ str ] = ( ),  # Empty tuple as default
          options: __.cabc.Mapping[ str, __.typx.Any ] = __.immut.Dictionary( )
      ) -> tuple[ str, ... ]:
          ''' Processes items with optional filters and configuration. '''
          filtered_items = [ item for item in items if all(
              filter_func( item ) for filter_func in filters ) ]
          # Apply options...
          return tuple( filtered_items )


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