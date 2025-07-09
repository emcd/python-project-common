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


import jinja2 as _jinja2

from . import __
from . import exceptions as _exceptions
from . import interfaces as _interfaces


class SurveyCommand(
    _interfaces.CliCommand, decorators = ( __.standard_tyro_class, ),
):
    ''' Surveys release versions published in static website. '''

    use_extant: __.typx.Annotated[
        bool,
        __.typx.Doc( ''' Fetch publication branch and use tarball. ''' ),
    ] = False

    async def __call__(
        self, auxdata: __.Globals, display: _interfaces.ConsoleDisplay
    ) -> None:
        survey( auxdata, use_extant = self.use_extant )


class UpdateCommand(
    _interfaces.CliCommand, decorators = ( __.standard_tyro_class, ),
):
    ''' Updates static website for particular release version. '''

    version: __.typx.Annotated[
        str,
        __.typx.Doc( ''' Release version to update. ''' ),
        __.tyro.conf.Positional,
    ]

    use_extant: __.typx.Annotated[
        bool,
        __.typx.Doc( ''' Fetch publication branch and use tarball. ''' ),
    ] = False

    production: __.typx.Annotated[
        bool,
        __.typx.Doc( ''' Update publication branch with new tarball.
                     Implies --use-extant to prevent data loss. ''' ),
    ] = False

    async def __call__(
        self, auxdata: __.Globals, display: _interfaces.ConsoleDisplay
    ) -> None:
        update(
            auxdata, self.version,
            use_extant = self.use_extant,
            production = self.production )


class CommandDispatcher(
    _interfaces.CliCommand, decorators = ( __.standard_tyro_class, ),
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

    async def __call__(
        self, auxdata: __.Globals, display: _interfaces.ConsoleDisplay
    ) -> None:
        ictr( 1 )( self.command )
        await self.command( auxdata = auxdata, display = display )


class Locations( __.immut.DataclassObject ):
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


def survey(
    auxdata: __.Globals, *,
    project_anchor: __.Absential[ __.Path ] = __.absent,
    use_extant: bool = False
) -> None:
    ''' Surveys release versions published in static website.

        Lists all versions from the versions manifest, showing their
        available documentation types and highlighting the latest version.
    '''
    locations = Locations.from_project_anchor( auxdata, project_anchor )

    # Handle --use-extant flag: fetch publication branch and checkout tarball
    if use_extant:
        _fetch_publication_branch_and_tarball( locations )
        # Extract the fetched tarball to view published versions
        if locations.archive.is_file( ):
            from tarfile import open as tarfile_open
            if locations.website.is_dir( ):
                __.shutil.rmtree( locations.website )
            locations.website.mkdir( exist_ok = True, parents = True )
            with tarfile_open( locations.archive, 'r:xz' ) as archive:
                archive.extractall( path = locations.website ) # noqa: S202

    if not locations.versions.is_file( ):
        context = "published" if use_extant else "local"
        print( f"No versions manifest found for {context} website. "
               f"Run 'website update' first." )
        return
    with locations.versions.open( 'r' ) as file:
        data = __.json.load( file )
    versions = data.get( 'versions', { } )
    latest = data.get( 'latest_version' )
    if not versions:
        context = "published" if use_extant else "local"
        print( f"No versions found in {context} manifest." )
        return
    context = "Published" if use_extant else "Local"
    print( f"{context} versions:" )
    for version, species in versions.items( ):
        marker = " (latest)" if version == latest else ""
        species_list = ', '.join( species ) if species else "none"
        print( f"  {version}{marker}: {species_list}" )


def update(
    auxdata: __.Globals,
    version: str, *,
    project_anchor: __.Absential[ __.Path ] = __.absent,
    use_extant: bool = False,
    production: bool = False
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
    # --production implies --use-extant to prevent clobbering existing versions
    if use_extant or production:
        _fetch_publication_branch_and_tarball( locations )
    if locations.website.is_dir( ): __.shutil.rmtree( locations.website )
    locations.website.mkdir( exist_ok = True, parents = True )
    if locations.archive.is_file( ):
        with tarfile_open( locations.archive, 'r:xz' ) as archive:
            archive.extractall( path = locations.website ) # noqa: S202
    available_species = _update_available_species( locations, version )
    j2context = _jinja2.Environment(
        loader = _jinja2.FileSystemLoader( locations.templates ),
        autoescape = True )
    index_data = _update_versions_json( locations, version, available_species )
    _enhance_index_data_with_stable_dev( index_data )
    _create_stable_dev_directories( locations, index_data )
    _update_index_html( locations, j2context, index_data )
    if ( locations.artifacts / 'coverage-pytest' ).is_dir( ):
        _update_coverage_badge( locations, j2context )
        _update_version_coverage_badge( locations, j2context, version )
    ( locations.website / '.nojekyll' ).touch( )
    from .filesystem import chdir
    with chdir( locations.website ): # noqa: SIM117
        with tarfile_open( locations.archive, 'w:xz' ) as archive:
            archive.add( '.' )
    if production: _update_publication_branch( locations, version )


def _create_stable_dev_directories(
    locations: Locations, data: dict[ __.typx.Any, __.typx.Any ]
) -> None:
    ''' Creates stable/ and development/ directories with current releases.

        Copies the content from the identified stable and development versions
        to stable/ and development/ directories to provide persistent URLs
        that don't change when new versions are released.
    '''
    stable_version = data.get( 'stable_version' )
    development_version = data.get( 'development_version' )
    if stable_version:
        stable_source = locations.website / stable_version
        stable_dest = locations.website / 'stable'
        if stable_dest.is_dir( ):
            __.shutil.rmtree( stable_dest )
        if stable_source.is_dir( ):
            __.shutil.copytree( stable_source, stable_dest )
    if development_version:
        dev_source = locations.website / development_version
        dev_dest = locations.website / 'development'
        if dev_dest.is_dir( ):
            __.shutil.rmtree( dev_dest )
        if dev_source.is_dir( ):
            __.shutil.copytree( dev_source, dev_dest )


def _enhance_index_data_with_stable_dev(
    data: dict[ __.typx.Any, __.typx.Any ]
) -> None:
    ''' Enhances index data with stable/development version information.

        Identifies the latest stable release and latest development version
        from the versions data and adds them as separate entries for the
        stable/development table.
    '''
    from packaging.version import Version
    versions = data.get( 'versions', { } )
    if not versions:
        data[ 'stable_dev_versions' ] = { }
        return
    stable_version = None
    development_version = None
    # Sort versions by packaging.version.Version for proper comparison
    sorted_versions = sorted(
        versions.items( ),
        key = lambda entry: Version( entry[ 0 ] ),
        reverse = True )
    # Find latest stable (non-prerelease) and development (prerelease) versions
    for version_string, species in sorted_versions:
        version_obj = Version( version_string )
        if not version_obj.is_prerelease and stable_version is None:
            stable_version = ( version_string, species )
        if version_obj.is_prerelease and development_version is None:
            development_version = ( version_string, species )
        if stable_version and development_version:
            break
    stable_dev_versions: dict[ str, tuple[ str, ... ] ] = { }
    if stable_version:
        stable_dev_versions[ 'stable (current)' ] = stable_version[ 1 ]
        data[ 'stable_version' ] = stable_version[ 0 ]
    if development_version:
        stable_dev_versions[ 'development (current)' ] = (
            development_version[ 1 ] )
        data[ 'development_version' ] = development_version[ 0 ]
    data[ 'stable_dev_versions' ] = stable_dev_versions


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


def _fetch_publication_branch_and_tarball( locations: Locations ) -> None:
    ''' Fetches publication branch and checks out existing tarball.

        Attempts to fetch the publication branch from origin and checkout
        the website tarball. Ignores failures if branch or tarball don't exist.
    '''
    with __.ctxl.suppress( Exception ):
        __.subprocess.run(
            [ 'git', 'fetch', 'origin', 'publication:publication' ],
            cwd = locations.project,
            check = False,
            capture_output = True )
    with __.ctxl.suppress( Exception ):
        __.subprocess.run(
            [ 'git', 'checkout', 'publication', '--',
              str( locations.archive ) ],
            cwd = locations.project,
            check = False,
            capture_output = True )


def _generate_coverage_badge_svg(
    locations: Locations, j2context: _jinja2.Environment
) -> str:
    ''' Generates coverage badge SVG content.

        Returns the rendered SVG content for a coverage badge based on the
        current coverage percentage. Colors indicate coverage quality:
        - red: < 50%
        - yellow: 50-79%
        - green: >= 80%
    '''
    coverage = _extract_coverage( locations )
    color = (
        'red' if coverage < 50 else ( # noqa: PLR2004
            'yellow' if coverage < 80 else 'green' ) ) # noqa: PLR2004
    label_text = 'coverage'
    value_text = f"{coverage}%"
    label_width = len( label_text ) * 6 + 10
    value_width = len( value_text ) * 6 + 15
    total_width = label_width + value_width
    template = j2context.get_template( 'coverage.svg.jinja' )
    # TODO: Add error handling for template rendering failures.
    return template.render(
        color = color,
        total_width = total_width,
        label_text = label_text,
        value_text = value_text,
        label_width = label_width,
        value_width = value_width )


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


def _update_coverage_badge(
    locations: Locations, j2context: _jinja2.Environment
) -> None:
    ''' Updates coverage badge SVG.

        Generates a color-coded coverage badge based on the current coverage
        percentage and writes it to the main coverage.svg location.
    '''
    svg_content = _generate_coverage_badge_svg( locations, j2context )
    with locations.coverage.open( 'w' ) as file:
        file.write( svg_content )


def _update_publication_branch( locations: Locations, version: str ) -> None:
    ''' Updates publication branch with new tarball.

        Adds the tarball to git, commits to the publication branch, and pushes
        to origin. Uses the same approach as the GitHub workflow.
    '''
    __.subprocess.run(
        [ 'git', 'add', str( locations.archive ) ],
        cwd = locations.project,
        check = True )
    # Commit to publication branch without checkout
    # Get current tree hash
    tree_result = __.subprocess.run(
        [ 'git', 'write-tree' ],
        cwd = locations.project,
        check = True, capture_output = True, text = True )
    tree_hash = tree_result.stdout.strip( )
    # Check if publication branch exists
    publication_exists = __.subprocess.run(
        [ 'git', 'show-ref', '--verify', '--quiet', 'refs/heads/publication' ],
        cwd = locations.project,
        check = False ).returncode == 0
    commit_result = __.subprocess.run(
        [ 'git', 'commit-tree', tree_hash,
          *( ( '-p', 'publication' ) if publication_exists else ( ) ),
          '-m', f"Update documents for publication. ({version})" ],
        cwd = locations.project,
        check = True, capture_output = True, text = True )
    commit_hash = commit_result.stdout.strip( )
    __.subprocess.run(
        [ 'git', 'branch', '--force', 'publication', commit_hash ],
        cwd = locations.project,
        check = True )
    __.subprocess.run(
        [ 'git', 'push', 'origin', 'publication:publication' ],
        cwd = locations.project,
        check = True )


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


def _update_version_coverage_badge(
    locations: Locations, j2context: _jinja2.Environment, version: str
) -> None:
    ''' Updates version-specific coverage badge SVG.

        Generates a coverage badge for the specific version and places it
        in the version's subtree. This allows each version to have its own
        coverage badge accessible at version/coverage.svg.
    '''
    svg_content = _generate_coverage_badge_svg( locations, j2context )
    version_coverage_path = locations.website / version / 'coverage.svg'
    with version_coverage_path.open( 'w' ) as file:
        file.write( svg_content )


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
