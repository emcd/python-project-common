# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Common imports used throughout the package. '''

# ruff: noqa: F401


import                      abc
import collections.abc as   cabc
import contextlib as        ctxl
import                      enum
import                      io
import                      json
import                      math
import                      os
import                      subprocess
import                      shutil
import                      sys
import                      tempfile
import                      types

from pathlib import Path

import                      appcore
import frigid as            immut
import typing_extensions as typx
# --- BEGIN: Injected by Copier ---
import tyro
# --- END: Injected by Copier ---

from absence import Absential, absent, is_absent
from appcore.state import Globals


simple_tyro_class = tyro.conf.configure( )
standard_tyro_class = tyro.conf.configure( tyro.conf.OmitArgPrefixes )
