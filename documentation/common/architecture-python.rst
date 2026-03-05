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
Architecture Documentation (Python)
*******************************************************************************

This guide contains Python-template-specific architectural notes.
For language-neutral architectural documentation practices, see
:doc:`architecture`.

The ``__`` Subpackage Pattern
===============================================================================

The double underscore (``__``) subpackage acts as a centralized import hub for
Python packages.

Core Concept
-------------------------------------------------------------------------------

Each Python package includes a ``__`` subdirectory containing:

* ``__init__.py``: Re-exports commonly used imports.
* ``imports.py``: Raw imports from external libraries.
* ``nomina.py``: Project-specific naming constants and conventions.

Primary Benefits
-------------------------------------------------------------------------------

**Namespace Management**

* Prevents pollution of individual module namespaces.
* Provides consistent access to common dependencies.
* Reduces import statement duplication and maintenance overhead.

**Performance and Maintenance**

* Centralizes common import costs.
* Supports targeted direct imports where performance matters.
* Allows common import changes to propagate through the package consistently.

Usage Pattern
-------------------------------------------------------------------------------

All modules use the same import pattern regardless of package depth:

.. code-block:: python

    # In any module at any package level
    from . import __

    # Usage throughout the module
    def process_data( items: __.cabc.Sequence[ str ] ) -> __.immut.Dictionary:
        ''' Processes sequence items into immutable dictionary. '''
        return __.immut.Dictionary( processed = True, count = len( items ) )

Cascading Import Hierarchy
-------------------------------------------------------------------------------

When projects grow to include subpackages, the pattern extends naturally:

* Each subpackage maintains its own ``__.py`` file.
* Subpackages inherit parent imports with ``from ..__ import *``.
* Each level can add specialized imports while retaining inherited ones.
* Deep subpackages gain consistent access to shared imports through the
  hierarchy.

Nested import resolution follows a predictable chain:
``nested/__.py`` → ``parent/__.py`` → ``root/__/imports.py``.

Subpackage Implementation Pattern
-------------------------------------------------------------------------------

.. code-block:: python

    # package/subpackage/__.py
    ''' Internal imports for subpackage functionality. '''

    # ruff: noqa: F403,F401

    # Additional specialized imports as needed
    import specialized_library

    from ..__ import *  # Inherit all parent imports
    from ..exceptions import *  # Package exceptions (if available)

All subpackage modules keep the same interface:

.. code-block:: python

    # package/subpackage/module.py
    from . import __

    def specialized_function(
        data: __.cabc.Sequence[ __.typx.Any ]
    ) -> __.immut.Dictionary:
        ''' Processes specialized data using inherited imports. '''
        return __.immut.Dictionary( processed = True, specialized = True )

Python Testing Organization
===============================================================================

Use :doc:`tests-python` for Python-specific test layout and workflow
expectations.
