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


''' Tests for website maintenance utilities. '''


from contextlib import AsyncExitStack
from pathlib import Path
from shutil import rmtree

import ictruck
import pytest

from platformdirs import PlatformDirs

from . import PACKAGE_NAME, cache_import_module, create_test_files


ictruck.register_module( PACKAGE_NAME )


@pytest.fixture
def application( ):
    ''' Provides internal application module. '''
    return cache_import_module( f"{ PACKAGE_NAME }.__.application" )


@pytest.fixture
def distribution( ):
    ''' Provides internal package distribution module. '''
    return cache_import_module( f"{ PACKAGE_NAME }.__.distribution" )


@pytest.fixture
def imports( ):
    ''' Provides internal imports package. '''
    return cache_import_module( f"{ PACKAGE_NAME }.__.imports" )


@pytest.fixture
def state( ):
    ''' Provides internal state package. '''
    return cache_import_module( f"{ PACKAGE_NAME }.__.state" )


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


# def test_000_locations_attributes( locations ):
#     ''' Locations class has expected attributes with injected anchor. '''
#     pathetic = Pathetic( )
#     assert pathetic.compare( locations.project, '/project' )
#     assert pathetic.compare( locations.auxiliary, '/project/.auxiliary' )
#     assert pathetic.compare(
#         locations.publications, '/project/.auxiliary/publications' )
#     assert pathetic.compare(
#         locations.archive,
#         '/project/.auxiliary/publications/website.tar.xz' )
#     assert pathetic.compare(
#         locations.artifacts, '/project/.auxiliary/artifacts' )
#     assert pathetic.compare(
#         locations.website, '/project/.auxiliary/artifacts/website' )
#     assert pathetic.compare(
#         locations.coverage,
#         '/project/.auxiliary/artifacts/website/coverage.svg' )
#     assert pathetic.compare(
#         locations.index,
#         '/project/.auxiliary/artifacts/website/index.html' )
#     assert pathetic.compare(
#         locations.versions,
#         '/project/.auxiliary/artifacts/website/versions.json' )
#     assert pathetic.compare( locations.templates, '/package/data/templates' )


def test_010_extract_coverage( locations, website, fs ):
    ''' Coverage extraction works with valid XML. '''
    xml_content = (
        '<?xml version="1.0" ?><coverage line-rate="0.85"></coverage>' )
    fs.create_file(
        locations.artifacts / 'coverage-pytest/coverage.xml',
        contents = xml_content )
    assert website._extract_coverage( locations ) == 85


def test_020_extract_coverage_missing_file( locations, website, exceptions ):
    ''' Coverage extraction raises FileAwol for missing XML. '''
    with pytest.raises( exceptions.FileAwol ):
        website._extract_coverage( locations )


def test_030_update_available_species( locations, website, fs ):
    ''' Species directories are copied correctly. '''
    fs.create_dir(
        locations.artifacts / 'coverage-pytest' )
    fs.create_file(
        locations.artifacts / 'coverage-pytest/test.txt', contents = 'test' )
    species = website._update_available_species( locations, 'v1.0' )
    assert 'coverage-pytest' in species
    assert ( locations.website / 'v1.0/coverage-pytest/test.txt' ).exists( )


def test_040_update_coverage_badge( locations, website, fs ):
    ''' Coverage badge is updated with injected jinja context. '''
    fs.create_dir( locations.artifacts / 'coverage-pytest' )
    fs.create_file(
        locations.artifacts / 'coverage-pytest/coverage.xml',
        contents = (
            '<?xml version="1.0" ?><coverage line-rate="0.9"></coverage>' ) )
    fs.create_dir( locations.website )
    fs.create_file(
        locations.templates / 'coverage.svg.jinja', contents = '{{ color }}' )
    import jinja2
    j2context = jinja2.Environment(
        loader = jinja2.FileSystemLoader( locations.templates ),
        autoescape = True )
    website._update_coverage_badge( locations, j2context )
    assert locations.coverage.exists( )
    assert locations.coverage.read_text( ) == 'green'


def test_050_update_index_html( locations, website, fs ):
    ''' Index HTML is updated with injected data and jinja context. '''
    fs.create_dir( locations.website )
    fs.create_file(
        locations.templates / 'website.html.jinja',
        contents = '{{ latest_version }}' )
    import jinja2
    j2context = jinja2.Environment(
        loader = jinja2.FileSystemLoader( locations.templates ),
        autoescape = True )
    data = { 'latest_version': 'v1.0' }
    website._update_index_html( locations, j2context, data )
    assert locations.index.exists( )
    assert locations.index.read_text( ) == 'v1.0'


def test_060_update_versions_json( locations, website, fs ):
    ''' Versions JSON is updated correctly. '''
    fs.create_dir( locations.website )
    species = ( 'coverage-pytest', )
    data = website._update_versions_json( locations, 'v1.0', species )
    assert locations.versions.exists( )
    assert data[ 'latest_version' ] == 'v1.0'
    assert data[ 'versions' ][ 'v1.0' ] == species


def test_100_integration_update(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Update with real filesystem. '''
    coverage_template = '''
<svg width="{{ total_width }}" height="20">
    <rect width="{{ label_width }}" height="20" fill="grey"/>
    <rect x="{{ label_width }}"
          width="{{ value_width }}" height="20" fill="{{ color }}"/>
    <text x="5" y="15" fill="white">{{ label_text }}</text>
    <text x="{{ label_width + 5 }}" y="15" fill="white">{{ value_text }}</text>
</svg>
    '''.strip( )
    test_files = {
        'project/.auxiliary/artifacts/coverage-pytest/coverage.xml':
            '<?xml version="1.0" ?><coverage line-rate="0.75"></coverage>',
        'package/data/templates/coverage.svg.jinja': coverage_template,
        'package/data/templates/website.html.jinja': '{{ latest_version }}',
    }
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project )
        assert locations_tmpdir.coverage.exists( )
        assert locations_tmpdir.index.read_text( ) == 'v1.0'
        assert ( locations_tmpdir.website / '.nojekyll' ).exists( )
        assert locations_tmpdir.archive.exists( )
        # Second pass to cover some branches not hit on first pass.
        rmtree( locations_tmpdir.artifacts / 'coverage-pytest' )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project )
