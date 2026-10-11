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


''' Publication building, promotion, and synchronization. '''


import jinja2 as _jinja2

from .. import __
from .. import exceptions as _exceptions
from .inventory import (
    _reject_alias_collisions,
    _snapshot_archive,
    _validate_legacy_inventory,
    _verify_retained_history,
)
from .locations import Locations
from .tracks import (
    _DEFAULT_TRACKS,
    TrackConfiguration,
    _is_package_version,
    _reject_ambiguous_known_tags,
    _select_latest,
    _validate_alias,
    load_track_configuration,
    validate_track_configuration,
)


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
    configuration: __.Absential[ __.Path | str ] = __.absent,
    legacy_inventory: __.Absential[ __.Path | str ] = __.absent,
) -> None:
    ''' Updates project website with latest documentation and coverage.

        Processes the specified version, copies documentation artifacts,
        updates version information, and generates coverage badges.
        Track configuration resolves from the explicit argument, then
        the standard project configuration file, then baked-in defaults.
    '''
    ictr( 2 )( version )
    _validate_version_label( version )
    locations = Locations.from_project_anchor( auxdata, project_anchor )
    if not __.is_absent( configuration ):
        tracks = load_track_configuration( configuration )  # type: ignore[arg-type]
    elif tracks is _DEFAULT_TRACKS:
        candidate = (
            locations.project / '.auxiliary'
            / 'configuration' / 'website.toml' )
        if candidate.is_file( ):
            tracks = load_track_configuration( candidate )
    tracks = validate_track_configuration( tracks )
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

    from ..filesystem import chdir
    with chdir( locations.website ): # noqa: SIM117
        with tarfile_open( locations.archive, 'w:xz' ) as archive:
            archive.add( '.' )
    if production:
        _update_publication_branch( locations, version, expected_sha )


def _promote_track_aliases(
    locations: Locations, data: dict[ __.typx.Any, __.typx.Any ]
) -> None:
    ''' Promotes every resolved track alias from its selected version.

        All aliases, including custom stable aliases, emit from the
        resolved selections, so out-of-order publishes never downgrade
        an alias to an older version.
    '''
    for alias, version in data.get( 'track_versions', { } ).items( ):
        _copy_version_to_alias( locations, version, alias )


def _validate_version_label( version: str ) -> None:
    ''' Validates version label before any destructive operation.

        Published versions are package versions and must parse as PEP 440
        (with optional leading `v`); anything else fails fast here rather
        than crashing version ordering later.
    '''
    if not version:
        raise _exceptions.PublicationSourceInvalidity( version,
            'empty version' )
    if (
        version.startswith( '/' )
        or version.startswith( '\\' )
        or '..' in version.replace( '\\', '/' ).split( '/' )
        or '/' in version
        or '\\' in version
        or version in ( '.', '..' )
        or version.startswith( '.' )
    ):
        raise _exceptions.PublicationSourceInvalidity( version,
            'traversal rejected' )
    from packaging.version import InvalidVersion, Version
    try: Version( version.lstrip( 'v' ) )
    except InvalidVersion as exception:
        raise _exceptions.PublicationSourceInvalidity(
            version, 'unparseable version' ) from exception


def _build_publication_tree(
    locations: Locations, version: str, tracks: TrackConfiguration,
    strict: bool = False,
    legacy_inventory: __.Absential[ __.Path | str ] = __.absent,
) -> None:
    ''' Builds version tree, aliases, and indexes for publication. '''
    baseline = _snapshot_archive( locations.archive )
    _restore_publication_tree( locations )
    available_species = _update_available_species( locations, version )
    j2context = _jinja2.Environment(
        loader = _jinja2.FileSystemLoader( locations.templates ),
        autoescape = True )
    index_data = _update_versions_json(
        locations, version, available_species )
    _enhance_index_data_with_stable_dev( index_data, tracks )
    _reject_ambiguous_known_tags(
        tracks, list( index_data.get( 'versions', { } ).keys( ) ) )
    _reject_alias_collisions( index_data, version )
    _promote_track_aliases( locations, index_data )
    _update_index_html( locations, j2context, index_data )
    if ( locations.artifacts / 'coverage-pytest' ).is_dir( ):
        _update_coverage_badge( locations, j2context )
        _update_version_coverage_badge( locations, j2context, version )
    ( locations.website / '.nojekyll' ).touch( )
    _record_provenance( locations, version, tracks, strict )
    _validate_publication_tree( locations, version, index_data )
    _verify_retained_history( locations, baseline, version, tracks )
    if not __.is_absent( legacy_inventory ):
        _validate_legacy_inventory(
            locations, legacy_inventory )  # type: ignore[arg-type]


def _copy_version_to_alias(
    locations: Locations, version: str, alias: str
) -> None:
    ''' Copies version tree to alias directory. '''
    canonical = _validate_alias( alias )
    source = locations.website / version
    destination = locations.website / canonical
    if source == destination: return
    if destination.is_dir( ): __.shutil.rmtree( destination )
    if source.is_dir( ): __.shutil.copytree( source, destination )


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
            versions.keys( ), track.get( 'tag-namespace', '' ),
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
    fetch = _run_git(
        locations, [ 'fetch', 'origin', 'publication:publication' ],
        check = False )
    if fetch.returncode != 0:
        if _remote_has_publication( locations ):
            raise _exceptions.PublicationSourceInvalidity(
                'publication', 'fetch failed with remote branch present' )
        _clear_stale_publication_state( locations )
        return ''
    probe = _run_git(
        locations,
        [ 'rev-parse', '--verify', '--quiet', 'publication' ],
        check = False )
    destination = probe.stdout.strip( ) if probe.returncode == 0 else ''
    if not destination:
        raise _exceptions.PublicationSourceInvalidity(
            'publication', 'unresolvable destination' )
    if locations.archive.is_file( ):
        locations.archive.unlink( )
    checkout = _run_git(
        locations,
        [ 'checkout', destination, '--', str( locations.archive ) ],
        check = False )
    if checkout.returncode != 0 or not locations.archive.is_file( ):
        raise _exceptions.PublicationSourceInvalidity(
            'publication', 'archive unrestorable from destination' )
    return destination


def _clear_stale_publication_state( locations: Locations ) -> None:
    ''' Clears stale local archive and publication ancestry.

        Runs on confirmed remote absence so an absent destination never
        publishes unrelated stale local state. Establishes absence and
        raises when either removal fails.
    '''
    if locations.archive.is_file( ) or locations.archive.is_symlink( ):
        try: locations.archive.unlink( )
        except OSError as exception:
            raise _exceptions.PublicationSourceInvalidity(
                'archive', 'stale archive irremovable' ) from exception
    elif locations.archive.exists( ):
        raise _exceptions.PublicationSourceInvalidity(
            'archive', 'stale archive irremovable' )
    with __.ctxl.suppress( Exception ):
        _run_git(
            locations, [ 'branch', '--delete', '--force', 'publication' ],
            check = False )
    probe = _run_git(
        locations,
        [ 'show-ref', '--verify', '--quiet', 'refs/heads/publication' ],
        check = False )
    if probe.returncode == 0:
        raise _exceptions.PublicationSourceInvalidity(
            'publication', 'stale ancestry irremovable' )


def _remote_has_publication( locations: Locations ) -> bool:
    ''' Checks whether origin holds a publication branch.

        Returns false only when absence is confirmed (no remote or empty
        remote branch list). Raises on query failure so callers fail
        closed instead of guessing absence.
    '''
    remote = _run_git(
        locations, [ 'remote', 'get-url', 'origin' ], check = False )
    if remote.returncode != 0: return False
    try:
        probe = _run_git(
            locations, [ 'ls-remote', '--heads', 'origin', 'publication' ],
            check = False )
    except Exception as exception:
        raise _exceptions.PublicationSourceInvalidity(
            'publication', 'remote probe failed' ) from exception
    if probe.returncode != 0:
        raise _exceptions.PublicationSourceInvalidity(
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
    commit = _resolve_source_identity( locations, version, strict )
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
            raise _exceptions.PublicationSourceInvalidity(
                'provenance', 'unparseable record' ) from exception
        if not isinstance( loaded, dict ):
            raise _exceptions.PublicationSourceInvalidity(
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


def _reject_symlinks_in_tree( root: __.Path ) -> None:
    ''' Rejects symlinks anywhere under publication tree. '''
    for path in sorted( root.rglob( '*' ) ):
        if path.is_symlink( ):
            raise _exceptions.PublicationSourceInvalidity(
                str( path ), 'symlink rejected' )


def _resolve_source_identity(
    locations: Locations, version: str, strict: bool
) -> str:
    ''' Resolves source commit, checking release tag in strict mode. '''
    commit = ''
    with __.ctxl.suppress( Exception ):
        result = _run_git(
            locations, [ 'rev-parse', 'HEAD' ], check = False )
        commit = result.stdout.strip( )
    if strict and not commit:
        raise _exceptions.PublicationSourceInvalidity(
            version, 'source identity unavailable' )
    if strict:
        tag_sha = _resolve_release_tag( locations, version )
        if not tag_sha:
            raise _exceptions.PublicationSourceInvalidity(
                version, 'unresolvable release tag' )
        if tag_sha != commit:
            raise _exceptions.PublicationSourceInvalidity(
                version, 'source identity mismatch' )
    return commit


def _resolve_release_tag( locations: Locations, version: str ) -> str:
    ''' Resolves release tag to commit SHA, or empty when absent.

        Peels exact tag references to commits, so annotated and signed
        tags compare by commit identity. Branches or other revisions
        sharing the name never resolve.
    '''
    candidates = [ version ]
    if not version.startswith( 'v' ):
        candidates.append( 'v' + version )
    for candidate in candidates:
        probe = _run_git(
            locations,
            [ 'rev-parse', '--verify', '--quiet',
              f"refs/tags/{candidate}^{{commit}}" ],
            check = False )
        if probe.returncode == 0 and probe.stdout.strip( ):
            return probe.stdout.strip( )
    return ''


def _restore_publication_tree( locations: Locations ) -> None:
    ''' Restores prior publication tree from archive, if present. '''
    from tarfile import open as tarfile_open
    if locations.website.is_dir( ): __.shutil.rmtree( locations.website )
    locations.website.mkdir( exist_ok = True, parents = True )
    if locations.archive.is_file( ):
        with tarfile_open( locations.archive, 'r:xz' ) as archive:
            _safe_extractall( archive, locations.website )


def _run_git(
    locations: Locations,
    arguments: __.cabc.Sequence[ str ],
    check: bool = True,
) -> __.typx.Any:
    ''' Runs git in the project without ambient repository redirection.

        Strips variables that would redirect git at another repository
        (e.g. `GIT_INDEX_FILE` exported by outer commit hooks) while
        preserving identity, transport, and editor settings.
    '''
    environment = {
        key: value for key, value in __.os.environ.items( )
        if key not in (
            'GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE',
            'GIT_PREFIX', 'GIT_COMMON_DIR' ) }
    return __.subprocess.run(
        [ 'git', *arguments ],
        cwd = locations.project,
        check = check,
        capture_output = True,
        text = True,
        env = environment )


def _safe_extractall( archive: __.typx.Any, destination: __.Path ) -> None:
    ''' Extracts archive after rejecting dangerous members. '''
    for member in archive.getmembers( ):
        name = member.name
        if name.startswith( '/' ) or name.startswith( '\\' ):
            raise _exceptions.PublicationSourceInvalidity(
                name, 'absolute path rejected' )
        parts = name.replace( '\\', '/' ).split( '/' )
        if '..' in parts:
            raise _exceptions.PublicationSourceInvalidity(
                name, 'traversal rejected' )
        if member.issym( ) or member.islnk( ):
            raise _exceptions.PublicationSourceInvalidity(
                name, 'link rejected' )
        if (
            member.ischr( ) or member.isblk( )
            or member.isfifo( ) or member.isdev( )
        ):
            raise _exceptions.PublicationSourceInvalidity(
                name, 'special file rejected' )
        if not ( member.isfile( ) or member.isdir( ) ):
            raise _exceptions.PublicationSourceInvalidity(
                name, 'non-regular rejected' )
    archive.extractall( path = destination ) # noqa: S202


def _validate_publication_tree(
    locations: Locations,
    version: str,
    index_data: dict[ __.typx.Any, __.typx.Any ],
) -> None:
    ''' Validates built tree before alias promotion and archiving. '''
    version_dir = locations.website / version
    if not version_dir.is_dir( ):
        raise _exceptions.PublicationSourceInvalidity( version,
            'version tree absent' )
    for requisite in ( locations.index, locations.versions ):
        if not requisite.is_file( ):
            raise _exceptions.PublicationSourceInvalidity(
                str( requisite ), 'requisite absent' )
    for alias in index_data.get( 'track_versions', { } ):
        if not ( locations.website / alias ).is_dir( ):
            raise _exceptions.PublicationSourceInvalidity( alias,
                'alias tree absent' )
    _reject_symlinks_in_tree( locations.website )


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
        An empty SHA means confirmed remote absence and pushes with an
        expected-absent lease, so concurrent creation fails instead of
        merging with unrelated local ancestry.
    '''
    _run_git( locations, [ 'add', str( locations.archive ) ] )
    # Commit to publication branch without checkout
    # Get current tree hash
    tree_result = _run_git( locations, [ 'write-tree' ] )
    tree_hash = tree_result.stdout.strip( )
    # Check if publication branch exists
    publication_exists = _run_git(
        locations,
        [ 'show-ref', '--verify', '--quiet', 'refs/heads/publication' ],
        check = False ).returncode == 0
    lease_expectation = expected_sha
    commit_result = _run_git(
        locations,
        [ 'commit-tree', tree_hash,
          *( ( '-p', 'publication' ) if publication_exists else ( ) ),
          '-m', f"Update documents for publication. ({version})" ] )
    commit_hash = commit_result.stdout.strip( )
    _run_git(
        locations, [ 'branch', '--force', 'publication', commit_hash ] )
    if lease_expectation:
        _run_git(
            locations,
            [ 'push', '--force-with-lease=publication:'
              + lease_expectation, 'origin', 'publication:publication' ] )
    else:
        _run_git(
            locations,
            [ 'push', '--force-with-lease=publication:',
              'origin', 'publication:publication' ] )


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
