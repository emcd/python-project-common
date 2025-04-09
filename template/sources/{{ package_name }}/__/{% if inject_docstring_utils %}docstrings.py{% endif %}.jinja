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


''' Docstring utilities. '''

# ruff: noqa: F403,F405


from __future__ import annotations

from . import doctab
from .imports import *


class Docstring( str ):
    ''' Dedicated docstring container. '''


def generate_docstring(
    *fragment_ids: type | Docstring | str,
    table: cabc.Mapping[ str, str ] = doctab.TABLE,
) -> str:
    ''' Sews together docstring fragments into clean docstring. '''
    from inspect import cleandoc, getdoc, isclass
    fragments: list[ str ] = [ ]
    for fragment_id in fragment_ids:
        if isclass( fragment_id ): fragment = getdoc( fragment_id ) or ''
        elif isinstance( fragment_id, Docstring ): fragment = fragment_id
        else: fragment = table[ fragment_id ]
        fragments.append( cleandoc( fragment ) )
    return '\n\n'.join( fragments )
