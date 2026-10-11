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


''' Tests for publication track configuration. '''


import pytest

from .__ import create_test_files


def test_065_validate_default_tracks( website ):
    ''' Default tracks validate with stable and development aliases. '''
    tracks = website.validate_track_configuration( website._DEFAULT_TRACKS )
    assert tracks[ 'stable' ][ 'alias' ] == 'stable'
    assert tracks[ 'development' ][ 'alias' ] == 'development'


def test_070_reject_traversal_alias( website ):
    ''' Track aliases with traversal are rejected. '''
    from frigid import Dictionary as FrozenDictionary
    tracks = {
        'evil': FrozenDictionary( {
            'tag-namespace': 'docs-*',
            'selector': 'exact-tag',
            'alias': '../escape',
        } ),
    }
    with pytest.raises( website.TrackConfigurationInvalidity ):
        website.validate_track_configuration( tracks )  # type: ignore[arg-type]


def test_075_reject_namespace_collision( website ):
    ''' Overlapping docs and package namespaces are rejected. '''
    from frigid import Dictionary as FrozenDictionary
    tracks = {
        'stable': FrozenDictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
        'docs': FrozenDictionary( {
            'tag-namespace': '*',
            'selector': 'exact-tag',
            'alias': 'docs-2',
        } ),
    }
    with pytest.raises( website.TrackConfigurationInvalidity ):
        website.validate_track_configuration( tracks )  # type: ignore[arg-type]


def test_080_custom_alias_emitted_from_selection(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Custom stable alias emits from resolved selection. '''
    from frigid import Dictionary as FrozenDictionary
    test_files = {
        'project/.auxiliary/artifacts/sphinx-html/guide.html':
            '<html><body></body></html>',
        'package/data/templates/coverage.svg.jinja': '{{ color }}',
        'package/data/templates/website.html.jinja': '{{ latest_version }}',
    }
    tracks = website.validate_track_configuration( {
        'release': FrozenDictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'release',
        } ),
        'development': FrozenDictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-prerelease',
            'alias': 'development',
        } ),
    } )  # type: ignore[arg-type]
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project,
            tracks = tracks )
        assert ( locations_tmpdir.website / 'release' ).is_dir( )
        assert not ( locations_tmpdir.website / 'stable' ).exists( )


def test_079_default_configuration_location_resolves(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Project configuration file supplies tracks when present. '''
    test_files = {
        'project/.auxiliary/artifacts/sphinx-html/guide.html':
            '<html><body></body></html>',
        'project/.auxiliary/configuration/website.toml':
            '[tracks.release]\n'
            'tag-namespace = "v*"\n'
            'selector = "latest-final"\n'
            'alias = "release"\n',
        'package/data/templates/coverage.svg.jinja': '{{ color }}',
        'package/data/templates/website.html.jinja': '{{ latest_version }}',
    }
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project )
        assert ( locations_tmpdir.website / 'release' ).is_dir( )
        assert not ( locations_tmpdir.website / 'stable' ).exists( )


def test_078_explicit_tracks_beat_ambient_file(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Explicit mapping wins over project configuration file. '''
    from frigid import Dictionary as FrozenDictionary
    test_files = {
        'project/.auxiliary/artifacts/sphinx-html/guide.html':
            '<html><body></body></html>',
        'project/.auxiliary/configuration/website.toml':
            '[tracks.release]\n'
            'tag-namespace = "v*"\n'
            'selector = "latest-final"\n'
            'alias = "release"\n',
        'package/data/templates/coverage.svg.jinja': '{{ color }}',
        'package/data/templates/website.html.jinja': '{{ latest_version }}',
    }
    tracks = website.validate_track_configuration( {
        'stable': FrozenDictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
        'development': FrozenDictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-prerelease',
            'alias': 'development',
        } ),
    } )  # type: ignore[arg-type]
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project,
            tracks = tracks )
        assert ( locations_tmpdir.website / 'stable' ).is_dir( )
        assert not ( locations_tmpdir.website / 'release' ).exists( )


def test_078_default_configuration_fails_closed( website, provide_tempdir ):
    ''' Non-regular, unreadable, or malformed default config aborts. '''
    from pathlib import Path
    project = Path( provide_tempdir ) / 'project'
    configuration = project / '.auxiliary/configuration/website.toml'
    configuration.parent.mkdir( parents = True, exist_ok = True )
    assert website._load_default_configuration(
        project )[ 'stable' ][ 'alias' ] == 'stable'
    configuration.mkdir( exist_ok = True )
    with pytest.raises( website.TrackConfigurationInvalidity ):
        website._load_default_configuration( project )
    configuration.rmdir( )
    configuration.write_text( 'not = [valid', newline = '' )
    with pytest.raises( website.TrackConfigurationInvalidity ):
        website._load_default_configuration( project )
    configuration.write_text(
        '[tracks.stable]\n'
        'tag-namespace = "v*"\n'
        'selector = "latest-final"\n'
        'alias = "stable"\n',
        newline = '' )
    configuration.chmod( 0o000 )
    try:
        with pytest.raises( website.TrackConfigurationInvalidity ):
            website._load_default_configuration( project )
    finally:
        configuration.chmod( 0o644 )


def test_081_out_of_order_publish_keeps_latest(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Older publish after newer does not downgrade aliases. '''
    test_files = {
        'project/.auxiliary/artifacts/sphinx-html/guide.html':
            '<html><body></body></html>',
        'package/data/templates/coverage.svg.jinja': '{{ color }}',
        'package/data/templates/website.html.jinja': '{{ latest_version }}',
    }
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        website.update(
            auxdata_tmpdir, 'v2.0',
            project_anchor = locations_tmpdir.project )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project )
        package_after = sorted(
            path.relative_to(
                locations_tmpdir.website / 'v2.0' ).as_posix( )
            for path in ( locations_tmpdir.website / 'v2.0' ).rglob( '*' ) )
        stable_suffixes = sorted(
            path.relative_to(
                locations_tmpdir.website / 'stable' ).as_posix( )
            for path in ( locations_tmpdir.website / 'stable' ).rglob( '*' ) )
        assert package_after == stable_suffixes


def test_082_overlap_rejected_on_production_path(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Unprobed namespace overlap aborts on retained labels. '''
    from frigid import Dictionary as FrozenDictionary
    test_files = {
        'project/.auxiliary/artifacts/sphinx-html/guide.html':
            '<html><body></body></html>',
        'package/data/templates/coverage.svg.jinja': '{{ color }}',
        'package/data/templates/website.html.jinja': '{{ latest_version }}',
    }
    tracks = website.validate_track_configuration( {
        'stable': FrozenDictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
        'development': FrozenDictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-prerelease',
            'alias': 'development',
        } ),
        'line-a': FrozenDictionary( {
            'tag-namespace': 'v9.*',
            'selector': 'exact-tag',
            'alias': 'line-a',
        } ),
        'line-b': FrozenDictionary( {
            'tag-namespace': 'v9.9',
            'selector': 'exact-tag',
            'alias': 'line-b',
        } ),
    } )  # type: ignore[arg-type]
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        with pytest.raises( website.TrackConfigurationInvalidity ):
            website.update(
                auxdata_tmpdir, 'v9.9',
                project_anchor = locations_tmpdir.project,
                tracks = tracks )


def test_083_reject_unparseable_version_label(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Non-version labels abort before any destructive operation. '''
    test_files = {
        'package/data/templates/coverage.svg.jinja': '{{ color }}',
        'package/data/templates/website.html.jinja': '{{ latest_version }}',
    }
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        with pytest.raises( website.PublicationSourceInvalidity ):
            website.update(
                auxdata_tmpdir, 'docs-2',
                project_anchor = locations_tmpdir.project )
        assert not list( locations_tmpdir.website.iterdir( ) )


def test_088_reject_absolute_alias_and_version( website ):
    ''' Leading-slash aliases and non-version labels are rejected. '''
    from frigid import Dictionary as FrozenDictionary
    tracks = {
        'docs': FrozenDictionary( {
            'tag-namespace': 'docs-*',
            'selector': 'exact-tag',
            'alias': '/docs-2',
        } ),
    }
    with pytest.raises( website.TrackConfigurationInvalidity ):
        website.validate_track_configuration( tracks )  # type: ignore[arg-type]
    for bad_version in (
        '', '../outside', '/absolute', 'a/b', '.hidden', 'docs-2'
    ):
        with pytest.raises( website.PublicationSourceInvalidity ):
            website._validate_version_label( bad_version )
    website._validate_version_label( 'v1.0' )
    website._validate_version_label( '1.61a0' )


def test_089_canonicalize_trailing_slash_alias( website ):
    ''' Trailing-slash aliases are stored in canonical form. '''
    from frigid import Dictionary as FrozenDictionary
    tracks = website.validate_track_configuration( {
        'docs': FrozenDictionary( {
            'tag-namespace': 'docs-*',
            'selector': 'exact-tag',
            'alias': 'docs-2/',
        } ),
    } )  # type: ignore[arg-type]
    assert tracks[ 'docs' ][ 'alias' ] == 'docs-2'


def test_092_reject_claimed_known_tag( website ):
    ''' Known tags claimed by two tracks are rejected. '''
    from frigid import Dictionary as FrozenDictionary
    tracks = {
        'docs-a': FrozenDictionary( {
            'tag-namespace': 'docs-*',
            'selector': 'exact-tag',
            'alias': 'docs-a',
        } ),
        'docs-b': FrozenDictionary( {
            'tag-namespace': 'docs-3*',
            'selector': 'exact-tag',
            'alias': 'docs-b',
        } ),
    }
    with pytest.raises( website.TrackConfigurationInvalidity ):
        website.validate_track_configuration(
            tracks, known_tags = ( 'docs-30', ) )  # type: ignore[arg-type]


def test_093_load_tracks_from_toml( website, exceptions, provide_tempdir ):
    ''' Track configuration loads from TOML file. '''
    from pathlib import Path
    location = Path( provide_tempdir ) / 'tracks.toml'
    location.write_text(
        '[tracks.stable]\n'
        'tag-namespace = "v*"\n'
        'selector = "latest-final"\n'
        'alias = "stable"\n'
        '[tracks.docs-2]\n'
        'tag-namespace = "docs-*"\n'
        'selector = "exact-tag"\n'
        'alias = "docs-2"\n',
        newline = '' )
    tracks = website.load_track_configuration( location )
    assert tracks[ 'stable' ][ 'alias' ] == 'stable'
    assert tracks[ 'docs-2' ][ 'tag-namespace' ] == 'docs-*'
    with pytest.raises( exceptions.FileAwol ):
        website.load_track_configuration(
            Path( provide_tempdir ) / 'absent.toml' )
