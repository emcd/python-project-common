<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->

<a id="germanic-derived-verb-vocabulary"></a>
# Germanic-derived Verb Vocabulary

This reference provides Germanic alternatives to Latin-derived verbs organized by semantic clusters. These terms can be used to maintain linguistic consistency within related function names, class hierarchies, or module-level names.

For core naming patterns and structural conventions, see the main
[nomenclature guide](nomenclature.md). For Latin-derived terms (project
default), see the [Latin-derived verb vocabulary](nomenclature-latin.md).

<a id="germanic-naming-philosophy"></a>
## Germanic Naming Philosophy

Germanic-derived terms often provide:

- **Directness**: `get` vs `access`, `make` vs `create`
- **Concrete imagery**: `grab` vs `acquire`, `sniff` vs `examine`
- **Technical familiarity**: `ping` vs `probe`, `dump` vs `save`
- **Compound flexibility**: `setup`, `handoff`, `unswitch`

Germanic terms should only be used to maintain consistency with existing terminology or because they form a better self-contained cluster of names than the equivalent Latin-derived terms (e.g., for the variants of some enums).

<a id="verb-prefixes-by-semantic-cluster"></a>
## Verb Prefixes by Semantic Cluster

<a id="analysis-and-discovery"></a>
### Analysis and Discovery

**find\_\<value\>** (discover)  
Detects or determines value from environment or context.

**list\_\<resource\>** (survey)  
Lists or enumerates members of external resource collection.

**sniff\_\<resource\>** (examine)  
Retrieves metadata about resource without accessing full content. Informal but established in technical contexts.

**weigh\_\<data\>** (assess)  
Examines data to derive insights or patterns.

<a id="component-initialization"></a>
### Component Initialization

**ready\_\<component\>** (prepare)  
Fully initializes component, including registration of handlers/extensions. Used as verb, not adjective.

**setup\_\<component\>** (configure)  
Applies settings or parameters to component, preparing it for operation. Compound from "set up".

<a id="computation"></a>
### Computation

**reckon\_\<value\>** (calculate)  
Computes value from one or more inputs using defined algorithm.

<a id="data-operations"></a>
### Data Operations

**ask\_\<resource\>** (query/request)  
Performs structured data retrieval with parameters or filters. Also used for initiating requests.

**change\_\<object\>** (modify)  
Updates in-process object state. Alternative to `freshen_<resource>` for disambiguation.

**fetch\_\<resource\>** (retrieve)  
Obtains copy of data from external resource. No release required.

**freshen\_\<resource\>** (update)  
Modifies state of external resource.

**get\_\<object\>** (access)  
Returns value via computed or indirect access (property getter, descriptor protocol). For in-process objects only.

**shape\_\<data\>** (transform)  
Changes data structure or format. Avoids Latin `re-` prefix.

**sift\_\<objects\>** (filter)  
Returns subset of objects matching specified criteria.

**split\_\<format\>** (parse)  
Extracts structured data from formatted input (JSON, XML).

<a id="exception-handling"></a>
### Exception Handling

**catch\_\<exceptions\>** (intercept)  
Invokes functions while capturing their exceptions for later handling.

<a id="persistence-and-serialization"></a>
### Persistence and Serialization

**load\_\<object\>** (restore)  
Deserializes object from persistent storage. Common pair with `dump`.

**dump\_\<object\>** (save)  
Serializes object to persistent storage. Common pair with `load`.

<a id="presentation-and-output"></a>
### Presentation and Output

**fillin\_\<template\>** or **mold\_\<template\>** (render)  
Produces output by combining template with data. Compound from "fill in".

**show\_\<data\>** (display)  
Presents data in user-facing format.

**tell\_\<data\>** (report)  
Collates data from analyses or diverse sources into a structured or human-readable form.

<a id="resource-lifecycle"></a>
### Resource Lifecycle

**free\_\<space\>** (deallocate/release)  
Frees previously allocated system memory or storage space. Also releases previously acquired shared resource.

**grab\_\<resource\>** (acquire)  
Obtains exclusive access to shared resource requiring explicit release. Common in technical contexts. Antonym: `free_<resource>`.

**kill\_\<resource\>** (delete)  
Removes resource external to current process. Antonym: `make_<resource>`.

**make\_\<resource\>** (create)  
Creates new resource external to current process (file, database table). Antonym: `kill_<resource>`.

**new\_\<object\>** (produce)  
Creates new instance in process memory. Verb form familiar to C++ programmers.

**righten\_\<resource\>** (ensure)  
Creates resource if it doesn't exist, returns existing resource if it does. Slightly archaic but precise.

**slot\_\<space\>** (allocate)  
Reserves system memory or storage space for future use. Antonym: `free_<space>`.

<a id="scheduling-and-futures"></a>
### Scheduling and Futures

**earmark\_\<resource\>** (reserve)  
Claims resource for future use.

**handoff\_\<execution\>** (schedule)  
Plans future execution of task or process. Compound from "hand off".

**stop\_\<future-or-reservation\>** (cancel)  
Revokes planned execution or resource claim. Also used for deactivation.

<a id="state-management"></a>
### State Management

**enroll\_\<reactor\>** (register)  
Adds event handler or callback to registry. Antonym: `unenroll_<reactor>`.

**start\_\<execution-or-service\>** (activate)  
Starts execution context or service. For both in-process executions and external services. Antonym: `stop_<execution-or-service>`.

**switch\_\<feature\>** (enable)  
Activates optional feature or functionality. Pairs with `unswitch`. Antonym: `unswitch_<feature>`.

**unenroll\_\<reactor\>** (deregister)  
Removes previously registered event handler or callback. Germanic `un-` prefix pattern. Antonym: `enroll_<reactor>`.

**unswitch\_\<feature\>** (disable)  
Deactivates optional feature or functionality. Neologism; pairs with `switch`. Antonym: `switch_<feature>`.

<a id="validation-and-testing"></a>
### Validation and Testing

**ping\_\<resource\>** (probe)  
Tests resource accessibility or status. From network terminology indicating basic connectivity check.

**sound\_\<object\>** (validate)  
Returns object if valid, raises exception if invalid. Archaic but precise meaning related to structural integrity.

**swear\_\<resource\>** (assert)  
Verifies resource exists or condition holds, raising exception if not. Alternative semantic meaning emphasizing commitment.

**truth\_\<condition\>** (verify)  
Tests condition or state. Used as verb: "to tell truth" about condition.
