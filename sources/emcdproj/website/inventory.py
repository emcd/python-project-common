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


''' Publication validation: inventory, history, and anchors. '''


from .. import __
from .. import exceptions as _exceptions
from .locations import Locations
from .tracks import TrackConfiguration, _toml_loads


_MUTABLE_TOP_LEVEL: tuple[ str, ... ] = (
    'index.html', 'versions.json', 'provenance.json',
    'coverage.svg', '.nojekyll' )


_VOLATILE_VERSION_FILES: tuple[ str, ... ] = (
    'coverage.xml', '.buildinfo' )


def _snapshot_archive( archive: __.Path ) -> dict[ str, str ]:
    ''' Snapshots retained-history digests from the trusted archive.

        Reads the pre-update archive members without extracting, so
        restore loss itself is visible to later comparison. Returns an
        empty manifest when no archive exists yet.
    '''
    import hashlib
    import tarfile
    if not archive.is_file( ): return { }
    manifest: dict[ str, str ] = { }
    try:
        with tarfile.open( archive, mode = 'r:*' ) as bundle:
            for member in bundle.getmembers( ):
                if not member.isfile( ): continue
                name = member.name.replace( '\\', '/' )
                while name.startswith( './' ): name = name[ 2 : ]
                if not name or name == '.': continue
                handle = bundle.extractfile( member )
                if handle is None: continue
                manifest[ name ] = hashlib.sha256(
                    handle.read( ) ).hexdigest( )
    except ( tarfile.TarError, OSError, EOFError ) as exception:
        raise _exceptions.PublicationSourceInvalidity(
            str( archive ), 'unreadable archive' ) from exception
    return manifest


def _reject_alias_collisions(
    index_data: dict[ __.typx.Any, __.typx.Any ],
    version: str,
) -> None:
    ''' Rejects aliases colliding with retained releases.

        An alias pointing at a different retained version would overwrite
        history that the retained check then skips. Only deliberate
        identity (alias equal to its selected version) is allowed.
    '''
    mapping = index_data.get( 'track_versions', { } )
    retained = {
        label for label in index_data.get( 'versions', { } )
        if label != version }
    for alias, selected in mapping.items( ):
        if alias != selected and alias in retained:
            raise _exceptions.PublicationSourceInvalidity(
                alias, 'alias collides with retained release' )
    if version in mapping and mapping.get( version ) != version:
        raise _exceptions.PublicationSourceInvalidity(
            version, 'version collides with alias' )


def _verify_retained_history(
    locations: Locations,
    snapshot: dict[ str, str ],
    version: str,
    tracks: TrackConfiguration,
) -> None:
    ''' Verifies retained history against the pre-build snapshot.

        Every snapshotted file outside the published version, configured
        aliases, and mutable top-level files must exist with identical
        content. Republished versions must reproduce retained files
        byte-identically apart from volatile build outputs; changed
        same-version content is refused while idempotent reruns pass.
        Legitimate new version files and mutable outputs are excluded by
        explicit class rules, never by regeneration.
    '''
    import hashlib
    aliases = {
        track.get( 'alias', name ) for name, track in tracks.items( ) }
    for relative, digest in snapshot.items( ):
        head = relative.split( '/', 1 )[ 0 ]
        if head in aliases and head != version: continue
        if '/' not in relative and relative in _MUTABLE_TOP_LEVEL: continue
        if head == version:
            base = relative.rsplit( '/', 1 )[ -1 ]
            if base in _VOLATILE_VERSION_FILES: continue
        candidate = locations.website / relative
        if not candidate.is_file( ):
            raise _exceptions.PublicationSourceInvalidity( relative,
                'history lost' )
        actual = hashlib.sha256( candidate.read_bytes( ) ).hexdigest( )
        if actual != digest:
            raise _exceptions.PublicationSourceInvalidity( relative,
                'history drift' )


def _validate_inventory_path( root: __.Path, entry: str ) -> __.Path:
    ''' Resolves inventory entry path under website root. '''
    if entry.startswith( '/' ) or entry.startswith( '\\' ):
        raise _exceptions.PublicationSourceInvalidity( entry,
            'absolute path rejected' )
    parts = entry.replace( '\\', '/' ).split( '/' )
    if '..' in parts or not entry:
        raise _exceptions.PublicationSourceInvalidity( entry,
            'traversal rejected' )
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
        raise _exceptions.PublicationSourceInvalidity(
            str( path ), 'unparseable inventory' ) from exception
    try: items = list( data.get( 'entries', [ ] ) )
    except TypeError as exception:
        raise _exceptions.PublicationSourceInvalidity(
            str( path ), 'malformed inventory' ) from exception
    if not items:
        raise _exceptions.PublicationSourceInvalidity(
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
    get = getattr( raw_entry, 'get', None )
    if get is None:
        raise _exceptions.PublicationSourceInvalidity( 'entry',
            'malformed entry' )
    relative = get( 'path', '' )
    semantics = get( 'semantics', 'frozen' )
    if not isinstance( relative, str ) or not isinstance( semantics, str ):
        raise _exceptions.PublicationSourceInvalidity( 'entry',
            'malformed entry' )
    if semantics not in ( 'frozen', 'follow' ):
        raise _exceptions.PublicationSourceInvalidity( relative,
            'unknown semantics' )
    target = _validate_inventory_path( locations.website, relative )
    if not target.is_file( ):
        raise _exceptions.PublicationSourceInvalidity( relative,
            'entry absent' )
    _check_entry_digest(
        target, relative, get( 'sha256', '' ), semantics )
    _check_entry_fragments(
        target, relative, get( 'fragments', [ ] ) )


def _check_entry_digest(
    target: __.Path, relative: str, digest: str, semantics: str
) -> None:
    ''' Checks entry content digest for frozen or pinned entries. '''
    import hashlib
    if digest or semantics == 'frozen':
        if not digest:
            raise _exceptions.PublicationSourceInvalidity(
                relative, 'frozen entry without digest' )
        actual = hashlib.sha256( target.read_bytes( ) ).hexdigest( )
        if actual != digest:
            raise _exceptions.PublicationSourceInvalidity(
                relative, 'content drift detected' )


def _check_entry_fragments(
    target: __.Path, relative: str, fragment_source: __.typx.Any
) -> None:
    ''' Checks entry anchor fragments as parsed element IDs. '''
    if isinstance( fragment_source, str ):
        raise _exceptions.PublicationSourceInvalidity(
            relative, 'malformed fragments' )
    try: fragments = list( fragment_source )
    except TypeError as exception:
        raise _exceptions.PublicationSourceInvalidity(
            relative, 'malformed fragments' ) from exception
    identifiers = _extract_element_ids(
        target.read_text( errors = 'replace' ) )
    for fragment in fragments:
        if not isinstance( fragment, str ) or fragment not in identifiers:
            raise _exceptions.PublicationSourceInvalidity( relative,
                'fragment absent' )


def _extract_element_ids( content: str ) -> set[ str ]:
    ''' Extracts element IDs from HTML content with a real parser. '''
    import html.parser
    identifiers: set[ str ] = set( )

    class Collector( html.parser.HTMLParser ):

        def handle_starttag(
            self, tag: str, attrs: list[ tuple[ str, str | None ] ]
        ) -> None:
            for name, value in attrs:
                if name == 'id' and value:
                    identifiers.add( value )

    parser = Collector( convert_charrefs = True )
    parser.feed( content )
    return identifiers
