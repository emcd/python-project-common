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


''' Assert basic characteristics of Rust extension module. '''


from . import PACKAGE_NAME, cache_import_module


def test_000_sanity( ):
    ''' Extension module is sane. '''
    module = cache_import_module( f"{PACKAGE_NAME}._extension" )
    assert module.__package__ == PACKAGE_NAME
    assert module.__name__ == f"{PACKAGE_NAME}._extension"


def test_010_version_sync( ):
    ''' Extension module version matches package version. '''
    package = cache_import_module( PACKAGE_NAME )
    module = cache_import_module( f"{PACKAGE_NAME}._extension" )
    assert hasattr( module, '__version__' )
    assert isinstance( module.__version__, str )
    assert module.__version__ == package.__version__
