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


''' Update website for publication. '''


from argparse import ArgumentParser
from contextlib import contextmanager
from json import dump as json_dump, load as json_load
from math import floor
from pathlib import Path
from shutil import copytree, rmtree
from tarfile import open as tarfile_open
from xml.etree import ElementTree  # nosec
from typing import Iterator, NamedTuple

from jinja2 import Environment, FileSystemLoader


class Paths( NamedTuple ):
    ''' Paths used in website generation. '''
    project: Path
    auxiliary: Path
    publications: Path
    archive: Path
    artifacts: Path
    website: Path
    coverage: Path
    index: Path
    versions: Path
    templates: Path


def discover_paths( ) -> Paths:
    ''' Discovers paths needed for website generation.

        Returns paths to project directories and files used in the website
        generation process, including locations for artifacts, templates,
        and publication outputs.
    '''
    project = Path( ).resolve( )  # TODO: Discover.
    auxiliary = project / '.auxiliary'
    publications = auxiliary / 'publications'
    return Paths(
        project = project,
        auxiliary = auxiliary,
        publications = publications,
        archive = publications / 'website.tar.xz',
        artifacts = auxiliary / 'artifacts',
        website = auxiliary / 'artifacts/website',
        coverage = auxiliary / 'artifacts/website/coverage.svg',
        index = auxiliary / 'artifacts/website/index.html',
        versions = auxiliary / 'artifacts/website/versions.json',
        templates = Path( __file__ ).parent.parent / 'data/templates',
    )


def extract_coverage( paths: Paths ) -> int:
    ''' Extracts coverage percentage from coverage report.

        Reads the coverage XML report and calculates the overall line coverage
        percentage, rounded down to the nearest integer.
    '''
    path = paths.artifacts / 'coverage-pytest/coverage.xml'
    # nosemgrep
    root = ElementTree.parse( path ).getroot( )  # nosec
    coverage = float( root.get( 'line-rate' ) )
    return floor( coverage * 100 )


@contextmanager
def springy_chdir( new_path: Path ) -> Iterator[ Path ]:
    ''' Temporarily changes working directory. '''
    from os import chdir, getcwd
    old_path = getcwd( )
    chdir( new_path )
    try: yield new_path
    finally: chdir( old_path )


def update_coverage_badge( paths: Paths, env: Environment ) -> None:
    ''' Updates coverage badge SVG.

        Generates a color-coded coverage badge based on the current coverage
        percentage. Colors indicate coverage quality:
        - red: < 50%
        - yellow: 50-79%
        - green: >= 80%
    '''
    coverage = extract_coverage( paths )
    color = 'red' if coverage < 50 else 'yellow' if coverage < 80 else 'green'
    label_text = 'coverage'
    value_text = f"{coverage}%"
    label_width = len( label_text ) * 6 + 10
    value_width = len( value_text ) * 6 + 15
    total_width = label_width + value_width

    template = env.get_template( 'coverage.svg.jinja' )
    with paths.coverage.open( 'w' ) as file:
        file.write( template.render(
            color = color,
            total_width = total_width,
            label_text = label_text,
            value_text = value_text,
            label_width = label_width,
            value_width = value_width,
        ) )


def update_index_html( paths: Paths, env: Environment, data: dict ) -> None:
    ''' Updates index.html with version information.

        Generates the main index page showing all available versions and their
        associated documentation and coverage reports.
    '''
    template = env.get_template( 'website.html.jinja' )
    with paths.index.open( 'w' ) as file:
        file.write( template.render( **data ) )


def update_versions_json( paths: Paths, version: str, species: list[ str ] ) -> dict:
    ''' Updates versions.json with new version information.

        Maintains a JSON file tracking all versions and their available
        documentation types. Versions are sorted in descending order, with
        the latest version marked separately.
    '''
    from packaging.version import Version
    if not paths.versions.is_file( ):
        data = { 'versions': { } }
        with paths.versions.open( 'w' ) as file:
            json_dump( data, file, indent = 4 )

    with paths.versions.open( 'r+' ) as file:
        data = json_load( file )
        versions = data[ 'versions' ]
        versions[ version ] = species
        versions = dict( sorted(
            versions.items( ),
            key = lambda entry: Version( entry[ 0 ] ),
            reverse = True ) )
        data[ 'latest_version' ] = next( iter( versions ) )
        data[ 'versions' ] = versions
        file.seek( 0 )
        json_dump( data, file, indent = 4 )
        file.truncate( )

    return data


def main( ) -> None:
    ''' Main entry point.

        Processes command line arguments and orchestrates the website update
        process, including copying documentation, updating version information,
        and generating coverage badges.
    '''
    parser = ArgumentParser( description = 'Update project website.' )
    parser.add_argument( 'version', help = 'Version being published' )
    args = parser.parse_args( )

    paths = discover_paths( )
    paths.publications.mkdir( exist_ok = True, parents = True )
    if paths.website.is_dir( ):
        rmtree( paths.website )
    paths.website.mkdir( exist_ok = True, parents = True )

    if paths.archive.is_file( ):
        with tarfile_open( paths.archive, 'r:xz' ) as archive:
            archive.extractall( path = paths.website )

    available_species = [ ]
    # Create/update destination if origin exists.
    for species in ( 'coverage-pytest', 'sphinx-html' ):
        origin_path = paths.artifacts / species
        if not origin_path.is_dir( ):
            continue
        destination_path = paths.website / args.version / species
        if destination_path.is_dir( ):
            rmtree( destination_path )
        copytree( origin_path, destination_path )
        available_species.append( species )

    env = Environment(
        loader = FileSystemLoader( paths.templates ),
        autoescape = True,
    )

    index_data = update_versions_json( paths, args.version, available_species )
    update_index_html( paths, env, index_data )

    if ( paths.artifacts / 'coverage-pytest' ).is_dir( ):
        update_coverage_badge( paths, env )

    ( paths.website / '.nojekyll' ).touch( )

    with springy_chdir( paths.website ):
        with tarfile_open( paths.archive, 'w:xz' ) as archive:
            archive.add( '.' )


if __name__ == '__main__': main( )
