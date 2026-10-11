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


''' Tests for publication inventory validation. '''


import pytest

from .conftest import _write_inventory_case


def test_097_validate_legacy_inventory( website, provide_tempdir ):
    ''' Legacy inventory passes on intact tree with digests and anchors. '''
    import hashlib

    from pathlib import Path
    root = Path( provide_tempdir ) / 'site'
    page = root / 'stable/guide.html'
    page.parent.mkdir( parents = True, exist_ok = True )
    content = '<html><body><a id="guide"></a><h1>Guide</h1></body></html>'
    page.write_text( content, newline = '' )
    digest = hashlib.sha256( content.encode( 'utf-8' ) ).hexdigest( )
    inventory = _write_inventory_case(
        provide_tempdir,
        [ ( 'stable/guide.html', digest, ( 'guide', ), 'frozen' ) ] )
    website.validate_legacy_inventory(
        website.Locations(
            project = Path( provide_tempdir ),
            auxiliary = Path( provide_tempdir ) / '.auxiliary',
            publications = Path( provide_tempdir ) / 'publications',
            archive = Path( provide_tempdir ) / 'website.tar.xz',
            artifacts = Path( provide_tempdir ) / 'artifacts',
            website = root,
            coverage = root / 'coverage.svg',
            index = root / 'index.html',
            versions = root / 'versions.json',
            templates = Path( provide_tempdir ) / 'templates' ),
        inventory )


def test_102_reject_bad_inventory_cases( website, provide_tempdir ):
    ''' Missing files, drift, anchors, and malformed input abort. '''
    import hashlib

    from pathlib import Path
    root = Path( provide_tempdir ) / 'site'
    page = root / 'stable/guide.html'
    page.parent.mkdir( parents = True, exist_ok = True )
    content = '<html><body><h1>No anchors here</h1></body></html>'
    page.write_text( content, newline = '' )
    digest = hashlib.sha256( content.encode( 'utf-8' ) ).hexdigest( )
    locations = website.Locations(
        project = Path( provide_tempdir ),
        auxiliary = Path( provide_tempdir ) / '.auxiliary',
        publications = Path( provide_tempdir ) / 'publications',
        archive = Path( provide_tempdir ) / 'website.tar.xz',
        artifacts = Path( provide_tempdir ) / 'artifacts',
        website = root,
        coverage = root / 'coverage.svg',
        index = root / 'index.html',
        versions = root / 'versions.json',
        templates = Path( provide_tempdir ) / 'templates' )
    cases = [
        [ ( 'stable/absent.html', digest, ( ), 'frozen' ) ],
        [ ( 'stable/guide.html', '0' * 64, ( ), 'frozen' ) ],
        [ ( 'stable/guide.html', digest, ( 'guide', ), 'frozen' ) ],
        [ ( 'stable/guide.html', '', ( ), 'frozen' ) ],
        [ ( '../escape.html', digest, ( ), 'frozen' ) ],
    ]
    for entries in cases:
        inventory = _write_inventory_case( provide_tempdir, entries )
        with pytest.raises( website.PublicationSourceInvalidity ):
            website.validate_legacy_inventory( locations, inventory )
    malformed = Path( provide_tempdir ) / 'inventory.toml'
    malformed.write_text( '[[entries]\nbroken', newline = '' )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.validate_legacy_inventory( locations, malformed )


def test_096_reject_comment_anchors_and_string_fragments(
    website, provide_tempdir
):
    ''' Commented IDs do not count; string fragments are malformed. '''
    import hashlib

    from pathlib import Path
    root = Path( provide_tempdir ) / 'site'
    page = root / 'stable/guide.html'
    page.parent.mkdir( parents = True, exist_ok = True )
    content = (
        '<html><body><!-- <a id="ghost"></a> -->'
        '<h1 id="guide">Guide</h1></body></html>' )
    page.write_text( content, newline = '' )
    digest = hashlib.sha256( content.encode( 'utf-8' ) ).hexdigest( )
    locations = website.Locations(
        project = Path( provide_tempdir ),
        auxiliary = Path( provide_tempdir ) / '.auxiliary',
        publications = Path( provide_tempdir ) / 'publications',
        archive = Path( provide_tempdir ) / 'website.tar.xz',
        artifacts = Path( provide_tempdir ) / 'artifacts',
        website = root,
        coverage = root / 'coverage.svg',
        index = root / 'index.html',
        versions = root / 'versions.json',
        templates = Path( provide_tempdir ) / 'templates' )
    assert website.extract_element_ids( content ) == { 'guide' }
    inventory = _write_inventory_case(
        provide_tempdir,
        [ ( 'stable/guide.html', digest, ( 'ghost', ), 'frozen' ) ] )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.validate_legacy_inventory( locations, inventory )
    inventory = Path( provide_tempdir ) / 'inventory.toml'
    inventory.write_text(
        '[[entries]]\n'
        'path = "stable/guide.html"\n'
        f'sha256 = "{digest}"\n'
        'fragments = "guide"\n'
        'semantics = "frozen"\n',
        newline = '' )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.validate_legacy_inventory( locations, inventory )
