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


''' Website update utilities. '''
# TODO: Fix Pyright suppressions.


from __future__ import annotations

import jinja2 as _jinja2

from . import __
from . import interfaces as _interfaces


class Command(
    _interfaces.CliCommand,
    decorators = ( __.standard_tyro_class, ),
):
    ''' Manages static website for project. '''

    async def __call__( self )-> None:
    # async def __call__( self, auxdata: __.Globals ) -> None:
        ''' Dispatches subcommand to manage static website. '''
        # TODO: Pass global state.
        # TODO: Implement.


class Paths( __.typx.NamedTuple ):
    ''' Paths used in website generation. '''
    project: __.Path
    auxiliary: __.Path
    publications: __.Path
    archive: __.Path
    artifacts: __.Path
    website: __.Path
    coverage: __.Path
    index: __.Path # pyright: ignore
    versions: __.Path
    templates: __.Path


def discover_paths( ) -> Paths:
    ''' Discovers paths needed for website generation.

        Returns paths to project directories and files used in the website
        generation process, including locations for artifacts, templates,
        and publication outputs.
    '''
    # TODO: Add error handling for scenarios where expected directories
    #       cannot be accessed due to permission issues.
    project = __.Path( ).resolve( )  # TODO: Discover.
    auxiliary = project / '.auxiliary'
    publications = auxiliary / 'publications'
    # Updated template path to use package-relative location
    templates = __.Path( __file__ ).parent / 'data/templates'
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
        templates = templates,
    )


def extract_coverage( paths: Paths ) -> int:
    ''' Extracts coverage percentage from coverage report.

        Reads the coverage XML report and calculates the overall line coverage
        percentage, rounded down to the nearest integer.
    '''
    # TODO: Add validation that the XML file exists and has expected format.
    path = paths.artifacts / 'coverage-pytest/coverage.xml'
    from xml.etree import ElementTree  # nosec
    # nosemgrep
    root = ElementTree.parse( path ).getroot( )  # nosec
    coverage = float( root.get( 'line-rate' ) ) # pyright: ignore
    return __.math.floor( coverage * 100 )


def update_coverage_badge( # pylint: disable=too-many-locals
    paths: Paths, env: _jinja2.Environment
) -> None:
    ''' Updates coverage badge SVG.

        Generates a color-coded coverage badge based on the current coverage
        percentage. Colors indicate coverage quality:
        - red: < 50%
        - yellow: 50-79%
        - green: >= 80%
    '''
    # TODO: Add error handling for template rendering failures.
    coverage = extract_coverage( paths )
    # pylint: disable=magic-value-comparison
    color = (
        'red' if coverage < 50 else (
            'yellow' if coverage < 80 else 'green' ) )
    # pylint: enable=magic-value-comparison
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


def update_index_html(
    paths: Paths,
    env: _jinja2.Environment,
    data: dict[ __.typx.Any, __.typx.Any ],
) -> None:
    ''' Updates index.html with version information.

        Generates the main index page showing all available versions and their
        associated documentation and coverage reports.
    '''
    # TODO: Add validation that the template exists before attempting to use it.
    template = env.get_template( 'website.html.jinja' )
    with paths.index.open( 'w' ) as file:
        file.write( template.render( **data ) )


def update_versions_json(
    paths: Paths,
    version: __.typx.Annotated[
        str, __.typx.Doc( "Version string being published" ) ],
    species: __.typx.Annotated[
        list[ str ],
        __.typx.Doc( "List of artifact types available for this version" ),
    ]
) -> dict[ __.typx.Any, __.typx.Any ]:
    ''' Updates versions.json with new version information.

        Maintains a JSON file tracking all versions and their available
        documentation types. Versions are sorted in descending order, with
        the latest version marked separately.
    '''
    # TODO: Add validation of version string format.
    # TODO: Consider file locking for concurrent update protection.

    # Import at function level to maintain clean module namespace
    from packaging.version import Version

    if not paths.versions.is_file( ):
        data: dict[ __.typx.Any, __.typx.Any ] = { 'versions': { } }
        with paths.versions.open( 'w' ) as file:
            __.json.dump( data, file, indent = 4 )

    with paths.versions.open( 'r+' ) as file:
        data = __.json.load( file )
        versions = data[ 'versions' ]
        versions[ version ] = species
        versions = dict( sorted(
            versions.items( ),
            key = lambda entry: Version( entry[ 0 ] ),
            reverse = True ) )
        data[ 'latest_version' ] = next( iter( versions ) )
        data[ 'versions' ] = versions
        file.seek( 0 )
        __.json.dump( data, file, indent = 4 )
        file.truncate( )

    return data


def update_website( # pylint: disable=too-many-locals
    version: __.typx.Annotated[
        str, __.typx.Doc( "Version string being published" ) ]
) -> None:
    ''' Updates the project website with the latest documentation and coverage.

        Processes the specified version, copies documentation artifacts,
        updates version information, and generates coverage badges.
    '''
    # TODO: Add checks for empty artifact directories.
    # TODO: Validate version string format.

    paths = discover_paths( )
    paths.publications.mkdir( exist_ok = True, parents = True )
    if paths.website.is_dir( ):
        __.shutil.rmtree( paths.website )
    paths.website.mkdir( exist_ok = True, parents = True )

    if paths.archive.is_file( ):
        from tarfile import open as tarfile_open
        with tarfile_open( paths.archive, 'r:xz' ) as archive:
            archive.extractall( path = paths.website )

    available_species: list[ str ] = [ ]
    # Create/update destination if origin exists.
    for species in ( 'coverage-pytest', 'sphinx-html' ):
        origin_path = paths.artifacts / species
        if not origin_path.is_dir( ):
            continue
        destination_path = paths.website / version / species
        if destination_path.is_dir( ):
            __.shutil.rmtree( destination_path )
        __.shutil.copytree( origin_path, destination_path )
        available_species.append( species )

    env = _jinja2.Environment(
        loader = _jinja2.FileSystemLoader( paths.templates ),
        autoescape = True,
    )

    index_data = update_versions_json( paths, version, available_species )
    update_index_html( paths, env, index_data )

    if ( paths.artifacts / 'coverage-pytest' ).is_dir( ):
        update_coverage_badge( paths, env )

    ( paths.website / '.nojekyll' ).touch( )

    from .filesystem import chdir
    with chdir( paths.website ):
        from tarfile import open as tarfile_open
        with tarfile_open( paths.archive, 'w:xz' ) as archive:
            archive.add( '.' )
