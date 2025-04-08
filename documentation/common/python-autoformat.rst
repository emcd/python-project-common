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

:orphan:


*******************************************************************************
Python: Automatic Formatting
*******************************************************************************

No tools currently exist to enforce compliance with the Python coding standard.
However, if you are familiar with ``isort`` and ``yapf``, then the following
configurations may help you gain some sense of the guidelines. Note, however,
that these tools should not be applied to the code base as they will frequently
do the "wrong" thing. You will likely have more success with an LLM which is
good at following instructions.

.. include:: formatters.toml
   :code: toml
