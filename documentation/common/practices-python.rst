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

* For visual formatting of multi-line imports, use parentheses with proper indentation.

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

  The :ref:`DataProcessor example <comprehensive-example>` demonstrates this principle:
  ``process_user_data`` accepts wide parameter types (``__.cabc.Sequence[ UserRecord ]``
  for maximum caller flexibility) while returning a narrow, specific type 
  (``__.immut.Dictionary[ str, UserRecord ]``) that provides clear guarantees.

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