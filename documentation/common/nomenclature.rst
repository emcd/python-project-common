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
Nomenclature
*******************************************************************************

This guide presents core naming patterns and conventions for all supported
languages. For comprehensive verb vocabularies, see :doc:`nomenclature-latin`
for Latin-derived terms (project default) or :doc:`nomenclature-germanic` for
Germanic alternatives.

When working with third-party APIs or established codebases, it may be
appropriate to follow their existing naming conventions rather than those
presented here. The goal is consistency within a given context rather than
rigid adherence to these patterns.


Modules, Packages, and Crates
===============================================================================

- Prefer single-word names: ``users``, ``authentication``, ``storage``.


- Use plurals for collections of related modules or classes: ``parsers``,
  ``validators``.

- Use ``-ation`` suffixes for functionality areas: ``authentication``,
  ``configuration``.

- Avoid underscores by making portmanteau words: ``datastore`` not
  ``data_store``, ``userauth`` not ``user_auth``.


**Python distribution packages and Rust crates:** Prefer single words; use
``kebab-case`` if compound names are required:

    frigid
    emcd-projects

**Python and Rust modules:** Prefer single words; use ``snake_case`` if
compound names are required:

    processors    # plural for collection
    userauth      # portmanteau for "user authentication"
    configuration # -ation for functionality area


Classes
===============================================================================

General Guidance
-------------------------------------------------------------------------------

- Use ``Async`` suffix for asynchronous interfaces, if you need to distinguish
  between asynchronous and synchronous varieties with the same module or
  package.

- Avoid ``Type`` suffix except when fitting to existing framework. I.e., do
  **not** follow the pattern in Python's ``types`` module (``NoneType``,
  etc...) unless there is good reason to do so.


Abstract Classes
-------------------------------------------------------------------------------

- Suffix with ``Abstract`` for abstract base classes if you need to distinguish
  between concrete and abstract classes within the same module or package.
  However, prefer to name concrete classes with additional detail so that such
  distinction is not necessary.

- Use adjective names for interface-like classes when they describe
  capabilities.

.. code-block:: python

    class DictionaryAbstract:
        ''' Abstract base for dictionary types. '''

    class Dictionary( DictionaryAbstract ):
        ''' Concrete class derived from abstract one. '''

    class Comparable:
        ''' Interface for objects supporting comparison. '''

    class Immutable:
        ''' Interface for objects preventing modification. '''

**Rust traits** follow similar patterns:

- **Capability adjectives:** ``Sized``, ``Clone``, ``Send``, ``Sync``
- **Ability suffixes:** ``Readable``, ``Writable``, ``Comparable``
- **Action agents:** ``Iterator``, ``Parser``, ``Builder``, ``Formatter``
- **Behavior descriptions:** ``Default``, ``Debug``, ``Display``

.. code-block:: rust

    trait Comparable {
        fn compare( &self, other: &Self ) -> Ordering;
    }

    trait ConfigurationBuilder {
        fn build( self ) -> Configuration;
    }


Base Classes
-------------------------------------------------------------------------------

- Use ``Base`` or ``Common`` suffix for base classes.

- Use ``Extension``/``Supplement`` (Latin-derived) or ``Mixin`` (Germanic-like)
  suffix for mix-in classes. Choose the suffix which matches the rest of the
  name.

.. code-block:: python

    class DictionaryBase:
        ''' Base class for dictionary implementations. '''

    class LoggingMixin:
        ''' Adds logging capabilities to classes. '''


Container Classes
-------------------------------------------------------------------------------

Name based on behavior rather than implementation. I.e., talk about **what**
instances of a class do and not **how** they do it.

.. code-block:: python

    class ProducerDictionary:
        ''' Dictionary producing values on demand. '''

    class QueueAsync:
        ''' Queue with asynchronous interface. '''


Enum Classes
-------------------------------------------------------------------------------

- Use plural nouns for enum class names.

- Use PascalCase for enum members to reflect singleton semantics.

.. code-block:: python

    class States:
        Initial = auto( )
        Execution = auto( )
        Complete = auto( )


Exception Classes
-------------------------------------------------------------------------------

- Follow standard hierarchy: ``Omniexception`` -> ``Omnierror`` -> specific
  exceptions.

- Use present tense verbs with these patterns:

    - ``[<Noun>]<Verb>Failure`` for operation failures
    - ``[<Noun>]<Verb>Interruption`` for interrupted operations
    - ``[<Noun>]<Verb>Invalidity`` for invalid states/data

- Use ``[<Noun>]<Property>Error`` for other error cases.

.. code-block:: python

    class ConfigureFailure( Omnierror ):
        ''' Raised when configuration fails. '''

    class AttributeInvalidity( Omnierror ):
        ''' Raised when attribute value is invalid. '''

    class ProcessInterruption( Omniexception ):
        ''' Raised when process is interrupted. '''


Metaclasses
-------------------------------------------------------------------------------

- Use ``Class``/``Factory`` (Latin-derived) or ``Builder``/``Maker``
  (Germanic-derived) suffix.

.. code-block:: python

    class ValidatorClass( type ):
        ''' Metaclass for creating validator classes. '''

    class SetBuilder( type ):
        ''' Metaclass for building set classes. '''


Special Purpose Classes
-------------------------------------------------------------------------------

Use appropriate suffix pairs based on purpose:

- ``Proxy`` (Latin-derived) or ``Wrapper`` (Germanic-derived) for delegation
  patterns
- ``Coordinator``/``Manager``/``Supervisor`` (Latin-derived) or ``Overseer``
  (Germanic-derived) for resource management
- ``Spectator``/``View`` for limited access patterns

.. code-block:: python

    class WeakrefWrapper:
        ''' Wraps object with weak reference semantics. '''

    class ConnectionManager:
        ''' Manages database connections. '''

    class DictionaryView:
        ''' Provides read-only view of dictionary. '''


Variables and Attributes
===============================================================================

- Prefer single-word names: ``name``, ``count``, ``timeout``, ``callback``.

- Avoid repeating the class or function name in variable names:

  - ``User.name`` not ``User.user_name``
  - ``validate_email( address )`` not ``validate_email( email_address )``
  - ``parse_json( content )`` not ``parse_json( json_content )``

- Avoid truncations: prefer ``configuration`` over ``config``, ``options``
  over ``opts``, ``arguments`` over ``args``.

- Portmanteau words are acceptable: ``configfile`` instead of
  ``configuration_file``, ``envvar`` instead of ``environment_variable``.

- Use context-appropriate specificity: ``start_time`` when multiple time
  values exist, ``time`` when unambiguous.

.. code-block:: python

    class DatabaseConnection:
        timeout: float          # Not connection_timeout
        host: str               # Not database_host

    def validate_email( address: str ) -> str:  # Not email_address
        ''' Validates email address format. Returns address if valid. '''

    def parse_configuration( filename: str ) -> dict[ str, __.typx.Any ]:  # Not config_file
        ''' Parses configuration from file. '''


Constants and Module-Level Variables
===============================================================================

**True constants** (immutable values):

- Use ``ALL_CAPS`` with underscores separating words.
- Use suffixes for semantic grouping: ``TIMEOUT_DEFAULT``, ``TIMEOUT_MAXIMUM``,
  ``RETRIES_MAXIMUM`` not ``DEFAULT_TIMEOUT``, ``MAX_TIMEOUT``, ``MAX_RETRIES``.
- Group related constants with common prefixes: ``HTTP_OK``, ``HTTP_NOT_FOUND``,
  ``HTTP_SERVER_ERROR``.

**Module-level caches** (internal mutability):

- Use leading underscore: ``_connection_pool``, ``_configuration_cache``.
- These have internal mutability even though they cannot be reassigned as
  module attributes.

.. code-block:: python

    # True constants
    API_VERSION = '2.1.0'
    TIMEOUT_DEFAULT = 30.0
    TIMEOUT_MAXIMUM = 300.0
    RETRIES_MAXIMUM = 3

    HTTP_OK = 200
    HTTP_NOT_FOUND = 404
    HTTP_SERVER_ERROR = 500

    # Module-level caches (internal mutability)
    _connection_pool = ConnectionPool( )
    _cached_settings = { }


Functions
===============================================================================

General Patterns
-------------------------------------------------------------------------------

``<verb>_<noun>``: Where verb describes the action and noun describes the
target.

``<preposition>_<noun>``: For methods only. Chainable operations typically
returning modified copies.

For comprehensive verb vocabularies with detailed definitions, see
:doc:`nomenclature-latin` (project default) or :doc:`nomenclature-germanic`
(alternative terms).

Noun Placeholders
-------------------------------------------------------------------------------

- ``<attribute>``: Named property or field of an object
- ``<component>``: Distinct part of a larger system or application
- ``<condition>``: Boolean predicate or state
- ``<data>``: Raw or structured information, regardless of location
- ``<execution>``: Execution context (process, thread, task) managed by current
  process
- ``<feature>``: Optional functionality that can be enabled/disabled
- ``<format>``: Data serialization format (JSON, XML, etc.)
- ``<future>``: Planned future execution
- ``<object>``: In-process entity (instance of a Python class)
- ``<reactor>``: Callback or event handler
- ``<reservation>``: Claim on future resource usage
- ``<resource>``: Entity external to the current process (file, network
  service, etc.)
- ``<service>``: Long-running process or daemon external to current process
- ``<space>``: Memory or storage allocation
- ``<type>``: Python type or class

Preposition Prefixes
-------------------------------------------------------------------------------

- ``as_<format-or-type>``: Returns copy of object in different format or type.
  Chainable with other methods.

- ``from_<format-or-type>``: Class method that constructs object from specific
  format or type.

- ``with_<attribute>``: Returns copy of object with modified attributes.
  Chainable with other methods.

Function Suffixes
-------------------------------------------------------------------------------

The project uses a limited set of function suffixes to indicate specific
execution patterns:

- ``_async``: Indicates asynchronous execution.
- ``_continuous``: Indicates generator/iterator return type (alternative:
  ``_streaming`` when using Germanic-derived terms).
- ``_recursive``: Indicates recursive execution when this is part of the
  function's contract rather than an implementation detail.

Other execution patterns (parallel processing, batch operations, etc.) are
better expressed through specific function names or appropriate use of
threading/multiprocessing facilities.

When Not to Use Suffixes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Avoid suffixes for:

- Implementation details (``_cached``, ``_optimized``)
- Batch operations (use prefix ``mass_`` or ``multi_`` prefixes instead)
- In-place operations (use Python's established patterns like list methods)
- Development status (``_experimental``)
- Debugging aids (``_verbose``)
- Parallel processing (use appropriate concurrency primitives instead)


Environment Variables
===============================================================================

- Use ``ALL_CAPS`` with underscores separating words.
- Begin with package/application name: ``MYAPP_TRACE_LEVEL``,
  ``MYAPP_DATABASE_CONNECTION_URL``.
- Follow standard Unix conventions for system integration.

.. code-block:: shell

    # Application-specific variables
    MYAPP_LOG_LEVEL=INFO
    MYAPP_DATABASE_URL=postgresql://localhost/mydb
    MYAPP_CACHE_TIMEOUT=3600


Linguistic Consistency
===============================================================================

The project generally uses Latin-derived terms for both class and function
names. This preference arises from:

- Prevalence of Latin-derived terms in computer science
- More precise technical meanings in Latin-derived terms
- Larger vocabulary of available terms

Germanic-derived and Greek-derived terms may be appropriate when maintaining
linguistic consistency within:

- Related function names
- Class hierarchies
- Enum members
- Module-level names

Within individual names, maintain agreement between verbs and nouns:

- ``shape_set`` (Germanic-derived verb with Germanic-derived noun)
- ``validate_sequence`` (Latin-derived verb with Latin-derived noun)
- ``analyze_algorithm`` (Greek-derived verb with Greek-influenced noun)

Technical abbreviations (``str``, ``obj``), acronyms (``xml``, ``json``), and
some portmanteau words are linguistically neutral and can be used with terms
from any linguistic derivation.

When in doubt, prefer Latin-derived terms as the project default.


Vocabulary References
-------------------------------------------------------------------------------

For detailed verb catalogs with comprehensive definitions and usage guidance:

- :doc:`nomenclature-latin`: Complete Latin-derived verb vocabulary (project default)
- :doc:`nomenclature-germanic`: Germanic alternatives organized by semantic clusters
