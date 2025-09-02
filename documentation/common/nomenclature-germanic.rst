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
Germanic-derived Verb Vocabulary
*******************************************************************************

This reference provides Germanic alternatives to Latin-derived verbs organized
by semantic clusters. These terms can be used to maintain linguistic
consistency within related function names, class hierarchies, or module-level
names.

For core naming patterns and structural conventions, see the main
:doc:`nomenclature` guide. For Latin-derived terms (project default), see
:doc:`nomenclature-latin`.


Germanic Naming Philosophy
===============================================================================

Germanic-derived terms often provide:

- **Directness**: ``get`` vs ``access``, ``make`` vs ``create``
- **Concrete imagery**: ``grab`` vs ``acquire``, ``sniff`` vs ``examine``  
- **Technical familiarity**: ``ping`` vs ``probe``, ``dump`` vs ``save``
- **Compound flexibility**: ``setup``, ``handoff``, ``unswitch``

Germanic terms should only be used to maintain consistency with existing 
terminology or because they form a better self-contained cluster of names than
the equivalent Latin-derived terms (e.g., for the variants of some enums).

Verb Prefixes by Semantic Cluster
===============================================================================

Analysis and Discovery
-------------------------------------------------------------------------------

**find_<value>** (discover)
    Detects or determines value from environment or context.

**list_<resource>** (survey)
    Lists or enumerates members of external resource collection.

**sniff_<resource>** (examine)
    Retrieves metadata about resource without accessing full content. Informal
    but established in technical contexts.

**weigh_<data>** (assess)
    Examines data to derive insights or patterns.


Component Initialization
-------------------------------------------------------------------------------

**ready_<component>** (prepare)
    Fully initializes component, including registration of handlers/extensions.
    Used as verb, not adjective.

**setup_<component>** (configure)
    Applies settings or parameters to component, preparing it for operation.
    Compound from "set up".


Computation
-------------------------------------------------------------------------------

**reckon_<value>** (calculate)
    Computes value from one or more inputs using defined algorithm.


Data Operations
-------------------------------------------------------------------------------

**ask_<resource>** (query/request)
    Performs structured data retrieval with parameters or filters. Also used
    for initiating requests.

**change_<object>** (modify)
    Updates in-process object state. Alternative to ``freshen_<resource>`` for
    disambiguation.

**fetch_<resource>** (retrieve)
    Obtains copy of data from external resource. No release required.

**freshen_<resource>** (update)
    Modifies state of external resource.

**get_<object>** (access)
    Returns value via computed or indirect access (property getter, descriptor
    protocol). For in-process objects only.

**shape_<data>** (transform)
    Changes data structure or format. Avoids Latin ``re-`` prefix.

**sift_<objects>** (filter)
    Returns subset of objects matching specified criteria.

**split_<format>** (parse)
    Extracts structured data from formatted input (JSON, XML).


Exception Handling
-------------------------------------------------------------------------------

**catch_<exceptions>** (intercept)
    Invokes functions while capturing their exceptions for later handling.


Persistence and Serialization
-------------------------------------------------------------------------------

**load_<object>** (restore)
    Deserializes object from persistent storage. Common pair with ``dump``.

**dump_<object>** (save)
    Serializes object to persistent storage. Common pair with ``load``.


Presentation and Output
-------------------------------------------------------------------------------

**fillin_<template>** or **mold_<template>** (render)
    Produces output by combining template with data. Compound from "fill in".

**show_<data>** (display)
    Presents data in user-facing format.

**tell_<data>** (report)
    Collates data from analyses or diverse sources into a structured or
    human-readable form.


Resource Lifecycle
-------------------------------------------------------------------------------

**free_<space>** (deallocate/release)
    Frees previously allocated system memory or storage space. Also releases
    previously acquired shared resource.

**grab_<resource>** (acquire)
    Obtains exclusive access to shared resource requiring explicit release.
    Common in technical contexts. Antonym: ``free_<resource>``.

**kill_<resource>** (delete)
    Removes resource external to current process. Antonym: ``make_<resource>``.

**make_<resource>** (create)
    Creates new resource external to current process (file, database table).
    Antonym: ``kill_<resource>``.

**new_<object>** (produce)
    Creates new instance in process memory. Verb form familiar to C++
    programmers.

**righten_<resource>** (ensure)
    Creates resource if it doesn't exist, returns existing resource if it does.
    Slightly archaic but precise.

**slot_<space>** (allocate)
    Reserves system memory or storage space for future use. Antonym:
    ``free_<space>``.


Scheduling and Futures
-------------------------------------------------------------------------------

**earmark_<resource>** (reserve)
    Claims resource for future use.

**handoff_<execution>** (schedule)
    Plans future execution of task or process. Compound from "hand off".

**stop_<future-or-reservation>** (cancel)
    Revokes planned execution or resource claim. Also used for deactivation.


State Management
-------------------------------------------------------------------------------

**enroll_<reactor>** (register)
    Adds event handler or callback to registry. Antonym: ``unenroll_<reactor>``.

**start_<execution-or-service>** (activate)
    Starts execution context or service. For both in-process executions and
    external services. Antonym: ``stop_<execution-or-service>``.

**switch_<feature>** (enable)
    Activates optional feature or functionality. Pairs with ``unswitch``.
    Antonym: ``unswitch_<feature>``.

**unenroll_<reactor>** (deregister)
    Removes previously registered event handler or callback. Germanic ``un-``
    prefix pattern. Antonym: ``enroll_<reactor>``.

**unswitch_<feature>** (disable)
    Deactivates optional feature or functionality. Neologism; pairs with
    ``switch``. Antonym: ``switch_<feature>``.


Validation and Testing
-------------------------------------------------------------------------------

**ping_<resource>** (probe)
    Tests resource accessibility or status. From network terminology indicating
    basic connectivity check.

**sound_<object>** (validate)
    Returns object if valid, raises exception if invalid. Archaic but precise
    meaning related to structural integrity.

**swear_<resource>** (assert)
    Verifies resource exists or condition holds, raising exception if not.
    Alternative semantic meaning emphasizing commitment.

**truth_<condition>** (verify)
    Tests condition or state. Used as verb: "to tell truth" about condition.


