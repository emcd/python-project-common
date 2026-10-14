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


''' Publication track configuration and selection. '''


from . import __


TrackConfiguration: __.typx.TypeAlias = __.cabc.Mapping[ str, __.typx.Any ]
TrackMap: __.typx.TypeAlias = __.immut.Dictionary[ str, __.typx.Any ]


_VALID_SELECTORS: tuple[ str, ... ] = (
    'latest-final', 'latest-prerelease', 'exact-tag' )


DEFAULT_TRACKS: TrackMap = (
    __.immut.Dictionary( {
        'stable': __.immut.Dictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
        'development': __.immut.Dictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-prerelease',
            'alias': 'development',
        } ),
    } ) )


def matches_namespace( tag: str, namespace: str ) -> bool:
    ''' Checks whether tag matches track namespace pattern.

        Version labels may be bare ('1.0') while namespaces are
        tag-shaped ('v*'); the 'v'-prefixed form is tried as fallback,
        but only when the label parses as a package version, so
        non-version labels (aliases, docs tags) never match spuriously.
    '''
    from fnmatch import fnmatchcase
    if fnmatchcase( tag, namespace ): return True
    if tag.startswith( 'v' ): return False
    if not fnmatchcase( f'v{tag}', namespace ): return False
    return _parse_package_version( tag ) is not None


def load_default_configuration( project: __.Path ) -> TrackMap:
    ''' Loads standard project configuration file or baked-in defaults.

        Honors default file absence only on confirmed missing-file errors;
        present non-regular, unreadable, or malformed configuration fails
        before publication rather than silently falling back.
    '''
    import stat
    candidate = (
        project / '.auxiliary' / 'configuration' / 'website.toml' )
    try: status = candidate.stat( )
    except FileNotFoundError: return DEFAULT_TRACKS
    except OSError as exception:
        raise __.exceptions.TrackConfigurationInvalidity(
            'configuration', 'unreadable configuration' ) from exception
    if not stat.S_ISREG( status.st_mode ):
        raise __.exceptions.TrackConfigurationInvalidity(
            'configuration', 'non-regular configuration' )
    try: return load_track_configuration( candidate )
    except __.exceptions.FileAwol as exception:
        raise __.exceptions.TrackConfigurationInvalidity(
            'configuration', 'unreadable configuration' ) from exception


def load_track_configuration( location: __.Path | str ) -> TrackMap:
    ''' Loads and validates track configuration from TOML file. '''
    path = __.Path( location )
    try: content = path.read_bytes( )
    except OSError as exception:
        raise __.exceptions.FileAwol( path ) from exception
    try: data = toml_loads( content )
    except Exception as exception:
        raise __.exceptions.TrackConfigurationInvalidity(
            str( path ), 'unparseable TOML' ) from exception
    if 'tracks' not in data:
        raise __.exceptions.TrackConfigurationInvalidity(
            str( path ), "missing 'tracks' table" )
    return validate_track_configuration( data[ 'tracks' ] )


def validate_track_configuration(
    tracks: TrackConfiguration,
    known_tags: __.Absential[ __.cabc.Sequence[ str ] ] = __.absent,
) -> TrackMap:
    ''' Validates track namespaces, selectors, and aliases. '''
    normalized: dict[ str, __.immut.Dictionary[ str, str ] ] = { }
    aliases: set[ str ] = set( )
    namespaces: list[ tuple[ str, str ] ] = [ ]
    for name, track in tracks.items( ):
        try: namespace = track[ 'tag-namespace' ]
        except KeyError as exception:
            raise __.exceptions.TrackConfigurationInvalidity(
                name, "missing 'tag-namespace'" ) from exception
        try: selector = track[ 'selector' ]
        except KeyError as exception:
            raise __.exceptions.TrackConfigurationInvalidity(
                name, "missing 'selector'" ) from exception
        try: alias = track[ 'alias' ]
        except KeyError as exception:
            raise __.exceptions.TrackConfigurationInvalidity(
                name, "missing 'alias'" ) from exception
        if selector not in _VALID_SELECTORS:
            raise __.exceptions.TrackConfigurationInvalidity( name,
                'invalid selector' )
        canonical = validate_alias( alias )
        if canonical in aliases:
            raise __.exceptions.TrackConfigurationInvalidity( canonical,
                'duplicate alias' )
        aliases.add( canonical )
        namespaces.append( ( name, namespace ) )
        normalized[ name ] = __.immut.Dictionary( {
            'tag-namespace': namespace,
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
                raise __.exceptions.TrackConfigurationInvalidity(
                    name_a, f"collides with '{name_b}'" )
    if not __.is_absent( known_tags ):
        reject_ambiguous_known_tags(
            normalized, known_tags )  # type: ignore[arg-type]
    return __.immut.Dictionary( normalized )


def validate_alias( alias: str ) -> str:
    ''' Validates alias and returns canonical single-component form. '''
    import re
    if not alias:
        raise __.exceptions.TrackConfigurationInvalidity( alias,
            'empty alias' )
    if alias.startswith( '/' ) or alias.startswith( '\\' ):
        raise __.exceptions.TrackConfigurationInvalidity( alias,
            'absolute path rejected' )
    normalized = alias.strip( '/' )
    if not normalized:
        raise __.exceptions.TrackConfigurationInvalidity( alias,
            'empty alias' )
    if (
        '..' in normalized
        or '/' in normalized
        or '\\' in normalized
        or normalized.startswith( '.' )
    ):
        raise __.exceptions.TrackConfigurationInvalidity( alias,
            'traversal rejected' )
    if not re.match( r'^[a-z0-9][a-z0-9-]*$', normalized ):
        raise __.exceptions.TrackConfigurationInvalidity( alias,
            'must be kebab-case' )
    return normalized


def _namespaces_collide(
    namespace_a: str, selector_a: str,
    namespace_b: str, selector_b: str,
) -> bool:
    ''' Checks whether two tracks can claim the same tag.

        Only exact-tag pairs can collide ambiguously; overlapping
        latest-selector aliases are legitimate shared pointers.
    '''
    if selector_a != 'exact-tag' and selector_b != 'exact-tag':
        return False
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


def reject_ambiguous_known_tags(
    tracks: __.cabc.Mapping[ str, __.cabc.Mapping[ str, str ] ],
    known_tags: __.cabc.Sequence[ str ],
) -> None:
    ''' Rejects known tags claimed by multiple exact-tag tracks.

        Overlapping latest-selector aliases are legitimate pointers at
        shared versions (e.g. stable and floating major); only exact-tag
        multi-claims are ambiguous about which track owns the tag.
    '''
    for tag in known_tags:
        claimants = [
            name for name, track in tracks.items( )
            if track[ 'selector' ] == 'exact-tag'
            and matches_namespace( tag, track[ 'tag-namespace' ] )
            and _selector_claims( tag, track[ 'selector' ] ) ]
        if len( claimants ) > 1:
            raise __.exceptions.TrackConfigurationInvalidity(
                tag, 'claimed by multiple tracks' )


def is_package_version( label: __.typx.Any ) -> bool:
    ''' Checks whether label parses as a package version. '''
    from packaging.version import InvalidVersion, Version
    try: Version( str( label ).lstrip( 'v' ) )
    except InvalidVersion: return False
    return True


def _parse_package_version( label: __.typx.Any ) -> __.typx.Any:
    ''' Parses label as package version, returning None when not parseable. '''
    from packaging.version import InvalidVersion, Version
    try: return Version( str( label ).lstrip( 'v' ) )
    except InvalidVersion: return None


def select_latest(
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
            raise __.exceptions.TrackConfigurationInvalidity(
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


def toml_loads( content: bytes ) -> dict[ str, __.typx.Any ]:
    ''' Parses TOML content. '''
    from tomli import loads as parse
    result: dict[ str, __.typx.Any ] = parse( content.decode( 'utf-8' ) )
    return result
