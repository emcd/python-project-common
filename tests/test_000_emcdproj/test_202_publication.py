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


''' Tests for publication building and synchronization. '''


from pathlib import Path

import pytest

from .__ import create_test_files
from .conftest import (
    _FakeMember,
    _assert_rejected,
    _git_environment,
    _make_git_repo,
    _write_inventory_case,
)


def test_085_docs_alias_does_not_alter_stable(
    locations, website, fs
):
    ''' Docs alias creation copies version tree without stable changes. '''
    fs.create_dir( locations.website / 'docs-2/sphinx-html' )
    fs.create_file(
        locations.website / 'docs-2/guide.txt', contents = 'guide' )
    fs.create_dir( locations.website / 'stable' )
    website.copy_version_to_alias(
        locations, 'docs-2', 'docs-2-copy' )
    assert ( locations.website / 'docs-2-copy/guide.txt' ).exists( )
    assert ( locations.website / 'stable' ).exists( )


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


def test_087_reject_symlinks_in_tree( website, provide_tempdir ):
    ''' Symlinks under publication tree are rejected. '''
    from pathlib import Path
    root = Path( provide_tempdir ) / 'site'
    root.mkdir( parents = True, exist_ok = True )
    ( root / 'real.txt' ).write_text( 'real' )
    ( root / 'link.txt' ).symlink_to( root / 'real.txt' )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.reject_symlinks_in_tree( root )


def test_090_floating_major_publish_contract(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Floating-major publish tracks newest line release pinned to stable.

        Fixture-based contract pin only; real staged CI receipts are
        required before any production URL cutover.
    '''
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
            'tag-namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
        'development': FrozenDictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-prerelease',
            'alias': 'development',
        } ),
        'v1': FrozenDictionary( {
            'tag-namespace': 'v1.*',
            'selector': 'latest-final',
            'alias': 'v1',
        } ),
    } )  # type: ignore[arg-type]
    inventory = _write_inventory_case(
        provide_tempdir,
        [ ( 'stable/coverage-pytest/coverage.xml', '', ( ), 'follow' ),
          ( 'v1.0/coverage-pytest/coverage.xml', '', ( ), 'follow' ),
          ( 'v1/coverage-pytest/coverage.xml', '', ( ), 'follow' ),
          ( 'index.html', '', ( ), 'follow' ) ] )
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project,
            tracks = tracks,
            legacy_inventory = inventory )
        website.update(
            auxdata_tmpdir, 'v1.1',
            project_anchor = locations_tmpdir.project,
            tracks = tracks,
            legacy_inventory = inventory )
        line_after = sorted(
            path.relative_to(
                locations_tmpdir.website / 'v1' ).as_posix( )
            for path in ( locations_tmpdir.website / 'v1' ).rglob( '*' )
            if path.name != 'coverage.svg' )
        package_after = sorted(
            path.relative_to(
                locations_tmpdir.website / 'v1.1' ).as_posix( )
            for path in ( locations_tmpdir.website / 'v1.1' ).rglob( '*' )
            if path.name != 'coverage.svg' )
        assert line_after == package_after
        stable_suffixes = sorted(
            path.relative_to(
                locations_tmpdir.website / 'stable' ).as_posix( )
            for path in ( locations_tmpdir.website / 'stable' ).rglob( '*' ) )
        assert package_after == stable_suffixes
        import json
        provenance = json.loads(
            ( locations_tmpdir.website / 'provenance.json' ).read_text( ) )
        assert 'v1' in provenance[ 'v1.1' ][ 'aliases' ]
        assert 'v1.0' in provenance


def test_095_provenance_per_release_and_strict(
    locations_tmpdir, website, provide_tempdir
):
    ''' Provenance merges per release and strict refuses empty identity. '''
    import json

    from frigid import Dictionary as FrozenDictionary
    tracks = website.validate_track_configuration( {
        'stable': FrozenDictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
    } )  # type: ignore[arg-type]
    locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
    website.record_provenance(
        locations_tmpdir, 'v1.0', tracks )
    website.record_provenance(
        locations_tmpdir, 'v1.1', tracks )
    provenance = json.loads(
        ( locations_tmpdir.website / 'provenance.json' ).read_text( ) )
    assert set( provenance.keys( ) ) == { 'v1.0', 'v1.1' }
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.record_provenance(
            locations_tmpdir, 'v1.2', tracks, strict = True )


def test_099_reject_unverifiable_fetch_base( website, provide_tempdir ):
    ''' Unverifiable fetch bases abort before any build. '''
    import subprocess
    project = provide_tempdir / 'fetchrepo'
    project.mkdir( parents = True, exist_ok = True )
    def git( *args ):
        import shutil
        executable = shutil.which( 'git' )
        return subprocess.run(  # noqa: S603
            [ executable, *args ], cwd = project, check = True,
            capture_output = True, text = True,
            env = _git_environment( ) )
    git( 'init' )
    git( 'config', 'user.email', 'test@example.com' )
    git( 'config', 'user.name', 'Test' )
    git( 'config', 'commit.gpgsign', 'false' )
    git( 'config', 'tag.gpgsign', 'false' )
    git( 'remote', 'add', 'origin', '/nonexistent/remote.git' )
    locations = website.Locations(
        project = project,
        auxiliary = project / '.auxiliary',
        publications = project / '.auxiliary/publications',
        archive = project / '.auxiliary/publications/website.tar.xz',
        artifacts = project / '.auxiliary/artifacts',
        website = project / '.auxiliary/artifacts/website',
        coverage = project / '.auxiliary/artifacts/website/coverage.svg',
        index = project / '.auxiliary/artifacts/website/index.html',
        versions = project / '.auxiliary/artifacts/website/versions.json',
        templates = project / 'templates' )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.fetch_publication_branch_and_tarball( locations )


def test_101_reject_branch_without_tarball( website, provide_tempdir ):
    ''' Publication branch without tarball aborts before any build. '''
    import shutil
    import subprocess
    executable = shutil.which( 'git' )
    assert executable is not None
    project = provide_tempdir / 'notarball'
    remote = provide_tempdir / 'remote-nt.git'
    project.mkdir( parents = True, exist_ok = True )
    ( project / 'seed.txt' ).write_text( 'seed', newline = '' )
    def git( *args ):
        return subprocess.run(  # noqa: S603
            [ executable, *args ], cwd = project, check = True,
            capture_output = True, text = True,
            env = _git_environment( ) )
    subprocess.run(  # noqa: S603
        [ executable, 'init', '--bare', str( remote ) ],
        check = True, capture_output = True,
        env = _git_environment( ) )
    git( 'init' )
    git( 'config', 'user.email', 'test@example.com' )
    git( 'config', 'user.name', 'Test' )
    git( 'config', 'commit.gpgsign', 'false' )
    git( 'config', 'tag.gpgsign', 'false' )
    git( 'remote', 'add', 'origin', str( remote ) )
    git( 'add', 'seed.txt' )
    git( 'commit', '-m', 'base' )
    git( 'branch', 'publication' )
    git( 'push', 'origin', 'publication:publication' )
    archive = project / '.auxiliary/publications/website.tar.xz'
    archive.parent.mkdir( parents = True, exist_ok = True )
    archive.write_bytes( b'stale-local' )
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
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.fetch_publication_branch_and_tarball( locations )


def test_097_verify_retained_history_classes( website, provide_tempdir ):
    ''' Retained history guards old versions, not new or mutable outputs. '''
    from pathlib import Path

    from frigid import Dictionary as FrozenDictionary
    root = Path( provide_tempdir ) / 'site'
    ( root / 'v1.0' ).mkdir( parents = True, exist_ok = True )
    ( root / 'v1.0/guide.html' ).write_text( 'old', newline = '' )
    ( root / 'v2.0' ).mkdir( parents = True, exist_ok = True )
    ( root / 'v2.0/guide.html' ).write_text( 'new', newline = '' )
    ( root / 'stable' ).mkdir( parents = True, exist_ok = True )
    ( root / 'stable/guide.html' ).write_text( 'alias', newline = '' )
    ( root / 'index.html' ).write_text( 'index', newline = '' )
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
    tracks = website.validate_track_configuration( {
        'stable': FrozenDictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
        'docs-2': FrozenDictionary( {
            'tag-namespace': 'docs-*',
            'selector': 'exact-tag',
            'alias': 'docs-2',
        } ),
    } )  # type: ignore[arg-type]
    import hashlib
    snapshot = {
        path.relative_to( root ).as_posix( ): hashlib.sha256(
            path.read_bytes( ) ).hexdigest( )
        for path in sorted( root.rglob( '*' ) ) if path.is_file( ) }
    website.verify_retained_history( locations, snapshot, 'v2.0', tracks )
    ( root / 'v1.0/guide.html' ).write_text( 'tampered', newline = '' )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.verify_retained_history(
            locations, snapshot, 'v2.0', tracks )
    ( root / 'v1.0/guide.html' ).write_text( 'old', newline = '' )
    ( root / 'stable/guide.html' ).write_text( 'recopied', newline = '' )
    ( root / 'index.html' ).write_text( 'rerendered', newline = '' )
    website.verify_retained_history( locations, snapshot, 'v2.0', tracks )


def test_098_provenance_validates_release_tag( website, provide_tempdir ):
    ''' Strict provenance requires HEAD to match the release tag. '''
    import shutil
    import subprocess

    from frigid import Dictionary as FrozenDictionary
    executable = shutil.which( 'git' )
    assert executable is not None
    project = Path( provide_tempdir ) / 'tagrepo'
    project.mkdir( parents = True, exist_ok = True )
    ( project / 'site' ).mkdir( parents = True, exist_ok = True )
    def git( *args ):
        return subprocess.run(  # noqa: S603
            [ executable, *args ], cwd = project, check = True,
            capture_output = True, text = True,
            env = _git_environment( ) )
    git( 'init' )
    git( 'config', 'user.email', 'test@example.com' )
    git( 'config', 'user.name', 'Test' )
    git( 'config', 'commit.gpgsign', 'false' )
    git( 'config', 'tag.gpgsign', 'false' )
    git( 'config', 'commit.gpgsign', 'false' )
    git( 'config', 'tag.gpgsign', 'false' )
    ( project / 'seed.txt' ).write_text( 'seed', newline = '' )
    git( 'add', 'seed.txt' )
    git( 'commit', '-m', 'base' )
    git( 'tag', 'v9.9' )
    locations = website.Locations(
        project = project,
        auxiliary = project / '.auxiliary',
        publications = project / '.auxiliary/publications',
        archive = project / 'website.tar.xz',
        artifacts = project / '.auxiliary/artifacts',
        website = project / 'site',
        coverage = project / 'site/coverage.svg',
        index = project / 'site/index.html',
        versions = project / 'site/versions.json',
        templates = project / 'templates' )
    locations.website.mkdir( parents = True, exist_ok = True )
    tracks = website.validate_track_configuration( {
        'stable': FrozenDictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
    } )  # type: ignore[arg-type]
    website.record_provenance(
        locations, '9.9', tracks, strict = True )
    ( project / 'other.txt' ).write_text( 'other', newline = '' )
    git( 'add', 'other.txt' )
    git( 'commit', '-m', 'advance' )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.record_provenance(
            locations, '9.9', tracks, strict = True )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.record_provenance(
            locations, '0.0', tracks, strict = True )


def test_103_inventory_failure_retains_previous_tree(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Failed inventory validation restores previous good tree. '''
    test_files = {
        'project/.auxiliary/artifacts/sphinx-html/guide.html':
            '<html><body><a id="guide"></a></body></html>',
        'package/data/templates/coverage.svg.jinja': '{{ color }}',
        'package/data/templates/website.html.jinja': '{{ latest_version }}',
    }
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project )
        baseline = (
            locations_tmpdir.website / 'v1.0/sphinx-html/guide.html'
        ).read_text( )
        inventory = _write_inventory_case(
            provide_tempdir,
            [ ( 'v1.0/sphinx-html/guide.html', '0' * 64, ( ), 'frozen' ) ] )
        with pytest.raises( website.PublicationSourceInvalidity ):
            website.update(
                auxdata_tmpdir, 'v1.0',
                project_anchor = locations_tmpdir.project,
                legacy_inventory = inventory )
        assert (
            locations_tmpdir.website / 'v1.0/sphinx-html/guide.html'
        ).read_text( ) == baseline


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
            capture_output = True, text = True,
            env = _git_environment( ) )
    subprocess.run(  # noqa: S603
        [ executable, 'init', '--bare', str( remote ) ],
        check = True, capture_output = True,
        env = _git_environment( ) )
    git( 'init' )
    git( 'config', 'user.email', 'test@example.com' )
    git( 'config', 'user.name', 'Test' )
    git( 'config', 'commit.gpgsign', 'false' )
    git( 'config', 'tag.gpgsign', 'false' )
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
    baseline = website.fetch_publication_branch_and_tarball( locations )
    assert baseline == ''
    # Confirmed absence clears stale state; build regenerates the archive.
    archive.write_bytes( b'archive-a' )
    website.update_publication_branch( locations, 'v1', baseline )
    published_a = git( 'rev-parse', 'publication' ).stdout.strip( )
    proceeding = git(
        'commit-tree', 'HEAD^{tree}', '-p', 'publication',
        '-m', 'writer B' ).stdout.strip( )
    git( 'push', 'origin', proceeding + ':publication' )
    with pytest.raises( subprocess.CalledProcessError ):
        website.update_publication_branch(
            locations, 'v1-stale', published_a )
    remote_head = subprocess.run(  # noqa: S603
        [ executable, '--git-dir', str( remote ),
          'rev-parse', 'publication' ],
        check = True, capture_output = True, text = True,
        env = _git_environment( ) ).stdout.strip( )
    assert remote_head == proceeding
    website.update_publication_branch( locations, 'v1-fresh', proceeding )
    remote_head = subprocess.run(  # noqa: S603
        [ executable, '--git-dir', str( remote ),
          'rev-parse', 'publication' ],
        check = True, capture_output = True, text = True,
        env = _git_environment( ) ).stdout.strip( )
    assert remote_head != proceeding


def test_104_annotated_tag_peels_to_commit( website, provide_tempdir ):
    ''' Annotated tags resolve by commit identity, branches never do. '''
    from frigid import Dictionary as FrozenDictionary
    project, git = _make_git_repo( provide_tempdir, 'tagrepo2' )
    site = project / 'site'
    site.mkdir( parents = True, exist_ok = True )
    ( project / 'seed.txt' ).write_text( 'seed', newline = '' )
    git( 'add', 'seed.txt' )
    git( 'commit', '-m', 'base' )
    git( 'tag', '-a', '-m', 'release', 'v9.8' )
    git( 'branch', 'wobbly' )
    locations = website.Locations(
        project = project,
        auxiliary = project / '.auxiliary',
        publications = project / '.auxiliary/publications',
        archive = project / 'website.tar.xz',
        artifacts = project / '.auxiliary/artifacts',
        website = site,
        coverage = site / 'coverage.svg',
        index = site / 'index.html',
        versions = site / 'versions.json',
        templates = project / 'templates' )
    tracks = website.validate_track_configuration( {
        'stable': FrozenDictionary( {
            'tag-namespace': 'v*',
            'selector': 'latest-final',
            'alias': 'stable',
        } ),
    } )  # type: ignore[arg-type]
    website.record_provenance(
        locations, '9.8', tracks, strict = True )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.record_provenance(
            locations, 'wobbly', tracks, strict = True )


def test_105_absence_clears_stale_local_state( website, provide_tempdir ):
    ''' Confirmed absence clears stale archive and publication ancestry. '''
    project, git = _make_git_repo( provide_tempdir, 'absentrepo' )
    ( project / 'seed.txt' ).write_text( 'seed', newline = '' )
    git( 'add', 'seed.txt' )
    git( 'commit', '-m', 'base' )
    archive = project / '.auxiliary/publications/website.tar.xz'
    archive.parent.mkdir( parents = True, exist_ok = True )
    archive.write_bytes( b'stale-local' )
    git( 'branch', 'publication' )
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
    assert website.fetch_publication_branch_and_tarball( locations ) == ''
    assert not archive.exists( )
    import shutil
    import subprocess
    executable = shutil.which( 'git' )
    assert executable is not None
    probe = subprocess.run(  # noqa: S603
        [ executable, 'show-ref', '--verify', '--quiet',
          'refs/heads/publication' ],
        cwd = project, check = False, capture_output = True,
        env = _git_environment( ) )
    assert probe.returncode != 0


def test_106_concurrent_creation_fails_without_loss(
    website, provide_tempdir
):
    ''' Race-created remote branch defeats plain absent-lease push. '''
    import shutil
    import subprocess
    executable = shutil.which( 'git' )
    assert executable is not None
    project, git = _make_git_repo( provide_tempdir, 'racerrepo' )
    remote = Path( provide_tempdir ) / 'remote-race.git'
    subprocess.run(  # noqa: S603
        [ executable, 'init', '--bare', str( remote ) ],
        check = True, capture_output = True,
        env = _git_environment( ) )
    git( 'remote', 'add', 'origin', str( remote ) )
    ( project / 'seed.txt' ).write_text( 'seed', newline = '' )
    git( 'add', 'seed.txt' )
    git( 'commit', '-m', 'base' )
    archive = project / '.auxiliary/publications/website.tar.xz'
    archive.parent.mkdir( parents = True, exist_ok = True )
    archive.write_bytes( b'archive-a' )
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
    assert website.fetch_publication_branch_and_tarball( locations ) == ''
    # Confirmed absence clears stale state; build regenerates the archive.
    archive.write_bytes( b'archive-a' )
    tree = git( 'rev-parse', 'HEAD:' ).stdout.strip( )
    proceeding = git(
        'commit-tree', tree, '-m', 'writer B' ).stdout.strip( )
    git( 'push', 'origin', proceeding + ':refs/heads/publication' )
    with pytest.raises( subprocess.CalledProcessError ) as excuse:
        website.update_publication_branch( locations, 'v1', '' )
    assert 'push' in str( excuse.value.cmd )
    local_head = git( 'rev-parse', 'publication' ).stdout.strip( )
    assert local_head != proceeding
    remote_head = subprocess.run(  # noqa: S603
        [ executable, '--git-dir', str( remote ),
          'rev-parse', 'publication' ],
        check = True, capture_output = True, text = True,
        env = _git_environment( ) ).stdout.strip( )
    assert remote_head == proceeding


def test_109_absence_without_race_publishes_cleanly(
    website, provide_tempdir
):
    ''' Confirmed absence with no race creates the remote branch. '''
    project, git = _make_git_repo( provide_tempdir, 'cleanrepo' )
    ( project / 'seed.txt' ).write_text( 'seed', newline = '' )
    git( 'add', 'seed.txt' )
    git( 'commit', '-m', 'base' )
    import shutil
    import subprocess
    executable = shutil.which( 'git' )
    assert executable is not None
    remote = Path( provide_tempdir ) / 'remote-clean.git'
    subprocess.run(  # noqa: S603
        [ executable, 'init', '--bare', str( remote ) ],
        check = True, capture_output = True,
        env = _git_environment( ) )
    git( 'remote', 'add', 'origin', str( remote ) )
    archive = project / '.auxiliary/publications/website.tar.xz'
    archive.parent.mkdir( parents = True, exist_ok = True )
    archive.write_bytes( b'archive-a' )
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
    assert website.fetch_publication_branch_and_tarball( locations ) == ''
    archive.write_bytes( b'archive-a' )
    website.update_publication_branch( locations, 'v1', '' )
    remote_head = subprocess.run(  # noqa: S603
        [ executable, '--git-dir', str( remote ),
          'rev-parse', 'publication' ],
        check = True, capture_output = True, text = True,
        env = _git_environment( ) ).stdout.strip( )
    local_head = git( 'rev-parse', 'publication' ).stdout.strip( )
    assert remote_head == local_head


def test_110_cleanup_failures_abort_before_build( website, provide_tempdir ):
    ''' Irremovable stale archive or ancestry aborts the fetch. '''
    project, git = _make_git_repo( provide_tempdir, 'stubbornrepo' )
    ( project / 'seed.txt' ).write_text( 'seed', newline = '' )
    git( 'add', 'seed.txt' )
    git( 'commit', '-m', 'base' )
    archive = project / '.auxiliary/publications/website.tar.xz'
    archive.parent.mkdir( parents = True, exist_ok = True )
    archive.mkdir( exist_ok = True )
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
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.fetch_publication_branch_and_tarball( locations )
    archive.rmdir( )
    archive.write_bytes( b'stale-local' )
    git( 'branch', 'publication' )
    git( 'checkout', 'publication' )
    with pytest.raises( website.PublicationSourceInvalidity ):
        website.fetch_publication_branch_and_tarball( locations )


def test_107_reject_alias_overwriting_retained_release(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Alias pointed at another retained release aborts. '''
    from frigid import Dictionary as FrozenDictionary
    test_files = {
        'project/.auxiliary/artifacts/sphinx-html/guide.html':
            '<html><body></body></html>',
        'package/data/templates/coverage.svg.jinja': '{{ color }}',
        'package/data/templates/website.html.jinja': '{{ latest_version }}',
    }
    honest = website.validate_track_configuration( {
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
        'v1': FrozenDictionary( {
            'tag-namespace': 'v1.*',
            'selector': 'latest-final',
            'alias': 'v1',
        } ),
    } )  # type: ignore[arg-type]
    rogue = website.validate_track_configuration( {
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
        'evil': FrozenDictionary( {
            'tag-namespace': 'v11',
            'selector': 'exact-tag',
            'alias': 'v10',
        } ),
    } )  # type: ignore[arg-type]
    inventory = _write_inventory_case(
        provide_tempdir,
        [ ( 'stable/sphinx-html/guide.html', '', ( ), 'follow' ) ] )
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project,
            tracks = honest,
            legacy_inventory = inventory )
        website.update(
            auxdata_tmpdir, 'v10',
            project_anchor = locations_tmpdir.project,
            tracks = honest,
            legacy_inventory = inventory )
        with pytest.raises( website.PublicationSourceInvalidity ):
            website.update(
                auxdata_tmpdir, 'v11',
                project_anchor = locations_tmpdir.project,
                tracks = rogue,
                legacy_inventory = inventory )


def test_108_changed_republish_refused_idempotent_passes(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Changed same-version content aborts; identical rerun passes. '''
    from pathlib import Path

    from frigid import Dictionary as FrozenDictionary
    test_files = {
        'project/.auxiliary/artifacts/sphinx-html/guide.html':
            '<html><body>one</body></html>',
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
        'v1': FrozenDictionary( {
            'tag-namespace': 'v1.*',
            'selector': 'latest-final',
            'alias': 'v1',
        } ),
    } )  # type: ignore[arg-type]
    inventory = _write_inventory_case(
        provide_tempdir,
        [ ( 'stable/sphinx-html/guide.html', '', ( ), 'follow' ),
          ( 'v1.0/sphinx-html/guide.html', '', ( ), 'follow' ),
          ( 'v1/sphinx-html/guide.html', '', ( ), 'follow' ) ] )
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project,
            tracks = tracks,
            legacy_inventory = inventory )
        website.update(
            auxdata_tmpdir, 'v1.1',
            project_anchor = locations_tmpdir.project,
            tracks = tracks,
            legacy_inventory = inventory )
        website.update(
            auxdata_tmpdir, 'v1.1',
            project_anchor = locations_tmpdir.project,
            tracks = tracks,
            legacy_inventory = inventory )
        guide = (
            Path( provide_tempdir )
            / 'project/.auxiliary/artifacts/sphinx-html/guide.html' )
        guide.write_text( '<html><body>two</body></html>', newline = '' )
        with pytest.raises( website.PublicationSourceInvalidity ):
            website.update(
                auxdata_tmpdir, 'v1.1',
                project_anchor = locations_tmpdir.project,
                tracks = tracks,
                legacy_inventory = inventory )


def test_111_retained_history_without_inventory(
    auxdata_tmpdir, locations_tmpdir, website, provide_tempdir
):
    ''' Retained history enforced without any inventory input. '''
    test_files = {
        'project/.auxiliary/artifacts/sphinx-html/guide.html':
            '<html><body>one</body></html>',
        'package/data/templates/coverage.svg.jinja': '{{ color }}',
        'package/data/templates/website.html.jinja': '{{ latest_version }}',
    }
    with create_test_files( provide_tempdir, test_files ):
        locations_tmpdir.website.mkdir( parents = True, exist_ok = True )
        website.update(
            auxdata_tmpdir, 'v1.0',
            project_anchor = locations_tmpdir.project )
        guide = (
            Path( provide_tempdir )
            / 'project/.auxiliary/artifacts/sphinx-html/guide.html' )
        guide.write_text( '<html><body>two</body></html>', newline = '' )
        with pytest.raises( website.PublicationSourceInvalidity ):
            website.update(
                auxdata_tmpdir, 'v1.0',
                project_anchor = locations_tmpdir.project )
        guide.write_text( '<html><body>one</body></html>', newline = '' )
        website.update(
            auxdata_tmpdir, 'v1.1',
            project_anchor = locations_tmpdir.project )
