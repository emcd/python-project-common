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
TOML Configuration Practices
*******************************************************************************

This guide covers **TOML-specific configuration design patterns and organizational decisions**.
For general guidance applicable to all languages, see the main :doc:`practices`.
For guidance on TOML formatting and visual presentation, see the :doc:`style-toml`.

Configuration Design
===============================================================================

* Prefer table arrays with ``name`` fields over proliferating custom subtables.
  This approach scales better and reduces configuration complexity.

  **❌ Avoid - custom subtables:**

  .. code-block:: toml

      [database]
      host = 'localhost'

      [database.primary]
      port = 5432
      timeout = 30

      [database.replica] 
      port = 5433
      timeout = 15

  **✅ Prefer - table arrays with name field:**

  .. code-block:: toml

      [[database]]
      name = 'primary'
      host = 'localhost'
      port = 5432
      timeout = 30

      [[database]]
      name = 'replica'
      host = 'localhost' 
      port = 5433
      timeout = 15

* Apply nomenclature guidelines from :doc:`nomenclature` to key and table names.
  Use Latin-derived words when they are the established norm in the domain.

Key Naming Conventions
===============================================================================

* Use hyphens instead of underscores in key names for better ergonomics and
  visual clarity.

  **❌ Avoid:**

  .. code-block:: toml

      max_connections = 100
      retry_count = 3
      database_url = 'postgresql://localhost/db'

  **✅ Prefer:**

  .. code-block:: toml

      max-connections = 100
      retry-count = 3
      database-url = 'postgresql://localhost/db'

* Follow the project's nomenclature patterns:

  - Use suffix patterns: ``timeout-default``, ``connections-maximum``
  - Use Latin-derived terms for consistency with the broader project
  - Group related keys with common prefixes: ``server-host``, ``server-port``, ``server-timeout``

Formatting Standards
===============================================================================

* Use single quotes for string values unless escapes are needed, in which case
  use double quotes.

  **✅ Prefer:**

  .. code-block:: toml

      name = 'example-service'
      pattern = 'user-.*'
      
      # Use double quotes when escapes are needed
      windows-path = "C:\\Program Files\\Example"

* Keep arrays and inline tables on single lines when they fit within reasonable length.
  For longer arrays, use multi-line format with trailing commas.

  **✅ Prefer:**

  .. code-block:: toml

      ports = [ 8080, 8443, 9090 ]
      server = { host = 'localhost', port = 8080, timeout = 30 }

      # Multi-line for longer arrays
      allowed-origins = [
          'https://example.com',
          'https://api.example.com',
      ]

Configuration Organization
===============================================================================

* Group related configuration keys into logical sections with descriptive
  table names.

  **✅ Prefer:**

  .. code-block:: toml

      [server]
      host = 'localhost'
      port = 8080
      max-connections = 100
      timeout-default = 30

      [database]
      url = 'postgresql://localhost/mydb'
      connections-maximum = 10
      timeout-query = 15

      [logging]
      level = 'INFO'
      file-path = '/var/log/myapp.log'
      rotation-size = '10MB'

* Use consistent patterns across configuration files in the project.

* Document complex or non-obvious configuration choices with comments.

.. todo::

   Expand TOML configuration practices with:
   
   - Environment integration patterns
   - Security considerations for configuration files
   - Configuration validation patterns
   - Environment variable integration strategies
   - Configuration file composition and inheritance
   - Deployment-specific configuration management
   - Configuration testing approaches