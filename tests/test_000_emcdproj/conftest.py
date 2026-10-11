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


''' Test fixtures. '''


import tempfile

from contextlib import AsyncExitStack
from pathlib import Path

import pytest
import typing_extensions as typx

from platformdirs import PlatformDirs

from .__ import PACKAGE_NAME, cache_import_module


@pytest.fixture
def provide_tempdir( ) -> typx.Iterator[ Path ]:
    ''' Provides temporary directory for test isolation. '''
    with tempfile.TemporaryDirectory( ) as tmpdir:
        yield Path( tmpdir )


def pytest_sessionfinish( session, exitstatus ):
    if exitstatus == 5:  # pytest exit code for "no tests collected"
        session.exitstatus = 0



@pytest.fixture
def application( ):
    ''' Provides appcore application module. '''
    return cache_import_module( "appcore.application" )


@pytest.fixture
def distribution( ):
    ''' Provides appcore distribution module. '''
    return cache_import_module( "appcore.distribution" )


@pytest.fixture
def imports( ):
    ''' Provides internal imports package. '''
    return cache_import_module( f"{ PACKAGE_NAME }.__.imports" )


@pytest.fixture
def state( ):
    ''' Provides appcore state module. '''
    return cache_import_module( "appcore.state" )


@pytest.fixture
def exceptions( ):
    ''' Provides exceptions module. '''
    return cache_import_module( f"{ PACKAGE_NAME }.exceptions" )


@pytest.fixture
def website( ):
    ''' Provides website module. '''
    return cache_import_module( f"{ PACKAGE_NAME }.website" )


@pytest.fixture
def auxdata( application, distribution, state ):
    ''' Provides minimal Globals instance for testing in mem fs. '''

    class FakeDistributionInformation:
        def __init__( self, name: str, location: Path, editable: bool ):
            self._info = distribution.Information(
                name = name, location = location, editable = editable )

        def __getattr__( self, name: str ):
            return getattr( self._info, name )

        def provide_data_location( self, *appendages: str ) -> Path:
            base = Path( '/package/data' )
            if appendages: return base.joinpath( *appendages )
            return base

    distribution_obj = FakeDistributionInformation(
        name = PACKAGE_NAME, location = Path( '/package' ), editable = True )
    return state.Globals(
        application = application.Information(
            name = PACKAGE_NAME ),
        configuration = { },  # Empty configuration for tests
        directories = PlatformDirs(
            appname = PACKAGE_NAME, ensure_exists = False ),
        distribution = distribution_obj,
        exits = AsyncExitStack( ) )


@pytest.fixture
def auxdata_tmpdir( application, distribution, state, provide_tempdir ):
    ''' Provides minimal Globals instance for testing on real fs. '''

    class FakeDistributionInformation:
        def __init__( self, name: str, location: Path, editable: bool ):
            self._info = distribution.Information(
                name = name, location = location, editable = editable )

        def __getattr__( self, name: str ):
            return getattr( self._info, name )

        def provide_data_location( self, *appendages: str ) -> Path:
            base = Path( provide_tempdir ) / 'package/data'
            if appendages: return base.joinpath( *appendages )
            return base

    distribution_obj = FakeDistributionInformation(
        name = PACKAGE_NAME,
        location = Path( provide_tempdir ) / 'package',
        editable = True )
    return state.Globals(
        application = application.Information(
            name = PACKAGE_NAME ),
        configuration = { },  # Empty configuration for tests
        directories = PlatformDirs(
            appname = PACKAGE_NAME, ensure_exists = False ),
        distribution = distribution_obj,
        exits = AsyncExitStack( ) )


@pytest.fixture
def locations( auxdata, website, fs ):
    ''' Provides locations in fake filesystem. '''
    fs.create_dir( '/project/.auxiliary/artifacts' )
    fs.create_dir( '/project/.auxiliary/publications' )
    fs.create_dir( '/package/data/templates' )
    return website.Locations.from_project_anchor( auxdata, Path( '/project' ) )


@pytest.fixture
def locations_tmpdir( auxdata_tmpdir, website, provide_tempdir ):
    ''' Provides locations in real filesystem. '''
    ( provide_tempdir / 'project/.auxiliary/artifacts' ).mkdir(
        exist_ok = True, parents = True )
    ( provide_tempdir / 'project/.auxiliary/publications' ).mkdir(
        exist_ok = True, parents = True )
    ( provide_tempdir / 'package/data/templates' ).mkdir(
        exist_ok = True, parents = True )
    return website.Locations.from_project_anchor(
        auxdata_tmpdir, Path( provide_tempdir ) / 'project' )


class _FakeMember:
    ''' Stands in for tarfile members in archive rejection tests. '''

    def __init__(
        self, name, symlink = False, hardlink = False,
        special = False, regular = True
    ):
        self.name = name
        self._symlink = symlink
        self._hardlink = hardlink
        self._special = special
        self._regular = regular
    def issym( self ): return self._symlink
    def islnk( self ): return self._hardlink
    def ischr( self ): return self._special
    def isblk( self ): return False
    def isfifo( self ): return self._special
    def isdev( self ): return self._special
    def isfile( self ): return self._regular and not self._special
    def isdir( self ): return False


class _FakeArchive:
    ''' Stands in for tarfile archives in rejection tests. '''

    def __init__( self, members ): self._members = members
    def getmembers( self ): return self._members
    def extractall( self, path = None ): raise AssertionError( 'extract' )


def _assert_rejected( website, destination, member ):
    ''' Asserts archive with single member is rejected. '''
    archive = _FakeArchive( [ member ] )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website._safe_extractall( archive, destination )


def _write_inventory_case( base, entries ):
    ''' Writes legacy inventory TOML and returns its path. '''
    from pathlib import Path
    lines = [ ]
    for path, sha256, fragments, semantics in entries:
        lines.append( '[[entries]]' )
        lines.append( f'path = "{path}"' )
        if sha256: lines.append( f'sha256 = "{sha256}"' )
        if fragments:
            quoted = ', '.join( f'"{fragment}"' for fragment in fragments )
            lines.append( f'fragments = [{quoted}]' )
        lines.append( f'semantics = "{semantics}"' )
    location = Path( base ) / 'inventory.toml'
    location.write_text( '\n'.join( lines ) + '\n', newline = '' )
    return location


def _git_environment( ):
    ''' Returns environment scrubbed of ambient Git variables.

        Outer `git commit` hooks export `GIT_INDEX_FILE` and friends,
        which would otherwise hijack throwaway test repositories.
    '''
    import os
    return {
        key: value for key, value in os.environ.items( )
        if not key.startswith( 'GIT_' ) }


def _make_git_repo( provide_tempdir, name ):
    ''' Creates git repo with disabled signing, returning paths. '''
    import shutil
    import subprocess

    from pathlib import Path
    executable = shutil.which( 'git' )
    assert executable is not None
    project = Path( provide_tempdir ) / name
    project.mkdir( parents = True, exist_ok = True )
    def git( *args ):
        return subprocess.run(  # noqa: S603
            [ executable, *args ], cwd = project, check = True,
            capture_output = True, text = True,
            env = _git_environment( ) )
    git( 'init' )
    git( 'config', 'user.email', 'test@example.com' )
    git( 'config', 'user.name', 'Test' )
    git( 'config', 'commit.gpgsign', 'false' )
    git( 'config', 'tag.gpgsign', 'false' )
    return project, git



