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


from shutil import rmtree

import ictruck
import pytest

from .__ import PACKAGE_NAME, create_test_files


ictruck.register_module( PACKAGE_NAME )


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
