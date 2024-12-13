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


''' Assert correct function of docstring utilities. '''


import pytest

from . import PACKAGE_NAME, cache_import_module


MODULE_QNAME = f"{PACKAGE_NAME}.__.docstrings"


def test_100_container_init( ):
    ''' Docstring container is a string subclass. '''
    module = cache_import_module( MODULE_QNAME )
    doc = module.Docstring( 'test' )
    assert isinstance( doc, str )
    assert 'test' == doc


def test_200_generator_fragments( ):
    ''' Docstring generator handles various fragment types. '''
    class Example:
        ''' Class docstring. '''

    module = cache_import_module( MODULE_QNAME )
    result = module.generate_docstring(
        Example,
        module.Docstring( 'Container string' ) )
    assert 'Class docstring. \n\nContainer string' == result


def test_210_generator_lookup( ):
    ''' Docstring generator uses provided lookup table. '''
    module = cache_import_module( MODULE_QNAME )
    test_table = { 'test_key': 'Test value' }
    result = module.generate_docstring( 'test_key', table = test_table )
    assert 'Test value' == result
    with pytest.raises( KeyError ):
        module.generate_docstring( 'nonexistent', table = test_table )
