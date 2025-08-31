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
Latin-derived Verb Vocabulary
*******************************************************************************

This reference provides comprehensive definitions and usage guidance for
Latin-derived verbs used in function naming. These terms serve as the project
default vocabulary for consistent nomenclature.

For core naming patterns and structural conventions, see the main
:doc:`nomenclature` guide. For Germanic alternatives, see
:doc:`nomenclature-germanic`.


Verb Prefixes by Semantic Cluster
===============================================================================

Analysis and Discovery
-------------------------------------------------------------------------------

**assess_<data>**
    Examines data to derive insights or patterns.

**discover_<value>**
    Detects or determines value from environment or context.

**examine_<resource>**
    Retrieves metadata about resource without accessing full content (file
    stats, HTTP HEAD).

**survey_<resource>**
    Lists or enumerates members of external resource collection.


Component Initialization
-------------------------------------------------------------------------------

**configure_<component>**
    Applies settings or parameters to component, preparing it for operation.

**prepare_<component>**
    Fully initializes component, including registration of
    handlers/extensions.


Computation
-------------------------------------------------------------------------------

**calculate_<value>**
    Computes value from one or more inputs using defined algorithm.


Data Operations
-------------------------------------------------------------------------------

**access_<object>**
    Returns value via computed or indirect access (property getter, descriptor
    protocol). For in-process objects only.

**filter_<objects>**
    Returns subset of objects matching specified criteria.

**modify_<object>**
    Updates in-process object state. Alternative to ``update_<resource>`` for
    disambiguation.

**parse_<format>**
    Extracts structured data from formatted input (JSON, XML).

**query_<resource>**
    Performs structured data retrieval with parameters or filters.

**retrieve_<resource>**
    Obtains copy of data from external resource. No release required.

**transform_<data>**
    Changes data structure or format. Synonym: ``convert_<data>``.

**update_<resource>**
    Modifies state of external resource.


Exception Handling (Python-specific)
-------------------------------------------------------------------------------

**intercept_<exceptions>**
    Invokes functions while capturing their exceptions for later handling. Used
    primarily in concurrent execution contexts where multiple exceptions need
    collection.


Persistence and Serialization
-------------------------------------------------------------------------------

**restore_<object>**
    Deserializes object from persistent storage.

**save_<object>**
    Serializes object to persistent storage.


Presentation and Output
-------------------------------------------------------------------------------

**display_<data>**
    Presents data in user-facing format. Synonym: ``present_<data>``.

**render_<template>**
    Produces output by combining template with data.

**report_<data>**
    Collates data from analyses or diverse sources into a structured or
    human-readable form.


Resource Lifecycle
-------------------------------------------------------------------------------

**acquire_<resource>**
    Obtains exclusive access to shared resource requiring explicit release
    (mutex, database connection). Antonym: ``release_<resource>``.

**allocate_<space>**
    Reserves system memory or storage space for future use. Antonym:
    ``deallocate_<space>``.

**create_<resource>**
    Creates new resource external to current process (file, database table).
    Antonym: ``delete_<resource>``.

**deallocate_<space>**
    Frees previously allocated system memory or storage space. Antonym:
    ``allocate_<space>``.

**delete_<resource>**
    Removes resource external to current process. [Python]: For in-process
    objects, rely on garbage collection. Antonym: ``create_<resource>``.

**ensure_<resource>**
    Creates resource if it doesn't exist, returns existing resource if it does.

**produce_<object>**
    Creates new instance in process memory. For external resource creation, see
    ``create_<resource>``.

**release_<resource>**
    Releases previously acquired shared resource. Antonym:
    ``acquire_<resource>``.


Scheduling and Futures
-------------------------------------------------------------------------------

**cancel_<future-or-reservation>**
    Revokes planned execution or resource claim. Antonym:
    ``schedule_<execution>`` and ``reserve_<resource>``.

**request_<action>**
    Initiates asynchronous operation, typically on remote service. Returns
    future or promise representing eventual completion.

**reserve_<resource>**
    Claims resource for future use.

**schedule_<execution>**
    Plans future execution of task or process.


State Management
-------------------------------------------------------------------------------

**activate_<execution-or-service>**
    Starts execution context or service. For both in-process executions and
    external services. Antonym: ``deactivate_<execution-or-service>``.

**deactivate_<execution-or-service>**
    Stops execution context or service. Antonym:
    ``activate_<execution-or-service>``.

**deregister_<reactor>**
    Removes previously registered event handler or callback. Antonym:
    ``register_<reactor>``.

**disable_<feature>**
    Deactivates optional feature or functionality. Antonym:
    ``enable_<feature>``.

**enable_<feature>**
    Activates optional feature or functionality. Antonym: ``disable_<feature>``.

**register_<reactor>**
    Adds event handler or callback to registry. Antonym: ``deregister_<reactor>``.


Validation and Testing
-------------------------------------------------------------------------------

**assert_<resource>** [Python]
    Verifies resource exists or condition holds, raising exception if not.
    [Rust]: Panics if condition fails.

**is_<member-or-state>**
    Tests type membership or current state. Returns boolean.

**probe_<resource>**
    Tests resource accessibility or status. Returns boolean indicating
    availability.

**test_<assertion>**
    Verifies specific assertion about code behavior. Note: Only for use in test
    suites, not in public interfaces.

**validate_<object>** [Python]
    Returns object if valid, raises exception if invalid. [Rust]: Returns
    ``Result::Ok`` containing object if valid else ``Result::Err``.

**verify_<condition>**
    Tests condition or state. Returns boolean.