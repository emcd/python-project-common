Excerpts from "Deprecating Python Package 📦🔚", which was originally about
sunsetting `emcd/python-lockup` but turned into a conversation about extracting
useful parts from `emcd/python-devshim`, upon which `python-lockup` depends.

---

**User**



Thanks! This is a decent start. I suspect that we will need to work on plumbing
the equivalent of PEP 508 environment markers from Hatch to its environment
management extensions. Let's forgo further discussion on this topic for now.
I've recorded this portion of our conversation into an ideas file in
`../python-project-common` so that we can reference it in a later conversation.

Let's shift focus to the release automation process that we discussed earlier.
If we could replace some of the steps in the `releases.rst` document with more
automation for creating releases, like we have in `python-devshim`, then that
would be great. In the Invoke tasks, I called `git` directly. However, I am
wondering if we could/should use something like `dulwich` or a package which
wraps a Git library and call that from a helper script, which could also be
invoked as an entrypoint via Hatch. What do you think?

---

**Assistant**


Using a Git library like `dulwich` or `GitPython` would give us several
advantages over direct `git` commands:

1. **Better Error Handling**: Instead of parsing command output and exit codes,
   we get proper Python exceptions and return values
2. **Type Safety**: With type hints, we can make the operations more reliable
   and self-documenting
3. **Cross-Platform**: Libraries handle platform-specific details better than
   raw commands
4. **Testing**: We can mock Git operations in tests more easily

Looking at the release steps from `releases.rst`, here's a potential approach
using `dulwich` (which is pure Python and has no external dependencies):

```python
#!/usr/bin/env python3

'''Git operations for release management.'''

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Optional

from dulwich.porcelain import (
    branch_create, push, status, tag_create,
    branch_list, current_branch
)
from dulwich.repo import Repo


class ReleaseStage(Enum):
    '''Release stage transitions.'''
    ALPHA_TO_RC = auto()
    RC_TO_RELEASE = auto()
    RELEASE_TO_PATCH = auto()


@dataclass
class ReleaseContext:
    '''Context for release operations.'''
    repo: Repo
    version: str
    remote: str = 'origin'
    branch: Optional[str] = None

    @classmethod
    def from_path(cls, path: Path, **kwargs) -> 'ReleaseContext':
        '''Creates context from repository path.'''
        return cls(Repo(str(path)), **kwargs)

    @property
    def current_branch(self) -> str:
        '''Returns current branch name.'''
        return current_branch(self.repo).decode('utf-8')


def create_release_branch(ctx: ReleaseContext, major: int, minor: int) -> None:
    '''Creates a new release branch.'''
    branch_name = f'release-{major}.{minor}'

    # Ensure we're on master
    if ctx.current_branch != 'master':
        raise ValueError('Must be on master branch')

    # Check working directory is clean
    changes = status(ctx.repo)
    if any(changes):
        raise ValueError('Working directory not clean')

    # Create and checkout branch
    branch_create(ctx.repo, branch_name)

    # Push branch with tracking
    push(ctx.repo, ctx.remote, branch_name)


def tag_version(ctx: ReleaseContext, version: str, message: str) -> None:
    '''Creates and pushes a version tag.'''
    tag_name = f'v{version}'
    tag_create(ctx.repo, tag_name, message=message.encode('utf-8'))
    push(ctx.repo, ctx.remote, tag_name)


def ensure_main_branch(ctx: ReleaseContext) -> None:
    '''Ensures we're on the main development branch.'''
    if ctx.current_branch != 'master':
        raise ValueError('Must be on master branch')


if __name__ == '__main__':
    import click

    @click.group()
    @click.option('--repo-path', type=Path, default=Path.cwd())
    @click.pass_context
    def cli(ctx, repo_path: Path):
        '''Release management operations.'''
        ctx.obj = ReleaseContext.from_path(repo_path)

    @cli.command()
    @click.argument('major', type=int)
    @click.argument('minor', type=int)
    @click.pass_obj
    def create_branch(ctx: ReleaseContext, major: int, minor: int):
        '''Creates a new release branch.'''
        create_release_branch(ctx, major, minor)

    @cli.command()
    @click.argument('version')
    @click.argument('message')
    @click.pass_obj
    def tag(ctx: ReleaseContext, version: str, message: str):
        '''Creates and pushes a version tag.'''
        tag_version(ctx, version, message)

    cli()
```

We could integrate this with Hatch in two ways:

1. As a script in the environment:
```toml
[tool.hatch.envs.release]
dependencies = ["dulwich", "click"]
scripts = {
    "branch" = "python .auxiliary/scripts/release.py create-branch",
    "tag" = "python .auxiliary/scripts/release.py tag"
}
```

2. As an entry point:
```toml
[project.scripts]
project-release = "project.release:cli"
```

The script could handle:
1. Branch creation and validation
2. Version tagging
3. Ensuring clean working directory
4. Remote operations

Benefits of this approach:
1. Testable Git operations
2. Better error messages
3. Type safety
4. Platform independence
5. No shell execution

Would you like me to:
1. Expand the script to cover more release operations?
2. Add error handling for specific Git scenarios?
3. Create tests for the Git operations?

---

**User**



This is a good start. Feedback:
- We use Tyro rather than Click for building CLIs.
- Would like to capture the Towncrier creation of the changelog. I don't think
  Towncrier has an API though, though we may need to use `subprocess` with the
  CLI.
- What do you think about post-release cherry-picks of the updated changelog
  and removal of Towncrier fragments back to `master` branch?

---

**Assistant**


Thanks for the feedback. Let me address each point:

1. **Tyro Instead of Click**:
Yes, Tyro provides better type safety and dataclass integration. Here's how we
could revise the CLI:

```python
from dataclasses import dataclass
from typing import Optional

from tyro import cli


@dataclass
class CreateBranchCommand:
    '''Creates a new release branch.'''
    major: int
    minor: int
    remote: str = 'origin'


@dataclass
class TagCommand:
    '''Creates and pushes a version tag.'''
    version: str
    message: str
    remote: str = 'origin'


@dataclass
class ReleaseCommands:
    '''Release management operations.'''
    command: CreateBranchCommand | TagCommand


def main() -> None:
    '''CLI entry point.'''
    cli(ReleaseCommands)
```

2. **Towncrier Integration**:
Yes, we'd need to use subprocess for Towncrier. We could wrap it in a clean
interface:

```python
from pathlib import Path
from subprocess import run, CalledProcessError
from typing import Optional

class ChangelogManager:
    '''Manages changelog generation and cleanup.'''

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.fragments_dir = project_root / 'documentation' / 'towncrier'

    def generate_changelog(self, version: str, keep_fragments: bool = True) -> str:
        '''Generates changelog for version.

        Returns the generated content for use in release notes.
        '''
        try:
            result = run(
                ['towncrier', 'build', '--version', version] +
                (['--keep'] if keep_fragments else []),
                capture_output=True,
                text=True,
                check=True,
                cwd=self.project_root
            )
            return result.stdout
        except CalledProcessError as e:
            raise RuntimeError(f"Changelog generation failed: {e.stderr}") from e

    def cleanup_fragments(self) -> None:
        '''Removes all changelog fragments.'''
        for fragment in self.fragments_dir.glob('*.rst'):
            fragment.unlink()
```

3. **Cherry-picking to Master**:
We could handle the post-release operations like this:

```python
from dulwich.porcelain import (
    cherry_pick, checkout, reset_hard,
    commit_staged, add
)

class PostReleaseManager:
    '''Manages post-release operations.'''

    def __init__(self, repo: Repo, changelog_manager: ChangelogManager):
        self.repo = repo
        self.changelog_manager = changelog_manager

    def sync_changelog_to_master(self, release_branch: str) -> None:
        '''Cherry-picks changelog changes to master.'''
        current = current_branch(self.repo)

        try:
            # Get the changelog commit from release branch
            changelog_commit = self._find_changelog_commit(release_branch)

            # Switch to master
            checkout(self.repo, b'master')

            # Cherry-pick the changelog commit
            cherry_pick(self.repo, changelog_commit)

            # Clean up fragments
            self.changelog_manager.cleanup_fragments()

            # Commit cleanup
            add(self.repo, 'documentation/towncrier/*.rst')
            commit_staged(self.repo, b'Clean up changelog fragments')

        finally:
            # Return to original branch
            checkout(self.repo, current)

    def _find_changelog_commit(self, branch: str) -> str:
        '''Finds the commit that updated the changelog.'''
        # Implementation to find the relevant commit
        # Could use commit message pattern matching
        ...
```

A complete release workflow might look like:

```python
class ReleaseManager:
    '''Manages the complete release process.'''

    def __init__(
        self,
        repo_path: Path,
        remote: str = 'origin'
    ):
        self.repo = Repo(str(repo_path))
        self.remote = remote
        self.changelog_manager = ChangelogManager(repo_path)
        self.post_release = PostReleaseManager(self.repo, self.changelog_manager)

    def create_release(self, version: str) -> None:
        '''Executes full release process.'''
        # Generate changelog
        changelog = self.changelog_manager.generate_changelog(version)

        # Create tag with changelog as message
        tag_version(self.repo, version, changelog)

        # Push changes
        push(self.repo, self.remote)

        # Sync changelog to master
        self.post_release.sync_changelog_to_master(current_branch(self.repo))

        # Push master
        checkout(self.repo, b'master')
        push(self.repo, self.remote)
```

This gives us:
1. Type-safe CLI with Tyro
2. Encapsulated Towncrier operations
3. Automated post-release cleanup and syncing
4. Clean abstractions for Git operations

Would you like me to:
1. Add error handling for specific scenarios (merge conflicts, dirty working
   directory)?
2. Add validation for version numbers and branch names?
3. Create tests for these operations?
4. Expand the changelog management to handle different types of releases (RC,
   patch)?
