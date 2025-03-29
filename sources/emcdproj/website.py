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


''' Static website maintenance utilities for projects. '''
# TODO: Support separate section for current documentation: stable, latest.
# TODO? Separate coverage SVG files for each release.


from __future__ import annotations

import jinja2 as _jinja2

from . import __
from . import exceptions as _exceptions
from . import interfaces as _interfaces


class CommandDispatcher(
    _interfaces.CliCommand,
    decorators = ( __.standard_tyro_class, ),
):
    ''' Dispatches commands for static website maintenance. '''

    command: __.typx.Union[
        __.typx.Annotated[
            SurveyCommand,
            __.tyro.conf.subcommand( 'survey', prefix_name = False ),
        ],
        __.typx.Annotated[
            UpdateCommand,
            __.tyro.conf.subcommand( 'update', prefix_name = False ),
        ],
    ]

    async def __call__( self, auxdata: __.Globals ) -> None:
        ictr( 1 )( self.command )
        await self.command( auxdata = auxdata )


class SurveyCommand(
    _interfaces.CliCommand,
    decorators = ( __.standard_tyro_class, ),
):
    ''' Surveys release versions published in static website. '''

    async def __call__( self, auxdata: __.Globals ) -> None:
        # TODO: Implement.
        pass


class UpdateCommand(
    _interfaces.CliCommand,
    decorators = ( __.standard_tyro_class, ),
):
    ''' Updates static website for particular release version. '''

    version: __.typx.Annotated[
        str,
        __.typx.Doc( ''' Release version to update. ''' ),
        __.tyro.conf.Positional,
    ]

    async def __call__( self, auxdata: __.Globals ) -> None:
        update( auxdata, self.version )


class Locations( metaclass = __.ImmutableDataclass ):
    ''' Locations associated with website maintenance. '''

    project: __.Path
    auxiliary: __.Path
    publications: __.Path
    archive: __.Path
    artifacts: __.Path
    website: __.Path
    coverage: __.Path
    index: __.Path
    versions: __.Path
    templates: __.Path

    @classmethod
    def from_project_anchor(
        selfclass,
        auxdata: __.Globals,
        anchor: __.Absential[ __.Path ] = __.absent,
    ) -> __.typx.Self:
        ''' Produces locations from project anchor, if provided.

            If project anchor is not given, then attempt to discover it.
        '''
        if __.is_absent( anchor ):
            # TODO: Discover missing anchor via directory traversal,
            #       seeking VCS markers.
            project = __.Path( ).resolve( strict = True )
        else: project = anchor.resolve( strict = True )
        auxiliary = project / '.auxiliary'
        publications = auxiliary / 'publications'
        templates = auxdata.distribution.provide_data_location( 'templates' )
        return selfclass(
            project = project,
            auxiliary = auxiliary,
            publications = publications,
            archive = publications / 'website.tar.xz',
            artifacts = auxiliary / 'artifacts',
            website = auxiliary / 'artifacts/website',
            coverage = auxiliary / 'artifacts/website/coverage.svg',
            index = auxiliary / 'artifacts/website/index.html',
            versions = auxiliary / 'artifacts/website/versions.json',
            templates = templates )



def update(
    auxdata: __.Globals,
    version: str, *,
    project_anchor: __.Absential[ __.Path ] = __.absent
) -> None:
    ''' Updates project website with latest documentation and coverage.

        Processes the specified version, copies documentation artifacts,
        updates version information, and generates coverage badges.
    '''
    ictr( 2 )( version )
    # TODO: Validate version string format.
    from tarfile import open as tarfile_open
    locations = Locations.from_project_anchor( auxdata, project_anchor )
    locations.publications.mkdir( exist_ok = True, parents = True )
    if locations.website.is_dir( ): __.shutil.rmtree( locations.website )
    locations.website.mkdir( exist_ok = True, parents = True )
    if locations.archive.is_file( ):
        with tarfile_open( locations.archive, 'r:xz' ) as archive:
            archive.extractall( path = locations.website )
    available_species = _update_available_species( locations, version )
    j2context = _jinja2.Environment(
        loader = _jinja2.FileSystemLoader( locations.templates ),
        autoescape = True )
    index_data = _update_versions_json( locations, version, available_species )
    _update_index_html( locations, j2context, index_data )
    if ( locations.artifacts / 'coverage-pytest' ).is_dir( ):
        _update_coverage_badge( locations, j2context )
    ( locations.website / '.nojekyll' ).touch( )
    from .filesystem import chdir
    with chdir( locations.website ):
        with tarfile_open( locations.archive, 'w:xz' ) as archive:
            archive.add( '.' )


def _extract_coverage( locations: Locations ) -> int:
    ''' Extracts coverage percentage from coverage report.

        Reads the coverage XML report and calculates the overall line coverage
        percentage, rounded down to the nearest integer.
    '''
    location = locations.artifacts / 'coverage-pytest/coverage.xml'
    if not location.exists( ): raise _exceptions.FileAwol( location )
    from defusedxml import ElementTree
    root = ElementTree.parse( location ).getroot( ) # pyright: ignore
    if root is None:
        raise _exceptions.FileEmpty( location ) # pragma: no cover
    line_rate = root.get( 'line-rate' )
    if not line_rate:
        raise _exceptions.FileDataAwol(
            location, 'line-rate' ) # pragma: no cover
    return __.math.floor( float( line_rate ) * 100 )


def _update_available_species(
    locations: Locations, version: str
) -> tuple[ str, ... ]:
    available_species: list[ str ] = [ ]
    for species in ( 'coverage-pytest', 'sphinx-html' ):
        origin = locations.artifacts / species
        if not origin.is_dir( ): continue
        destination = locations.website / version / species
        if destination.is_dir( ): __.shutil.rmtree( destination )
        __.shutil.copytree( origin, destination )
        available_species.append( species )
    return tuple( available_species )


def _update_coverage_badge( # pylint: disable=too-many-locals
    locations: Locations, j2context: _jinja2.Environment
) -> None:
    ''' Updates coverage badge SVG.

        Generates a color-coded coverage badge based on the current coverage
        percentage. Colors indicate coverage quality:
        - red: < 50%
        - yellow: 50-79%
        - green: >= 80%
    '''
    coverage = _extract_coverage( locations )
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
    template = j2context.get_template( 'coverage.svg.jinja' )
    # TODO: Add error handling for template rendering failures.
    with locations.coverage.open( 'w' ) as file:
        file.write( template.render(
            color = color,
            total_width = total_width,
            label_text = label_text,
            value_text = value_text,
            label_width = label_width,
            value_width = value_width ) )


def _update_index_html(
    locations: Locations,
    j2context: _jinja2.Environment,
    data: dict[ __.typx.Any, __.typx.Any ],
) -> None:
    ''' Updates index.html with version information.

        Generates the main index page showing all available versions and their
        associated documentation and coverage reports.
    '''
    template = j2context.get_template( 'website.html.jinja' )
    # TODO: Add error handling for template rendering failures.
    with locations.index.open( 'w' ) as file:
        file.write( template.render( **data ) )


def _update_versions_json(
    locations: Locations,
    version: str,
    species: tuple[ str, ... ],
) -> dict[ __.typx.Any, __.typx.Any ]:
    ''' Updates versions.json with new version information.

        Maintains a JSON file tracking all versions and their available
        documentation types. Versions are sorted in descending order, with
        the latest version marked separately.
    '''
    # TODO: Add validation of version string format.
    # TODO: Consider file locking for concurrent update protection.
    from packaging.version import Version
    if not locations.versions.is_file( ):
        data: dict[ __.typx.Any, __.typx.Any ] = { 'versions': { } }
        with locations.versions.open( 'w' ) as file:
            __.json.dump( data, file, indent = 4 )
    with locations.versions.open( 'r+' ) as file:
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
