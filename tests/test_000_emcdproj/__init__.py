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


''' Package of tests.

    Common imports, constants, and utilities for tests.
'''


import collections.abc as   cabc
import contextlib as        ctxl
import dataclasses as       dcls
import                      os
import                      types
import                      unicodedata

from pathlib import Path, PurePosixPath

import typing_extensions as typx

from absence import Absential, absent, is_absent



PACKAGE_NAME = 'emcdproj'
PACKAGES_NAMES = ( PACKAGE_NAME, )


_modules_cache: dict[ str, types.ModuleType ] = { }
def cache_import_module( qname: str ) -> types.ModuleType:
    ''' Imports module from package by name and caches it. '''
    from importlib import import_module
    package_name, *maybe_module_name = qname.rsplit( '.', maxsplit = 1 )
    if not maybe_module_name: arguments = ( qname, )
    else: arguments = ( f".{maybe_module_name[0]}", package_name, )
    if qname not in _modules_cache:
        _modules_cache[ qname ] = import_module( *arguments )
    return _modules_cache[ qname ]


@ctxl.contextmanager
def create_test_files(
    base_dir: Path, files: dict[ str, str ]
) -> typx.Iterator[ None ]:
    ''' Creates test files in specified directory. '''
    created: list[ Path ] = [ ]
    try: # pylint: disable=too-many-try-statements
        for relpath, content in files.items( ):
            filepath = base_dir / relpath
            filepath.parent.mkdir( parents = True, exist_ok = True )
            filepath.write_text( content, newline = '' )
            created.append( filepath )
        yield
    finally:
        for filepath in reversed( created ):
            if filepath.exists( ): filepath.unlink( )


@dcls.dataclass
class Pathetic:
    ''' Handles cross-platform path nativization and normalization. '''

    _windows_roots_map: cabc.Mapping[ str, str ] = (
        dcls.field( default_factory = lambda: { 'C:\\': '/' } ) )

    def compare(
        self,
        path1: bytes | str | os.PathLike,
        path2: bytes | str | os.PathLike,
    ) -> bool:
        ''' Compares two paths, normalizing across platforms. '''
        # TODO? Nativize paths and then compare.
        p1 = Path( path1 ) if isinstance( path1, ( bytes, str ) ) else path1
        p2 = Path( path2 ) if isinstance( path2, ( bytes, str ) ) else path2
        return self.normalize( p1 ) == self.normalize( p2 )

    # TODO: nativize

    def normalize(
        self,
        path: Path,
        case_function: Absential[ cabc.Callable[ [ str ], str ] ] = absent,
        unicode_nf: Absential[ typx.Literal[ 'NFC', 'NFD' ] ] = absent,
    ) -> PurePosixPath:
        ''' Normalizes path into a pure POSIX path.

            Windows drive letters and UNC shares are remapped, as necessary.
        '''
        parts = path.parts
        if path.drive:
            parts = ( self._windows_roots_map[ path.root ], *parts[ 1 : ] )
        if not is_absent( unicode_nf ):
            parts = tuple( map(
                lambda s: unicodedata.normalize( unicode_nf, s ), parts ) )
        if not is_absent( case_function ):
            parts = tuple( map( case_function, parts ) )
        return PurePosixPath( *parts )


def _discover_module_names( package_name: str ) -> tuple[ str, ... ]:
    package = cache_import_module( package_name )
    if not package.__file__: return ( )
    return tuple(
        path.stem
        for path in Path( package.__file__ ).parent.glob( '*.py' )
        if      path.name not in ( '__init__.py', '__main__.py' )
            and path.is_file( ) )


MODULES_NAMES_BY_PACKAGE_NAME = types.MappingProxyType( {
    name: _discover_module_names( name ) for name in PACKAGES_NAMES } )
PACKAGES_NAMES_BY_MODULE_QNAME = types.MappingProxyType( {
    f"{subpackage_name}.{module_name}": subpackage_name
    for subpackage_name in PACKAGES_NAMES
    for module_name in MODULES_NAMES_BY_PACKAGE_NAME[ subpackage_name ] } )
MODULES_QNAMES = tuple( PACKAGES_NAMES_BY_MODULE_QNAME.keys( ) )
MODULES_NAMES_BY_MODULE_QNAME = types.MappingProxyType( {
    name: name.rsplit( '.', maxsplit = 1 )[ -1 ]
    for name in PACKAGES_NAMES_BY_MODULE_QNAME.keys( ) } )
