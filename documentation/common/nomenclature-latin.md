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

<a id="latin-derived-verb-vocabulary"></a>
# Latin-derived Verb Vocabulary

This reference provides comprehensive definitions and usage guidance for Latin-derived verbs used in function naming. These terms serve as the project default vocabulary for consistent nomenclature.

For core naming patterns and structural conventions, see the main
[nomenclature guide](nomenclature.md). For Germanic alternatives, see the
[Germanic-derived verb vocabulary](nomenclature-germanic.md).

<a id="verb-prefixes-by-semantic-cluster"></a>
## Verb Prefixes by Semantic Cluster

<a id="analysis-and-discovery"></a>
### Analysis and Discovery

**assess\_\<data\>**  
Examines data to derive insights or patterns.

**discover\_\<value\>**  
Detects or determines value from environment or context.

**examine\_\<resource\>**  
Retrieves metadata about resource without accessing full content (file stats, HTTP HEAD).

**survey\_\<resource\>**  
Lists or enumerates members of external resource collection.

<a id="component-initialization"></a>
### Component Initialization

**configure\_\<component\>**  
Applies settings or parameters to component, preparing it for operation.

**prepare\_\<component\>**  
Fully initializes component, including registration of handlers/extensions.

<a id="computation"></a>
### Computation

**calculate\_\<value\>**  
Computes value from one or more inputs using defined algorithm.

<a id="data-operations"></a>
### Data Operations

**access\_\<object\>**  
Returns value via computed or indirect access (property getter, descriptor protocol). For in-process objects only.

**filter\_\<objects\>**  
Returns subset of objects matching specified criteria.

**modify\_\<object\>**  
Updates in-process object state. Alternative to `update_<resource>` for disambiguation.

**parse\_\<format\>**  
Extracts structured data from formatted input (JSON, XML).

**query\_\<resource\>**  
Performs structured data retrieval with parameters or filters.

**retrieve\_\<resource\>**  
Obtains copy of data from external resource. No release required.

**transform\_\<data\>**  
Changes data structure or format. Synonym: `convert_<data>`.

**update\_\<resource\>**  
Modifies state of external resource.

<a id="exception-handling-python-specific"></a>
### Exception Handling (Python-specific)

**intercept\_\<exceptions\>**  
Invokes functions while capturing their exceptions for later handling. Used primarily in concurrent execution contexts where multiple exceptions need collection.

<a id="persistence-and-serialization"></a>
### Persistence and Serialization

**restore\_\<object\>**  
Deserializes object from persistent storage.

**save\_\<object\>**  
Serializes object to persistent storage.

<a id="presentation-and-output"></a>
### Presentation and Output

**display\_\<data\>**  
Presents data in user-facing format. Synonym: `present_<data>`.

**render\_\<template\>**  
Produces output by combining template with data.

**report\_\<data\>**  
Collates data from analyses or diverse sources into a structured or human-readable form.

<a id="resource-lifecycle"></a>
### Resource Lifecycle

**acquire\_\<resource\>**  
Obtains exclusive access to shared resource requiring explicit release (mutex, database connection). Antonym: `release_<resource>`.

**allocate\_\<space\>**  
Reserves system memory or storage space for future use. Antonym: `deallocate_<space>`.

**create\_\<resource\>**  
Creates new resource external to current process (file, database table). Antonym: `delete_<resource>`.

**deallocate\_\<space\>**  
Frees previously allocated system memory or storage space. Antonym: `allocate_<space>`.

**delete\_\<resource\>**  
Removes resource external to current process. \[Python\]: For in-process objects, rely on garbage collection. Antonym: `create_<resource>`.

**ensure\_\<resource\>**  
Creates resource if it doesn't exist, returns existing resource if it does.

**produce\_\<object\>**  
Creates new instance in process memory. For external resource creation, see `create_<resource>`.

**release\_\<resource\>**  
Releases previously acquired shared resource. Antonym: `acquire_<resource>`.

<a id="scheduling-and-futures"></a>
### Scheduling and Futures

**cancel\_\<future-or-reservation\>**  
Revokes planned execution or resource claim. Antonym: `schedule_<execution>` and `reserve_<resource>`.

**request\_\<action\>**  
Initiates asynchronous operation, typically on remote service. Returns future or promise representing eventual completion.

**reserve\_\<resource\>**  
Claims resource for future use.

**schedule\_\<execution\>**  
Plans future execution of task or process.

<a id="state-management"></a>
### State Management

**activate\_\<execution-or-service\>**  
Starts execution context or service. For both in-process executions and external services. Antonym: `deactivate_<execution-or-service>`.

**deactivate\_\<execution-or-service\>**  
Stops execution context or service. Antonym: `activate_<execution-or-service>`.

**deregister\_\<reactor\>**  
Removes previously registered event handler or callback. Antonym: `register_<reactor>`.

**disable\_\<feature\>**  
Deactivates optional feature or functionality. Antonym: `enable_<feature>`.

**enable\_\<feature\>**  
Activates optional feature or functionality. Antonym: `disable_<feature>`.

**register\_\<reactor\>**  
Adds event handler or callback to registry. Antonym: `deregister_<reactor>`.

<a id="validation-and-testing"></a>
### Validation and Testing

**assert\_\<resource\>** \[Python\]  
Verifies resource exists or condition holds, raising exception if not. \[Rust\]: Panics if condition fails.

**is\_\<member-or-state\>**  
Tests type membership or current state. Returns boolean.

**probe\_\<resource\>**  
Tests resource accessibility or status. Returns boolean indicating availability.

**test\_\<assertion\>**  
Verifies specific assertion about code behavior. Note: Only for use in test suites, not in public interfaces.

**validate\_\<object\>** \[Python\]  
Returns object if valid, raises exception if invalid. \[Rust\]: Returns `Result::Ok` containing object if valid else `Result::Err`.

**verify\_\<condition\>**  
Tests condition or state. Returns boolean.
