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
Release Notes
*******************************************************************************

.. towncrier release notes start

Emcdproj 1.31 (2025-07-16)
==========================

Repairs
-------

- CLI: Do not expose application information as a configurable. No strong reason
  to do so and now requires a default name, due to breaking change upstream.


Emcdproj 1.29.1 (2025-07-12)
============================

Repairs
-------

- Properly detect data directory when running from installed package
  distribution.


Emcdproj 1.29 (2025-07-11)
==========================

Enhancements
------------

- CLI: Enable environment detection. Add concealment and immutability to package modules.
- Copier Template: Add write-tests and write-release-notes custom slash commands. Enhance existing release commands with improved guidance on cherry-picking commits and development cycle management.


Emcdproj 1.28 (2025-07-10)
==========================

Repairs
-------

- Website: Ensure that first release publication of documentation and coverage
  reports succeeds.


Emcdproj 1.24 (2025-06-29)
==========================

Enhancements
------------

- Website: Add --production flag for safe publication branch updates.
- Website: Add --use-extant flag to preserve existing published versions.
- Website: Add stable and development release table with persistent URLs.
- Website: Add survey subcommand to list all published versions.
- Website: Generate coverage badges in each version subdirectory.


Emcdproj 1.22 (2025-06-14)
==========================

Enhancements
------------

- Lock dependencies ahead of breaking changes.


Emcdproj 1.18 (2025-05-27)
==========================

Enhancements
------------

- Add '--preserve' flag to 'template validate' subcommand. Prevents cleanup of
  temporary directory allocated for Copier template validation which allows
  inspection of generated files.


Repairs
-------

- Fix description of 'template' subcommand.


Emcdproj 1.17 (2025-04-30)
==========================

Enhancements
------------

- New CLI subcommand 'template' to validate changes to Copier template with some
  preset. Currently available presets are 'default' and 'maximum'.


emcd-projects 1.15 (2025-04-08)
===============================

Enhancements
------------

- Update API documentation. Fix internals documentation.


emcd-projects 1.14 (2025-04-08)
===============================

Enhancements
------------

- Ability to update static website with documentation and code coverage report
  for particular package version.
