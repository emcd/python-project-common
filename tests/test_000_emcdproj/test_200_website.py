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


''' Tests for website maintenance utilities. '''


from contextlib import AsyncExitStack
from pathlib import Path
from shutil import rmtree

import ictruck
import pytest

from platformdirs import PlatformDirs

from .__ import PACKAGE_NAME, cache_import_module, create_test_files


ictruck.register_module( PACKAGE_NAME )


@pytest.fixture
def application( ):
    ''' Provides appcore application module. '''
    return cache_import_module( "appcore.application" )


@pytest.fixture
def distribution( ):
    ''' Provides appcore distribution module. '''
    return cache_import_module( "appcore.distribution" )


@pytest.fixture
def imports( ):
    ''' Provides internal imports package. '''
    return cache_import_module( f"{ PACKAGE_NAME }.__.imports" )


@pytest.fixture
def state( ):
    ''' Provides appcore state module. '''
    return cache_import_module( "appcore.state" )


@pytest.fixture
def exceptions( ):
    ''' Provides exceptions module. '''
    return cache_import_module( f"{ PACKAGE_NAME }.exceptions" )


@pytest.fixture
def website( ):
    ''' Provides website module. '''
    return cache_import_module( f"{ PACKAGE_NAME }.website" )


@pytest.fixture
def auxdata( application, distribution, state ):
    ''' Provides minimal Globals instance for testing in mem fs. '''

    class FakeDistributionInformation:
        def __init__( self, name: str, location: Path, editable: bool ):
            self._info = distribution.Information(
                name = name, location = location, editable = editable )

        def __getattr__( self, name: str ):
            return getattr( self._info, name )

        def provide_data_location( self, *appendages: str ) -> Path:
            base = Path( '/package/data' )
            if appendages: return base.joinpath( *appendages )
            return base

    distribution_obj = FakeDistributionInformation(
        name = PACKAGE_NAME, location = Path( '/package' ), editable = True )
    return state.Globals(
        application = application.Information(
            name = PACKAGE_NAME ),
        configuration = { },  # Empty configuration for tests
        directories = PlatformDirs(
            appname = PACKAGE_NAME, ensure_exists = False ),
        distribution = distribution_obj,
        exits = AsyncExitStack( ) )


@pytest.fixture
def auxdata_tmpdir( application, distribution, state, provide_tempdir ):
    ''' Provides minimal Globals instance for testing on real fs. '''

    class FakeDistributionInformation:
        def __init__( self, name: str, location: Path, editable: bool ):
            self._info = distribution.Information(
                name = name, location = location, editable = editable )

        def __getattr__( self, name: str ):
            return getattr( self._info, name )

        def provide_data_location( self, *appendages: str ) -> Path:
            base = Path( provide_tempdir ) / 'package/data'
            if appendages: return base.joinpath( *appendages )
            return base

    distribution_obj = FakeDistributionInformation(
        name = PACKAGE_NAME,
        location = Path( provide_tempdir ) / 'package',
        editable = True )
    return state.Globals(
        application = application.Information(
            name = PACKAGE_NAME ),
        configuration = { },  # Empty configuration for tests
        directories = PlatformDirs(
            appname = PACKAGE_NAME, ensure_exists = False ),
        distribution = distribution_obj,
        exits = AsyncExitStack( ) )


@pytest.fixture
def locations( auxdata, website, fs ):
    ''' Provides locations in fake filesystem. '''
    fs.create_dir( '/project/.auxiliary/artifacts' )
    fs.create_dir( '/project/.auxiliary/publications' )
    fs.create_dir( '/package/data/templates' )
    return website.Locations.from_project_anchor( auxdata, Path( '/project' ) )


@pytest.fixture
def locations_tmpdir( auxdata_tmpdir, website, provide_tempdir ):
    ''' Provides locations in real filesystem. '''
    ( provide_tempdir / 'project/.auxiliary/artifacts' ).mkdir(
        exist_ok = True, parents = True )
    ( provide_tempdir / 'project/.auxiliary/publications' ).mkdir(
        exist_ok = True, parents = True )
    ( provide_tempdir / 'package/data/templates' ).mkdir(
        exist_ok = True, parents = True )
    return website.Locations.from_project_anchor(
        auxdata_tmpdir, Path( provide_tempdir ) / 'project' )


# def test_000_locations_attributes( locations ):
#     ''' Locations class has expected attributes with injected anchor. '''
#     pathetic = Pathetic( )
#     assert pathetic.compare( locations.project, '/project' )
#     assert pathetic.compare( locations.auxiliary, '/project/.auxiliary' )
#     assert pathetic.compare(
#         locations.publications, '/project/.auxiliary/publications' )
#     assert pathetic.compare(
#         locations.archive,
#         '/project/.auxiliary/publications/website.tar.xz' )
#     assert pathetic.compare(
#         locations.artifacts, '/project/.auxiliary/artifacts' )
#     assert pathetic.compare(
#         locations.website, '/project/.auxiliary/artifacts/website' )
#     assert pathetic.compare(
#         locations.coverage,
#         '/project/.auxiliary/artifacts/website/coverage.svg' )
#     assert pathetic.compare(
#         locations.index,
#         '/project/.auxiliary/artifacts/website/index.html' )
#     assert pathetic.compare(
#         locations.versions,
#         '/project/.auxiliary/artifacts/website/versions.json' )
#     assert pathetic.compare( locations.templates, '/package/data/templates' )


def test_010_extract_coverage( locations, website, fs ):
    ''' Coverage extraction works with valid XML. '''
    xml_content = (
        '<?xml version="1.0" ?><coverage line-rate="0.85"></coverage>' )
    fs.create_file(
        locations.artifacts / 'coverage-pytest/coverage.xml',
        contents = xml_content )
    assert website._extract_coverage( locations ) == 85


def test_020_extract_coverage_missing_file( locations, website, exceptions ):
    ''' Coverage extraction raises FileAwol for missing XML. '''
    with pytest.raises( exceptions.FileAwol ):
        website._extract_coverage( locations )


def test_030_update_available_species( locations, website, fs ):
    ''' Species directories are copied correctly. '''
    fs.create_dir(
        locations.artifacts / 'coverage-pytest' )
    fs.create_file(
        locations.artifacts / 'coverage-pytest/test.txt', contents = 'test' )
    species = website._update_available_species( locations, 'v1.0' )
    assert 'coverage-pytest' in species
    assert ( locations.website / 'v1.0/coverage-pytest/test.txt' ).exists( )


def test_040_update_coverage_badge( locations, website, fs ):
    ''' Coverage badge is updated with injected jinja context. '''
    fs.create_dir( locations.artifacts / 'coverage-pytest' )
    fs.create_file(
        locations.artifacts / 'coverage-pytest/coverage.xml',
        contents = (
            '<?xml version="1.0" ?><coverage line-rate="0.9"></coverage>' ) )
    fs.create_dir( locations.website )
    fs.create_file(
        locations.templates / 'coverage.svg.jinja', contents = '{{ color }}' )
    import jinja2
    j2context = jinja2.Environment(
        loader = jinja2.FileSystemLoader( locations.templates ),
        autoescape = True )
    website._update_coverage_badge( locations, j2context )
    assert locations.coverage.exists( )
    assert locations.coverage.read_text( ) == 'green'


def test_050_update_index_html( locations, website, fs ):
    ''' Index HTML is updated with injected data and jinja context. '''
    fs.create_dir( locations.website )
    fs.create_file(
        locations.templates / 'website.html.jinja',
        contents = '{{ latest_version }}' )
    import jinja2
    j2context = jinja2.Environment(
        loader = jinja2.FileSystemLoader( locations.templates ),
        autoescape = True )
    data = { 'latest_version': 'v1.0' }
    website._update_index_html( locations, j2context, data )
    assert locations.index.exists( )
    assert locations.index.read_text( ) == 'v1.0'


def test_060_update_versions_json( locations, website, fs ):
    ''' Versions JSON is updated correctly. '''
    fs.create_dir( locations.website )
    species = ( 'coverage-pytest', )
    data = website._update_versions_json( locations, 'v1.0', species )
    assert locations.versions.exists( )
    assert data[ 'latest_version' ] == 'v1.0'
    assert data[ 'versions' ][ 'v1.0' ] == species


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
            'tag_namespace': 'docs-*',
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
            'tag_namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
        'docs': FrozenDictionary( {
            'tag_namespace': '*',
            'selector': 'exact-tag',
            'alias': 'docs-2',
        } ),
    }
    with pytest.raises( website.TrackConfigurationInvalidity ):
        website.validate_track_configuration( tracks )  # type: ignore[arg-type]


def test_080_select_docs_alias_leaves_stable_pinned( website ):
    ''' Package versions select no docs alias; docs tags do. '''
    from frigid import Dictionary as FrozenDictionary
    tracks = website.validate_track_configuration( {
        'stable': FrozenDictionary( {
            'tag_namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
        'development': FrozenDictionary( {
            'tag_namespace': 'v*',
            'selector': 'latest-prerelease',
            'alias': 'development',
        } ),
        'docs-2': FrozenDictionary( {
            'tag_namespace': 'docs-2',
            'selector': 'exact-tag',
            'alias': 'docs-2',
        } ),
    } )  # type: ignore[arg-type]
    assert website.__.is_absent(
        website.select_docs_alias( 'v1.0', tracks ) )
    assert website.select_docs_alias( 'docs-2', tracks ) == 'docs-2'


def test_085_docs_alias_does_not_alter_stable(
    locations, website, fs
):
    ''' Docs alias creation copies version tree without stable changes. '''
    fs.create_dir( locations.website / 'docs-2/sphinx-html' )
    fs.create_file(
        locations.website / 'docs-2/guide.txt', contents = 'guide' )
    fs.create_dir( locations.website / 'stable' )
    website._create_docs_alias_directories(
        locations, 'docs-2', 'docs-2-copy' )
    assert ( locations.website / 'docs-2-copy/guide.txt' ).exists( )
    assert ( locations.website / 'stable' ).exists( )


class _FakeMember:
    ''' Stands in for tarfile members in archive rejection tests. '''

    def __init__(
        self, name, symlink = False, hardlink = False,
        special = False, regular = True
    ):
        self.name = name
        self._symlink = symlink
        self._hardlink = hardlink
        self._special = special
        self._regular = regular
    def issym( self ): return self._symlink
    def islnk( self ): return self._hardlink
    def ischr( self ): return self._special
    def isblk( self ): return False
    def isfifo( self ): return self._special
    def isdev( self ): return self._special
    def isfile( self ): return self._regular and not self._special
    def isdir( self ): return False


class _FakeArchive:
    ''' Stands in for tarfile archives in rejection tests. '''

    def __init__( self, members ): self._members = members
    def getmembers( self ): return self._members
    def extractall( self, path = None ): raise AssertionError( 'extract' )


def _assert_rejected( website, destination, member ):
    ''' Asserts archive with single member is rejected. '''
    archive = _FakeArchive( [ member ] )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website._safe_extractall( archive, destination )


def test_086_reject_dangerous_archive_members( website, provide_tempdir ):
    ''' Archive members with traversal or links are rejected. '''
    from pathlib import Path
    destination = Path( provide_tempdir ) / 'destination'
    for bad_name in ( '/absolute.txt', '../traversal.txt', 'a/../../b.txt' ):
        _assert_rejected( website, destination, _FakeMember( bad_name ) )
    _assert_rejected(
        website, destination, _FakeMember( 'good.txt', symlink = True ) )
    _assert_rejected(
        website, destination, _FakeMember( 'dev-null', special = True ) )


def test_088_reject_absolute_alias_and_version( website ):
    ''' Leading-slash aliases and escaping versions are rejected. '''
    from frigid import Dictionary as FrozenDictionary
    tracks = {
        'docs': FrozenDictionary( {
            'tag_namespace': 'docs-*',
            'selector': 'exact-tag',
            'alias': '/docs-2',
        } ),
    }
    with pytest.raises( website.TrackConfigurationInvalidity ):
        website.validate_track_configuration( tracks )  # type: ignore[arg-type]
    for bad_version in ( '', '../outside', '/absolute', 'a/b', '.hidden' ):
        with pytest.raises( website.PublicationSourceInvalidity ):
            website._validate_version_label( bad_version )
    website._validate_version_label( 'v1.0' )
    website._validate_version_label( 'docs-2' )


def test_089_canonicalize_trailing_slash_alias( website ):
    ''' Trailing-slash aliases are stored in canonical form. '''
    from frigid import Dictionary as FrozenDictionary
    tracks = website.validate_track_configuration( {
        'docs': FrozenDictionary( {
            'tag_namespace': 'docs-*',
            'selector': 'exact-tag',
            'alias': 'docs-2/',
        } ),
    } )  # type: ignore[arg-type]
    assert tracks[ 'docs' ][ 'alias' ] == 'docs-2'


def test_087_reject_symlinks_in_tree( website, provide_tempdir ):
    ''' Symlinks under publication tree are rejected. '''
    from pathlib import Path
    root = Path( provide_tempdir ) / 'site'
    root.mkdir( parents = True, exist_ok = True )
    ( root / 'real.txt' ).write_text( 'real' )
    ( root / 'link.txt' ).symlink_to( root / 'real.txt' )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website._reject_symlinks_in_tree( root )


def test_090_staged_docs2_proof(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Staged docs-2 publish leaves stable pinned and adds docs alias. '''
    from frigid import Dictionary as FrozenDictionary
    coverage_template = '{{ color }}'
    test_files = {
        'project/.auxiliary/artifacts/coverage-pytest/coverage.xml':
            '<?xml version="1.0" ?><coverage line-rate="0.9"></coverage>',
        'package/data/templates/coverage.svg.jinja': coverage_template,
        'package/data/templates/website.html.jinja': '{{ latest_version }}',
    }
    tracks = website.validate_track_configuration( {
        'stable': FrozenDictionary( {
            'tag_namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
        'development': FrozenDictionary( {
            'tag_namespace': 'v*',
            'selector': 'latest-prerelease',
            'alias': 'development',
        } ),
        'docs-2': FrozenDictionary( {
            'tag_namespace': 'docs-*',
            'selector': 'exact-tag',
            'alias': 'docs-2',
        } ),
    } )  # type: ignore[arg-type]
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project,
            tracks = tracks )
        stable_before = sorted(
            path.relative_to( locations_tmpdir.website ).as_posix( )
            for path in ( locations_tmpdir.website / 'stable' ).rglob( '*' ) )
        website.update(
            auxdata_tmpdir, 'docs-2',
            project_anchor = locations_tmpdir.project,
            tracks = tracks )
        stable_after = sorted(
            path.relative_to( locations_tmpdir.website ).as_posix( )
            for path in ( locations_tmpdir.website / 'stable' ).rglob( '*' ) )
        assert set( stable_before ) <= set( stable_after )
        package_after = sorted(
            path.relative_to(
                locations_tmpdir.website / 'v1.0' ).as_posix( )
            for path in ( locations_tmpdir.website / 'v1.0' ).rglob( '*' ) )
        stable_suffixes = sorted(
            path.relative_to(
                locations_tmpdir.website / 'stable' ).as_posix( )
            for path in ( locations_tmpdir.website / 'stable' ).rglob( '*' ) )
        assert package_after == stable_suffixes
        assert ( locations_tmpdir.website / 'docs-2' ).is_dir( )
        import json
        provenance = json.loads(
            ( locations_tmpdir.website / 'provenance.json' ).read_text( ) )
        assert provenance[ 'version' ] == 'docs-2'
        assert 'docs-2' in provenance[ 'aliases' ]


def test_091_reject_ambiguous_docs_tracks( website ):
    ''' Multiple docs tracks claiming one version are rejected. '''
    from frigid import Dictionary as FrozenDictionary
    tracks = website.validate_track_configuration( {
        'docs-a': FrozenDictionary( {
            'tag_namespace': 'docs-*',
            'selector': 'exact-tag',
            'alias': 'docs-a',
        } ),
        'docs-b': FrozenDictionary( {
            'tag_namespace': 'docs-9*',
            'selector': 'exact-tag',
            'alias': 'docs-b',
        } ),
    } )  # type: ignore[arg-type]
    with pytest.raises( website.TrackConfigurationInvalidity ):
        website.select_docs_alias( 'docs-99', tracks )


def test_092_reject_claimed_known_tag( website ):
    ''' Known tags claimed by two tracks are rejected. '''
    from frigid import Dictionary as FrozenDictionary
    tracks = {
        'docs-a': FrozenDictionary( {
            'tag_namespace': 'docs-*',
            'selector': 'exact-tag',
            'alias': 'docs-a',
        } ),
        'docs-b': FrozenDictionary( {
            'tag_namespace': 'docs-3*',
            'selector': 'exact-tag',
            'alias': 'docs-b',
        } ),
    }
    with pytest.raises( website.TrackConfigurationInvalidity ):
        website.validate_track_configuration(
            tracks, known_tags = ( 'docs-30', ) )  # type: ignore[arg-type]


def test_093_load_tracks_from_toml( website, provide_tempdir ):
    ''' Track configuration loads from TOML file. '''
    from pathlib import Path
    location = Path( provide_tempdir ) / 'tracks.toml'
    location.write_text(
        '[tracks.stable]\n'
        'tag_namespace = "v*"\n'
        'selector = "latest-final"\n'
        'alias = "stable"\n'
        '[tracks.docs-2]\n'
        'tag_namespace = "docs-*"\n'
        'selector = "exact-tag"\n'
        'alias = "docs-2"\n',
        newline = '' )
    tracks = website.load_track_configuration( location )
    assert tracks[ 'stable' ][ 'alias' ] == 'stable'
    assert tracks[ 'docs-2' ][ 'tag_namespace' ] == 'docs-*'
    with pytest.raises( website._exceptions.FileAwol ):
        website.load_track_configuration(
            Path( provide_tempdir ) / 'absent.toml' )


def test_094_stale_lease_fails_without_loss( website, provide_tempdir ):
    ''' Stale compare-and-swap baseline fails instead of losing updates. '''
    import shutil
    import subprocess
    executable = shutil.which( 'git' )
    assert executable is not None
    project = provide_tempdir / 'pubrepo'
    remote = provide_tempdir / 'remote.git'
    archive = project / 'website.tar.xz'
    project.mkdir( parents = True, exist_ok = True )
    archive.write_bytes( b'archive-a' )
    def git( *args ):
        return subprocess.run(  # noqa: S603
            [ executable, *args ], cwd = project, check = True,
            capture_output = True, text = True )
    subprocess.run(  # noqa: S603
        [ executable, 'init', '--bare', str( remote ) ],
        check = True, capture_output = True )
    git( 'init' )
    git( 'config', 'user.email', 'test@example.com' )
    git( 'config', 'user.name', 'Test' )
    git( 'remote', 'add', 'origin', str( remote ) )
    git( 'add', str( archive ) )
    git( 'commit', '-m', 'base' )
    locations = website.Locations(
        project = project,
        auxiliary = project / '.auxiliary',
        publications = project / '.auxiliary/publications',
        archive = archive,
        artifacts = project / '.auxiliary/artifacts',
        website = project / '.auxiliary/artifacts/website',
        coverage = project / '.auxiliary/artifacts/website/coverage.svg',
        index = project / '.auxiliary/artifacts/website/index.html',
        versions = project / '.auxiliary/artifacts/website/versions.json',
        templates = project / 'templates' )
    baseline = website._fetch_publication_branch_and_tarball( locations )
    assert baseline == ''
    website._update_publication_branch( locations, 'v1', baseline )
    published_a = git( 'rev-parse', 'publication' ).stdout.strip( )
    proceeding = git(
        'commit-tree', 'HEAD^{tree}', '-p', 'publication',
        '-m', 'writer B' ).stdout.strip( )
    git( 'push', 'origin', proceeding + ':publication' )
    with pytest.raises( subprocess.CalledProcessError ):
        website._update_publication_branch(
            locations, 'v1-stale', published_a )
    remote_head = subprocess.run(  # noqa: S603
        [ executable, '--git-dir', str( remote ),
          'rev-parse', 'publication' ],
        check = True, capture_output = True, text = True ).stdout.strip( )
    assert remote_head == proceeding
    website._update_publication_branch( locations, 'v1-fresh', proceeding )
    remote_head = subprocess.run(  # noqa: S603
        [ executable, '--git-dir', str( remote ),
          'rev-parse', 'publication' ],
        check = True, capture_output = True, text = True ).stdout.strip( )
    assert remote_head != proceeding


def test_100_integration_update(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Update with real filesystem. '''
    coverage_template = '''
<svg width="{{ total_width }}" height="20">
    <rect width="{{ label_width }}" height="20" fill="grey"/>
    <rect x="{{ label_width }}"
          width="{{ value_width }}" height="20" fill="{{ color }}"/>
    <text x="5" y="15" fill="white">{{ label_text }}</text>
    <text x="{{ label_width + 5 }}" y="15" fill="white">{{ value_text }}</text>
</svg>
    '''.strip( )
    test_files = {
        'project/.auxiliary/artifacts/coverage-pytest/coverage.xml':
            '<?xml version="1.0" ?><coverage line-rate="0.75"></coverage>',
        'package/data/templates/coverage.svg.jinja': coverage_template,
        'package/data/templates/website.html.jinja': '{{ latest_version }}',
    }
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project )
        assert locations_tmpdir.coverage.exists( )
        assert locations_tmpdir.index.read_text( ) == 'v1.0'
        assert ( locations_tmpdir.website / '.nojekyll' ).exists( )
        assert locations_tmpdir.archive.exists( )
        # Second pass to cover some branches not hit on first pass.
        rmtree( locations_tmpdir.artifacts / 'coverage-pytest' )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project )
