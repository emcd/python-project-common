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

    tracks_config: __.typx.Annotated[
        str,
        __.typx.Doc( ''' Track configuration TOML file for publication. ''' ),
    ] = ''

    legacy_inventory: __.typx.Annotated[
        str,
        __.typx.Doc( ''' Legacy-link inventory TOML file for validation. ''' ),
    ] = ''

    async def __call__(
        self, auxdata: __.Globals, display: _interfaces.ConsoleDisplay
    ) -> None:
        tracks: TrackConfiguration = _DEFAULT_TRACKS
        if self.tracks_config:
            tracks = load_track_configuration( self.tracks_config )
        inventory: __.Absential[ __.Path ] = __.absent
        if self.legacy_inventory:
            inventory = __.Path( self.legacy_inventory )
        update(
            auxdata, self.version,
            use_extant = self.use_extant,
            production = self.production,
            tracks = tracks,
            legacy_inventory = inventory )


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


TrackConfiguration: __.typx.TypeAlias = __.cabc.Mapping[ str, __.typx.Any ]
TrackMap: __.typx.TypeAlias = __.immut.Dictionary[ str, __.typx.Any ]

_VALID_SELECTORS: tuple[ str, ... ] = (
    'latest-final', 'latest-prerelease', 'exact-tag' )

_DEFAULT_TRACKS: TrackMap = (
    __.immut.Dictionary( {
        'stable': __.immut.Dictionary( {
            'tag_namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
        'development': __.immut.Dictionary( {
            'tag_namespace': 'v*',
            'selector': 'latest-prerelease',
            'alias': 'development',
        } ),
    } ) )


class TrackConfigurationInvalidity( _exceptions.Omnierror, ValueError ):
    ''' Invalid publication track configuration. '''

    def __init__( self, track: str, issue: str ):
        super( ).__init__(
            f"Invalid track configuration for '{track}': {issue}." )


class PublicationSourceInvalidity( _exceptions.Omnierror, ValueError ):
    ''' Invalid publication source or tree. '''

    def __init__( self, source: str, issue: str ):
        super( ).__init__(
            f"Invalid publication source '{source}': {issue}." )


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


def matches_namespace( tag: str, namespace: str ) -> bool:
    ''' Checks whether tag matches track namespace pattern. '''
    from fnmatch import fnmatchcase
    return fnmatchcase( tag, namespace )


def select_docs_alias(
    version: str,
    tracks: TrackConfiguration = _DEFAULT_TRACKS,
) -> __.Absential[ str ]:
    ''' Selects docs-line alias for version without altering stable/dev. '''
    candidates: list[ str ] = [ ]
    for name, track in tracks.items( ):
        if name in ( 'stable', 'development' ): continue
        namespace = track.get( 'tag_namespace', '' )
        selector = track.get( 'selector', 'exact-tag' )
        if not matches_namespace( version, namespace ): continue
        if not _selector_claims( version, selector ): continue
        candidates.append( track.get( 'alias', name ) )
    if not candidates: return __.absent
    if len( candidates ) > 1:
        raise TrackConfigurationInvalidity(
            version, 'ambiguous docs tracks' )
    return candidates[ 0 ]


def load_track_configuration( location: __.Path | str ) -> TrackMap:
    ''' Loads and validates track configuration from TOML file. '''
    path = __.Path( location )
    try: content = path.read_bytes( )
    except OSError as exception:
        raise _exceptions.FileAwol( path ) from exception
    try: data = _toml_loads( content )
    except Exception as exception:
        raise TrackConfigurationInvalidity(
            str( path ), 'unparseable TOML' ) from exception
    if 'tracks' not in data:
        raise TrackConfigurationInvalidity(
            str( path ), "missing 'tracks' table" )
    return validate_track_configuration( data[ 'tracks' ] )


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


def update(  # noqa: PLR0913
    auxdata: __.Globals,
    version: str, *,
    project_anchor: __.Absential[ __.Path ] = __.absent,
    use_extant: bool = False,
    production: bool = False,
    tracks: TrackConfiguration = _DEFAULT_TRACKS,
    legacy_inventory: __.Absential[ __.Path | str ] = __.absent,
) -> None:
    ''' Updates project website with latest documentation and coverage.

        Processes the specified version, copies documentation artifacts,
        updates version information, and generates coverage badges.
    '''
    ictr( 2 )( version )
    _validate_version_label( version )
    tracks = validate_track_configuration( tracks )
    locations = Locations.from_project_anchor( auxdata, project_anchor )
    locations.publications.mkdir( exist_ok = True, parents = True )
    # --production implies --use-extant to prevent clobbering existing versions
    expected_sha = ''
    if use_extant or production:
        expected_sha = _fetch_publication_branch_and_tarball( locations )
    try:
        _build_publication_tree(
            locations, version, tracks, production, legacy_inventory )
    except Exception:
        _restore_publication_tree( locations )
        raise
    from tarfile import open as tarfile_open
    from .filesystem import chdir
    with chdir( locations.website ): # noqa: SIM117
        with tarfile_open( locations.archive, 'w:xz' ) as archive:
            archive.add( '.' )
    if production:
        _update_publication_branch( locations, version, expected_sha )


def validate_track_configuration(
    tracks: TrackConfiguration,
    known_tags: __.Absential[ __.cabc.Sequence[ str ] ] = __.absent,
) -> TrackMap:
    ''' Validates track namespaces, selectors, and aliases. '''
    normalized: dict[ str, __.immut.Dictionary[ str, str ] ] = { }
    aliases: set[ str ] = set( )
    namespaces: list[ tuple[ str, str ] ] = [ ]
    for name, track in tracks.items( ):
        try: namespace = track[ 'tag_namespace' ]
        except KeyError as exception:
            raise TrackConfigurationInvalidity(
                name, "missing 'tag_namespace'" ) from exception
        try: selector = track[ 'selector' ]
        except KeyError as exception:
            raise TrackConfigurationInvalidity(
                name, "missing 'selector'" ) from exception
        try: alias = track[ 'alias' ]
        except KeyError as exception:
            raise TrackConfigurationInvalidity(
                name, "missing 'alias'" ) from exception
        if selector not in _VALID_SELECTORS:
            raise TrackConfigurationInvalidity( name, 'invalid selector' )
        canonical = _validate_alias( alias )
        if canonical in aliases:
            raise TrackConfigurationInvalidity( canonical, 'duplicate alias' )
        aliases.add( canonical )
        namespaces.append( ( name, namespace ) )
        normalized[ name ] = __.immut.Dictionary( {
            'tag_namespace': namespace,
            'selector': selector,
            'alias': canonical,
        } )
    selectors: dict[ str, str ] = {
        name: tracks[ name ][ 'selector' ] for name in normalized }
    for i, ( name_a, namespace_a ) in enumerate( namespaces ):
        for name_b, namespace_b in namespaces[ i + 1 : ]:
            if _namespaces_collide(
                namespace_a, selectors[ name_a ],
                namespace_b, selectors[ name_b ],
            ):
                raise TrackConfigurationInvalidity(
                    name_a, f"collides with '{name_b}'" )
    if not __.is_absent( known_tags ):
        _reject_ambiguous_known_tags(
            normalized, known_tags )  # type: ignore[arg-type]
    return __.immut.Dictionary( normalized )


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


def _validate_alias( alias: str ) -> str:
    ''' Validates alias and returns canonical single-component form. '''
    import re
    if not alias:
        raise TrackConfigurationInvalidity( alias, 'empty alias' )
    if alias.startswith( '/' ) or alias.startswith( '\\' ):
        raise TrackConfigurationInvalidity( alias, 'absolute path rejected' )
    normalized = alias.strip( '/' )
    if not normalized:
        raise TrackConfigurationInvalidity( alias, 'empty alias' )
    if (
        '..' in normalized
        or '/' in normalized
        or '\\' in normalized
        or normalized.startswith( '.' )
    ):
        raise TrackConfigurationInvalidity( alias, 'traversal rejected' )
    if not re.match( r'^[a-z0-9][a-z0-9-]*$', normalized ):
        raise TrackConfigurationInvalidity( alias, 'must be kebab-case' )
    return normalized


def _validate_version_label( version: str ) -> None:
    ''' Validates version label before any destructive operation. '''
    if not version:
        raise PublicationSourceInvalidity( version, 'empty version' )
    if (
        version.startswith( '/' )
        or version.startswith( '\\' )
        or '..' in version.replace( '\\', '/' ).split( '/' )
        or '/' in version
        or '\\' in version
        or version in ( '.', '..' )
        or version.startswith( '.' )
    ):
        raise PublicationSourceInvalidity( version, 'traversal rejected' )


def _build_publication_tree(
    locations: Locations, version: str, tracks: TrackConfiguration,
    strict: bool = False,
    legacy_inventory: __.Absential[ __.Path | str ] = __.absent,
) -> None:
    ''' Builds version tree, aliases, and indexes for publication. '''
    _restore_publication_tree( locations )
    available_species = _update_available_species( locations, version )
    j2context = _jinja2.Environment(
        loader = _jinja2.FileSystemLoader( locations.templates ),
        autoescape = True )
    index_data = _update_versions_json(
        locations, version, available_species )
    _enhance_index_data_with_stable_dev( index_data, tracks )
    _create_stable_dev_directories( locations, index_data )
    _promote_docs_alias( locations, version, tracks )
    _update_index_html( locations, j2context, index_data )
    if ( locations.artifacts / 'coverage-pytest' ).is_dir( ):
        _update_coverage_badge( locations, j2context )
        _update_version_coverage_badge( locations, j2context, version )
    ( locations.website / '.nojekyll' ).touch( )
    _record_provenance( locations, version, tracks, strict )
    _validate_publication_tree( locations, version, tracks, index_data )
    if not __.is_absent( legacy_inventory ):
        _validate_legacy_inventory(
            locations, legacy_inventory )  # type: ignore[arg-type]


def _create_docs_alias_directories(
    locations: Locations, version: str, alias: str
) -> None:
    ''' Creates docs-line alias directory without altering stable/dev. '''
    canonical = _validate_alias( alias )
    source = locations.website / version
    destination = locations.website / canonical
    if source == destination: return
    if destination.is_dir( ): __.shutil.rmtree( destination )
    if source.is_dir( ): __.shutil.copytree( source, destination )


def _promote_docs_alias(
    locations: Locations, version: str, tracks: TrackConfiguration
) -> None:
    ''' Promotes docs-line alias for version, leaving stable/dev pinned. '''
    docs_alias = select_docs_alias( version, tracks )
    if __.is_absent( docs_alias ): return
    _create_docs_alias_directories(
        locations, version, docs_alias )  # type: ignore[arg-type]


def _enhance_index_data_with_stable_dev(
    data: dict[ __.typx.Any, __.typx.Any ],
    tracks: TrackConfiguration = _DEFAULT_TRACKS,
) -> None:
    ''' Enhances index data with stable/development version information.

        Selects versions per configured track namespaces and selectors,
        defaulting to latest final release for stable and latest prerelease
        for development exactly as before.
    '''
    versions = data.get( 'versions', { } )
    if not versions:
        data[ 'stable_dev_versions' ] = { }
        data[ 'track_versions' ] = { }
        return
    track_versions: dict[ __.typx.Any, __.typx.Any ] = { }
    for name, track in tracks.items( ):
        selected = _select_latest(
            versions.keys( ), track.get( 'tag_namespace', '' ),
            track.get( 'selector', 'exact-tag' ), name )
        if not __.is_absent( selected ):
            track_versions[ track.get( 'alias', name ) ] = selected
    data[ 'track_versions' ] = track_versions
    stable_version = track_versions.get( 'stable' )
    development_version = track_versions.get( 'development' )
    stable_dev_versions: dict[ str, tuple[ str, ... ] ] = { }
    if stable_version is not None:
        stable_dev_versions[ 'stable (current)' ] = versions[ stable_version ]
        data[ 'stable_version' ] = stable_version
    if development_version is not None:
        stable_dev_versions[ 'development (current)' ] = (
            versions[ development_version ] )
        data[ 'development_version' ] = development_version
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


def _fetch_publication_branch_and_tarball( locations: Locations ) -> str:
    ''' Fetches publication branch and tarball, returning destination SHA.

        Returns the fetched destination commit only when that exact SHA's
        archive was loaded, or an empty string when remote branch absence
        is confirmed. Raises on query failure, failed fetch with a present
        remote branch, and unrestorable archives, so builds never proceed
        silently on stale bases. The returned SHA threads through build to
        push unchanged as the compare-and-swap baseline.
    '''
    fetch = __.subprocess.run(
        [ 'git', 'fetch', 'origin', 'publication:publication' ],
        cwd = locations.project,
        check = False,
        capture_output = True )
    if fetch.returncode != 0:
        if _remote_has_publication( locations ):
            raise PublicationSourceInvalidity(
                'publication', 'fetch failed with remote branch present' )
        return ''
    probe = __.subprocess.run(
        [ 'git', 'rev-parse', '--verify', '--quiet', 'publication' ],
        cwd = locations.project,
        check = False, capture_output = True, text = True )
    destination = probe.stdout.strip( ) if probe.returncode == 0 else ''
    if not destination:
        raise PublicationSourceInvalidity(
            'publication', 'unresolvable destination' )
    if locations.archive.is_file( ):
        locations.archive.unlink( )
    checkout = __.subprocess.run(
        [ 'git', 'checkout', 'publication', '--', str( locations.archive ) ],
        cwd = locations.project,
        check = False,
        capture_output = True )
    if checkout.returncode != 0 or not locations.archive.is_file( ):
        raise PublicationSourceInvalidity(
            'publication', 'archive unrestorable from destination' )
    return destination


def _remote_has_publication( locations: Locations ) -> bool:
    ''' Checks whether origin holds a publication branch.

        Returns false only when absence is confirmed (no remote or empty
        remote branch list). Raises on query failure so callers fail
        closed instead of guessing absence.
    '''
    remote = __.subprocess.run(
        [ 'git', 'remote', 'get-url', 'origin' ],
        cwd = locations.project,
        check = False, capture_output = True )
    if remote.returncode != 0: return False
    try:
        probe = __.subprocess.run(
            [ 'git', 'ls-remote', '--heads', 'origin', 'publication' ],
            cwd = locations.project,
            check = False, capture_output = True, text = True )
    except Exception as exception:
        raise PublicationSourceInvalidity(
            'publication', 'remote probe failed' ) from exception
    if probe.returncode != 0:
        raise PublicationSourceInvalidity(
            'publication', 'remote probe failed' )
    return bool( probe.stdout.strip( ) )


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


def _namespaces_collide(
    namespace_a: str, selector_a: str,
    namespace_b: str, selector_b: str,
) -> bool:
    ''' Checks whether two tracks can claim the same tag. '''
    if namespace_a == '*' or namespace_b == '*': return True
    if (
        namespace_a == namespace_b
        and selector_a == selector_b
    ):
        return True
    if (
        { selector_a, selector_b }
        == { 'latest-final', 'latest-prerelease' }
    ):
        return False
    probes = (
        'v1.0', 'v1.0a1', 'v2.0rc1', 'v10.0', '1.0', '1.0a1', '2.0',
        'docs-1', 'docs-2', 'docs-3', 'docs-1.9', 'docs-3.1',
        'release-1.0', 'stable', 'development', 'nightly', 'latest' )
    for probe in probes:
        if (
            matches_namespace( probe, namespace_a )
            and matches_namespace( probe, namespace_b )
            and _selector_claims( probe, selector_a )
            and _selector_claims( probe, selector_b )
        ):
            return True
    return False


def _selector_claims( tag: str, selector: str ) -> bool:
    ''' Checks whether selector can claim tag. '''
    if selector == 'exact-tag': return True
    try:
        from packaging.version import Version
        version = Version( tag.lstrip( 'v' ) )
    except Exception: return selector == 'latest-final'
    if selector == 'latest-final': return not version.is_prerelease
    return version.is_prerelease


def _record_provenance(
    locations: Locations, version: str, tracks: TrackConfiguration,
    strict: bool = False,
) -> None:
    ''' Records tag-to-commit provenance for publication.

        Maintains one record per retained release. Refuses to record when
        source identity is unavailable in strict mode, so production never
        promotes with empty provenance.
    '''
    import datetime
    commit = ''
    with __.ctxl.suppress( Exception ):
        result = __.subprocess.run(
            [ 'git', 'rev-parse', 'HEAD' ],
            cwd = locations.project,
            check = False, capture_output = True, text = True )
        commit = result.stdout.strip( )
    if strict and not commit:
        raise PublicationSourceInvalidity(
            version, 'source identity unavailable' )
    aliases: list[ str ] = [ ]
    for name, track in tracks.items( ):
        alias = track.get( 'alias', name )
        if alias not in aliases: aliases.append( alias )
    data: dict[ str, __.typx.Any ] = { }
    provenance_file = locations.website / 'provenance.json'
    if provenance_file.is_file( ):
        try:
            with provenance_file.open( 'r' ) as file:
                loaded: dict[ str, __.typx.Any ] = __.json.load( file )
        except ValueError as exception:
            raise PublicationSourceInvalidity(
                'provenance', 'unparseable record' ) from exception
        if not isinstance( loaded, dict ):
            raise PublicationSourceInvalidity(
                'provenance', 'malformed record' )
        data = loaded
    data[ version ] = {
        'commit': commit,
        'timestamp': datetime.datetime.now(
            datetime.timezone.utc ).isoformat( ),
        'aliases': sorted( aliases ),
    }
    with provenance_file.open( 'w' ) as file:
        __.json.dump( data, file, indent = 4 )


def _reject_ambiguous_known_tags(
    tracks: dict[ str, __.immut.Dictionary[ str, str ] ],
    known_tags: __.cabc.Sequence[ str ],
) -> None:
    ''' Rejects known tags claimed by multiple tracks. '''
    for tag in known_tags:
        claimants = [
            name for name, track in tracks.items( )
            if matches_namespace( tag, track[ 'tag_namespace' ] )
            and _selector_claims( tag, track[ 'selector' ] ) ]
        if len( claimants ) > 1:
            raise TrackConfigurationInvalidity(
                tag, 'claimed by multiple tracks' )


def _reject_symlinks_in_tree( root: __.Path ) -> None:
    ''' Rejects symlinks anywhere under publication tree. '''
    for path in sorted( root.rglob( '*' ) ):
        if path.is_symlink( ):
            raise PublicationSourceInvalidity(
                str( path ), 'symlink rejected' )


def _restore_publication_tree( locations: Locations ) -> None:
    ''' Restores prior publication tree from archive, if present. '''
    from tarfile import open as tarfile_open
    if locations.website.is_dir( ): __.shutil.rmtree( locations.website )
    locations.website.mkdir( exist_ok = True, parents = True )
    if locations.archive.is_file( ):
        with tarfile_open( locations.archive, 'r:xz' ) as archive:
            _safe_extractall( archive, locations.website )


def _safe_extractall( archive: __.typx.Any, destination: __.Path ) -> None:
    ''' Extracts archive after rejecting dangerous members. '''
    for member in archive.getmembers( ):
        name = member.name
        if name.startswith( '/' ) or name.startswith( '\\' ):
            raise PublicationSourceInvalidity( name, 'absolute path rejected' )
        parts = name.replace( '\\', '/' ).split( '/' )
        if '..' in parts:
            raise PublicationSourceInvalidity( name, 'traversal rejected' )
        if member.issym( ) or member.islnk( ):
            raise PublicationSourceInvalidity( name, 'link rejected' )
        if (
            member.ischr( ) or member.isblk( )
            or member.isfifo( ) or member.isdev( )
        ):
            raise PublicationSourceInvalidity( name, 'special file rejected' )
        if not ( member.isfile( ) or member.isdir( ) ):
            raise PublicationSourceInvalidity( name, 'non-regular rejected' )
    archive.extractall( path = destination ) # noqa: S202


def _validate_inventory_path( root: __.Path, entry: str ) -> __.Path:
    ''' Resolves inventory entry path under website root. '''
    if entry.startswith( '/' ) or entry.startswith( '\\' ):
        raise PublicationSourceInvalidity( entry, 'absolute path rejected' )
    parts = entry.replace( '\\', '/' ).split( '/' )
    if '..' in parts or not entry:
        raise PublicationSourceInvalidity( entry, 'traversal rejected' )
    return root / entry.replace( '/', __.os.sep )


def _validate_legacy_inventory(
    locations: Locations, inventory: __.Path | str
) -> None:
    ''' Validates legacy-link inventory against built tree.

        Every entry must resolve; frozen entries require matching content
        digests; listed fragments must occur as element IDs. Malformed
        staged input aborts promotion without changing prior output.
    '''
    path = __.Path( inventory )
    try: content = path.read_bytes( )
    except OSError as exception:
        raise _exceptions.FileAwol( path ) from exception
    try: data = _toml_loads( content )
    except Exception as exception:
        raise PublicationSourceInvalidity(
            str( path ), 'unparseable inventory' ) from exception
    try: items = list( data.get( 'entries', [ ] ) )
    except TypeError as exception:
        raise PublicationSourceInvalidity(
            str( path ), 'malformed inventory' ) from exception
    if not items:
        raise PublicationSourceInvalidity(
            str( path ), 'empty inventory' )
    for raw_entry in items:
        _validate_inventory_entry( locations, raw_entry )


def _validate_inventory_entry(
    locations: Locations, raw_entry: __.typx.Any
) -> None:
    ''' Validates one legacy inventory entry against built tree.

        Consumes dynamic TOML values validated at runtime via duck typing;
        malformed staged input aborts promotion.
    '''
    import hashlib
    get = getattr( raw_entry, 'get', None )
    if get is None:
        raise PublicationSourceInvalidity( 'entry', 'malformed entry' )
    relative = get( 'path', '' )
    semantics = get( 'semantics', 'frozen' )
    if semantics not in ( 'frozen', 'follow' ):
        raise PublicationSourceInvalidity( relative, 'unknown semantics' )
    target = _validate_inventory_path( locations.website, relative )
    if not target.is_file( ):
        raise PublicationSourceInvalidity( relative, 'entry absent' )
    digest = get( 'sha256', '' )
    if digest or semantics == 'frozen':
        if not digest:
            raise PublicationSourceInvalidity(
                relative, 'frozen entry without digest' )
        actual = hashlib.sha256( target.read_bytes( ) ).hexdigest( )
        if actual != digest:
            raise PublicationSourceInvalidity(
                relative, 'content drift detected' )
    text = target.read_text( errors = 'replace' )
    try: fragments = list( get( 'fragments', [ ] ) )
    except TypeError as exception:
        raise PublicationSourceInvalidity(
            relative, 'malformed fragments' ) from exception
    for fragment in fragments:
        if f'id="{fragment}"' not in text:
            raise PublicationSourceInvalidity( relative, 'fragment absent' )


def _validate_publication_tree(
    locations: Locations,
    version: str,
    tracks: TrackConfiguration,
    index_data: dict[ __.typx.Any, __.typx.Any ],
) -> None:
    ''' Validates built tree before alias promotion and archiving. '''
    version_dir = locations.website / version
    if not version_dir.is_dir( ):
        raise PublicationSourceInvalidity( version, 'version tree absent' )
    for requisite in ( locations.index, locations.versions ):
        if not requisite.is_file( ):
            raise PublicationSourceInvalidity(
                str( requisite ), 'requisite absent' )
    expected_aliases: list[ str ] = [ ]
    if index_data.get( 'stable_version' ):
        expected_aliases.append( 'stable' )
    if index_data.get( 'development_version' ):
        expected_aliases.append( 'development' )
    docs_alias = select_docs_alias( version, tracks )
    if not __.is_absent( docs_alias ):
        expected_aliases.append( docs_alias )  # type: ignore[arg-type]
    for alias in expected_aliases:
        if not ( locations.website / alias ).is_dir( ):
            raise PublicationSourceInvalidity( alias, 'alias tree absent' )
    _reject_symlinks_in_tree( locations.website )


def _is_package_version( label: __.typx.Any ) -> bool:
    ''' Checks whether label parses as a package version. '''
    from packaging.version import InvalidVersion, Version
    try: Version( str( label ).lstrip( 'v' ) )
    except InvalidVersion: return False
    return True


def _sort_versions(
    versions: dict[ __.typx.Any, __.typx.Any ],
) -> dict[ __.typx.Any, __.typx.Any ]:
    ''' Sorts package versions descending, docs tags after by name. '''
    from packaging.version import Version
    package_entries: list[ tuple[ __.typx.Any, __.typx.Any ] ] = [
        entry for entry in versions.items( )
        if _is_package_version( entry[ 0 ] ) ]
    docs_entries: list[ tuple[ __.typx.Any, __.typx.Any ] ] = [
        entry for entry in versions.items( )
        if not _is_package_version( entry[ 0 ] ) ]
    package_entries.sort(
        key = lambda entry: Version( str( entry[ 0 ] ).lstrip( 'v' ) ),
        reverse = True )
    docs_entries.sort( key = lambda entry: str( entry[ 0 ] ) )
    return dict( package_entries + docs_entries )


def _parse_package_version( label: __.typx.Any ) -> __.typx.Any:
    ''' Parses label as package version, returning None when not parseable. '''
    from packaging.version import InvalidVersion, Version
    try: return Version( str( label ).lstrip( 'v' ) )
    except InvalidVersion: return None


def _select_latest(
    versions: __.cabc.Iterable[ __.typx.Any ],
    namespace: str, selector: str, track: str,
) -> __.Absential[ __.typx.Any ]:
    ''' Selects version for track from namespace and selector. '''
    from packaging.version import Version
    matched = [
        version for version in versions
        if matches_namespace( str( version ), namespace ) ]
    if selector == 'exact-tag':
        if not matched: return __.absent
        if len( matched ) > 1:
            raise TrackConfigurationInvalidity(
                track, 'ambiguous exact-tag matches' )
        return matched[ 0 ]
    package_versions: list[ tuple[ __.typx.Any, Version ] ] = [ ]
    for version in matched:
        parsed = _parse_package_version( version )
        if parsed is None: continue
        if selector == 'latest-final' and parsed.is_prerelease: continue
        if selector == 'latest-prerelease' and not parsed.is_prerelease:
            continue
        package_versions.append( ( version, parsed ) )
    if not package_versions: return __.absent
    package_versions.sort( key = lambda entry: entry[ 1 ], reverse = True )
    return package_versions[ 0 ][ 0 ]


def _toml_loads( content: bytes ) -> dict[ str, __.typx.Any ]:
    ''' Parses TOML content. '''
    from tomli import loads as parse
    result: dict[ str, __.typx.Any ] = parse( content.decode( 'utf-8' ) )
    return result


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


def _update_publication_branch(
    locations: Locations, version: str, expected_sha: str = ''
) -> None:
    ''' Updates publication branch with new tarball.

        Pushes with compare-and-swap against the expected destination SHA
        captured from the same fetch that supplied the archive. Fails
        without lost updates when the destination ref advances concurrently;
        caller refetches, rebuilds, and revalidates or fails. Never
        refetches here, so a stale build cannot acquire a fresh lease.
        An empty SHA means confirmed remote absence and pushes plainly,
        which still fails closed on concurrent creation.
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
    lease_expectation = expected_sha
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
    if lease_expectation:
        __.subprocess.run(
            [ 'git', 'push', '--force-with-lease=publication:'
              + lease_expectation, 'origin', 'publication:publication' ],
            cwd = locations.project,
            check = True )
    else:
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
    if not locations.versions.is_file( ):
        data: dict[ __.typx.Any, __.typx.Any ] = { 'versions': { } }
        with locations.versions.open( 'w' ) as file:
            __.json.dump( data, file, indent = 4 )
    with locations.versions.open( 'r+' ) as file:
        data = __.json.load( file )
        versions = data[ 'versions' ]
        versions[ version ] = species
        versions = _sort_versions( versions )
        data[ 'latest_version' ] = next( iter( versions ) )
        data[ 'versions' ] = versions
        file.seek( 0 )
        __.json.dump( data, file, indent = 4 )
        file.truncate( )
    return data
