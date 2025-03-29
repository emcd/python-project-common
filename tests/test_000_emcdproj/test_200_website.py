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

import ictruck
import pytest
import typing_extensions as typx

from pyfakefs.fake_filesystem import FakeFilesystem

from . import PACKAGE_NAME, cache_import_module, create_test_files


ictruck.register_module( PACKAGE_NAME )


@pytest.fixture
def website_module( ):
    ''' Provides cached website module. '''
    return cache_import_module( f'{ PACKAGE_NAME }.website' )


@pytest.fixture
def globals_instance( ) -> typx.Any:
    ''' Provides a minimal Globals instance for testing. '''
    base_module = cache_import_module( f'{ PACKAGE_NAME }.__' )
    distribution_module = cache_import_module( f'{ PACKAGE_NAME }.__.distribution' )
    application_module = cache_import_module( f'{ PACKAGE_NAME }.__.application' )

    # Define a custom provide_data_location function for testing
    def provide_data_location( self, *appendages: str ) -> Path:
        base = Path( '/fake' )
        if appendages: return base.joinpath( *appendages )
        return base

    # Create a custom DistributionInformation with the overridden method
    class TestDistributionInformation( distribution_module.Information ):
        def provide_data_location( self, *appendages: str ) -> Path:
            return provide_data_location( self, *appendages )

    distribution = TestDistributionInformation(
        name = PACKAGE_NAME,
        location = Path( '/fake/dist' ),
        editable = True,
    )
    return base_module.Globals(
        application = application_module.Information( name = PACKAGE_NAME ),
        directories = base_module.PlatformDirs( appname = PACKAGE_NAME, ensure_exists = False ),
        distribution = distribution,
        exits = AsyncExitStack( ),
    )


def test_000_locations_attributes( globals_instance, fs: FakeFilesystem, website_module ):
    ''' Locations class has expected attributes with injected anchor. '''
    fs.create_dir( '/project/.auxiliary/artifacts' )
    fs.create_dir( '/project/.auxiliary/publications' )
    fs.create_dir( '/fake/templates' )
    locations = website_module.Locations.from_project_anchor(
        globals_instance, Path( '/project' ) )
    assert locations.project == Path( '/project' )
    assert locations.auxiliary == Path( '/project/.auxiliary' )
    assert locations.publications == Path( '/project/.auxiliary/publications' )
    assert locations.archive == Path( '/project/.auxiliary/publications/website.tar.xz' )
    assert locations.artifacts == Path( '/project/.auxiliary/artifacts' )
    assert locations.website == Path( '/project/.auxiliary/artifacts/website' )
    assert locations.coverage == Path( '/project/.auxiliary/artifacts/website/coverage.svg' )
    assert locations.index == Path( '/project/.auxiliary/artifacts/website/index.html' )
    assert locations.versions == Path( '/project/.auxiliary/artifacts/website/versions.json' )
    assert locations.templates == Path( '/fake/templates' )


def test_010_extract_coverage( fs: FakeFilesystem, website_module ):
    ''' Coverage extraction works with valid XML. '''
    xml_content = '<?xml version="1.0" ?><coverage line-rate="0.85"></coverage>'
    locations = website_module.Locations(
        project = Path( '/project' ),
        auxiliary = Path( '/project/.auxiliary' ),
        publications = Path( '/project/.auxiliary/publications' ),
        archive = Path( '/project/.auxiliary/publications/website.tar.xz' ),
        artifacts = Path( '/project/.auxiliary/artifacts' ),
        website = Path( '/project/.auxiliary/artifacts/website' ),
        coverage = Path( '/project/.auxiliary/artifacts/website/coverage.svg' ),
        index = Path( '/project/.auxiliary/artifacts/website/index.html' ),
        versions = Path( '/project/.auxiliary/artifacts/website/versions.json' ),
        templates = Path( '/fake/templates' ),
    )
    fs.create_file( locations.artifacts / 'coverage-pytest/coverage.xml', contents = xml_content )
    assert website_module._extract_coverage( locations ) == 85


def test_020_extract_coverage_missing_file( fs: FakeFilesystem, website_module ):
    ''' Coverage extraction raises FileAwol for missing XML. '''
    exceptions = cache_import_module( f'{ PACKAGE_NAME }.exceptions' )
    locations = website_module.Locations(
        project = Path( '/project' ),
        auxiliary = Path( '/project/.auxiliary' ),
        publications = Path( '/project/.auxiliary/publications' ),
        archive = Path( '/project/.auxiliary/publications/website.tar.xz' ),
        artifacts = Path( '/project/.auxiliary/artifacts' ),
        website = Path( '/project/.auxiliary/artifacts/website' ),
        coverage = Path( '/project/.auxiliary/artifacts/website/coverage.svg' ),
        index = Path( '/project/.auxiliary/artifacts/website/index.html' ),
        versions = Path( '/project/.auxiliary/artifacts/website/versions.json' ),
        templates = Path( '/fake/templates' ),
    )
    with pytest.raises( exceptions.FileAwol ): website_module._extract_coverage( locations )


def test_030_update_available_species( fs: FakeFilesystem, website_module ):
    ''' Species directories are copied correctly. '''
    locations = website_module.Locations(
        project = Path( '/project' ),
        auxiliary = Path( '/project/.auxiliary' ),
        publications = Path( '/project/.auxiliary/publications' ),
        archive = Path( '/project/.auxiliary/publications/website.tar.xz' ),
        artifacts = Path( '/project/.auxiliary/artifacts' ),
        website = Path( '/project/.auxiliary/artifacts/website' ),
        coverage = Path( '/project/.auxiliary/artifacts/website/coverage.svg' ),
        index = Path( '/project/.auxiliary/artifacts/website/index.html' ),
        versions = Path( '/project/.auxiliary/artifacts/website/versions.json' ),
        templates = Path( '/fake/templates' ),
    )
    fs.create_dir( locations.artifacts / 'coverage-pytest' )
    fs.create_file( locations.artifacts / 'coverage-pytest/test.txt', contents = 'test' )
    species = website_module._update_available_species( locations, 'v1.0' )
    assert 'coverage-pytest' in species
    assert fs.exists( locations.website / 'v1.0/coverage-pytest/test.txt' )


def test_040_update_coverage_badge( fs: FakeFilesystem, website_module ):
    ''' Coverage badge is updated with injected jinja context. '''
    locations = website_module.Locations(
        project = Path( '/project' ),
        auxiliary = Path( '/project/.auxiliary' ),
        publications = Path( '/project/.auxiliary/publications' ),
        archive = Path( '/project/.auxiliary/publications/website.tar.xz' ),
        artifacts = Path( '/project/.auxiliary/artifacts' ),
        website = Path( '/project/.auxiliary/artifacts/website' ),
        coverage = Path( '/project/.auxiliary/artifacts/website/coverage.svg' ),
        index = Path( '/project/.auxiliary/artifacts/website/index.html' ),
        versions = Path( '/project/.auxiliary/artifacts/website/versions.json' ),
        templates = Path( '/fake/templates' ),
    )
    fs.create_dir( locations.artifacts / 'coverage-pytest' )
    fs.create_file(
        locations.artifacts / 'coverage-pytest/coverage.xml',
        contents = '<?xml version="1.0" ?><coverage line-rate="0.9"></coverage>',
    )
    fs.create_dir( locations.website )
    fs.create_file( locations.templates / 'coverage.svg.jinja', contents = '{{ color }}' )
    import jinja2
    j2context = jinja2.Environment(
        loader = jinja2.FileSystemLoader( locations.templates ),
        autoescape = True )
    website_module._update_coverage_badge( locations, j2context )
    assert fs.exists( locations.coverage )
    assert locations.coverage.read_text( ) == 'green'


def test_050_update_index_html( fs: FakeFilesystem, website_module ):
    ''' Index HTML is updated with injected data and jinja context. '''
    locations = website_module.Locations(
        project = Path( '/project' ),
        auxiliary = Path( '/project/.auxiliary' ),
        publications = Path( '/project/.auxiliary/publications' ),
        archive = Path( '/project/.auxiliary/publications/website.tar.xz' ),
        artifacts = Path( '/project/.auxiliary/artifacts' ),
        website = Path( '/project/.auxiliary/artifacts/website' ),
        coverage = Path( '/project/.auxiliary/artifacts/website/coverage.svg' ),
        index = Path( '/project/.auxiliary/artifacts/website/index.html' ),
        versions = Path( '/project/.auxiliary/artifacts/website/versions.json' ),
        templates = Path( '/fake/templates' ),
    )
    fs.create_dir( locations.website )
    fs.create_file(
        locations.templates / 'website.html.jinja',
        contents = '{{ latest_version }}' )
    import jinja2
    j2context = jinja2.Environment(
        loader = jinja2.FileSystemLoader( locations.templates ),
        autoescape = True )
    data = { 'latest_version': 'v1.0' }
    website_module._update_index_html( locations, j2context, data )
    assert fs.exists( locations.index )
    assert locations.index.read_text( ) == 'v1.0'


def test_060_update_versions_json( fs: FakeFilesystem, website_module ):
    ''' Versions JSON is updated correctly. '''
    locations = website_module.Locations(
        project = Path( '/project' ),
        auxiliary = Path( '/project/.auxiliary' ),
        publications = Path( '/project/.auxiliary/publications' ),
        archive = Path( '/project/.auxiliary/publications/website.tar.xz' ),
        artifacts = Path( '/project/.auxiliary/artifacts' ),
        website = Path( '/project/.auxiliary/artifacts/website' ),
        coverage = Path( '/project/.auxiliary/artifacts/website/coverage.svg' ),
        index = Path( '/project/.auxiliary/artifacts/website/index.html' ),
        versions = Path( '/project/.auxiliary/artifacts/website/versions.json' ),
        templates = Path( '/fake/templates' ),
    )
    fs.create_dir( locations.website )
    species = ( 'coverage-pytest', )
    data = website_module._update_versions_json( locations, 'v1.0', species )
    assert fs.exists( locations.versions )
    assert data[ 'latest_version' ] == 'v1.0'
    assert data[ 'versions' ][ 'v1.0' ] == species


def test_100_integration_update( provide_tempdir: Path, website_module ):
    ''' Integration test for update with real filesystem, respecting immutability. '''
    base_module = cache_import_module( f'{ PACKAGE_NAME }.__' )
    distribution_module = cache_import_module( f'{ PACKAGE_NAME }.__.distribution' )
    application_module = cache_import_module( f'{ PACKAGE_NAME }.__.application' )

    def provide_data_location( self, *appendages: str ) -> Path:
        base = provide_tempdir / 'data'
        if appendages: return base.joinpath( *appendages )
        return base

    class TestDistributionInformation( distribution_module.Information ):
        def provide_data_location( self, *appendages: str ) -> Path:
            return provide_data_location( self, *appendages )

    distribution = TestDistributionInformation(
        name = PACKAGE_NAME,
        location = provide_tempdir,  # Set at construction
        editable = True,
    )
    globals_instance = base_module.Globals(
        application = application_module.Information( name = PACKAGE_NAME ),
        directories = base_module.PlatformDirs( appname = PACKAGE_NAME, ensure_exists = False ),
        distribution = distribution,
        exits = AsyncExitStack( ),
    )
    coverage_template = '''
<svg width="{{ total_width }}" height="20">
    <rect width="{{ label_width }}" height="20" fill="grey"/>
    <rect x="{{ label_width }}" width="{{ value_width }}" height="20" fill="{{ color }}"/>
    <text x="5" y="15" fill="white">{{ label_text }}</text>
    <text x="{{ label_width + 5 }}" y="15" fill="white">{{ value_text }}</text>
</svg>
    '''.strip( )
    test_files = {
        '.auxiliary/artifacts/coverage-pytest/coverage.xml':
            '<?xml version="1.0" ?><coverage line-rate="0.75"></coverage>',
        'data/templates/coverage.svg.jinja': coverage_template,
        'data/templates/website.html.jinja': '{{ latest_version }}',
    }
    with create_test_files( provide_tempdir, test_files ):
        website_dir = provide_tempdir / '.auxiliary/artifacts/website'
        website_dir.mkdir( parents = True, exist_ok = True )
        website_module.update( globals_instance, 'v1.0' )
        assert ( provide_tempdir / '.auxiliary/artifacts/website/coverage.svg' ).exists( )
        assert ( provide_tempdir / '.auxiliary/artifacts/website/index.html' ).read_text( ) == 'v1.0'
        assert ( provide_tempdir / '.auxiliary/artifacts/website/versions.json' ).exists( )
        assert ( provide_tempdir / '.auxiliary/artifacts/website/.nojekyll' ).exists( )
        assert ( provide_tempdir / '.auxiliary/publications/website.tar.xz' ).exists( )
