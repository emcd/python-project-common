Excerpts from "Deprecating Python Package 📦🔚", which was originally about
sunsetting `emcd/python-lockup` but turned into a conversation about extracting
useful parts from `emcd/python-devshim`, upon which `python-lockup` depends.

---

**User**



Before we make a proof-of-concept, please read
`../python-devshim/.github/workflows/reusable--updater.yaml` for reference.
(However, note that it uses a monolithic lock file `pypackages.fixtures.toml`.
This was a design mistake on my part; we definitely want separate per-platform,
per-version files. Part of the trick is to determine what constitutes a
separate platform... OS + Python implementation?)

---

**Assistant**



Yes, regarding platform differentiation, we should consider:

1. **Primary Platform Factors**:
   - Operating System (Linux, macOS, Windows)
   - Python Implementation (CPython, PyPy)
   - Python Version (3.10, 3.11, etc.)

2. **Secondary Factors** that might affect dependencies:
   - Architecture (x86_64, aarch64)
   - Libc version (for Linux)
   - ABI compatibility (especially for PyPy)

For a first iteration, I suggest:

```
.auxiliary/requirements/
├── linux
│   ├── cpython
│   │   ├── 3.10.txt
│   │   ├── 3.11.txt
│   │   └── 3.12.txt
│   └── pypy
│       └── 3.10.txt
├── macos
│   └── cpython
│       ├── 3.10.txt
│       ├── 3.11.txt
│       └── 3.12.txt
└── windows
    └── cpython
        ├── 3.10.txt
        ├── 3.11.txt
        └── 3.12.txt
```

Key improvements over devshim's approach:
1. Separate files instead of monolithic TOML
2. Platform-specific organization
3. Implementation-specific organization
4. Clear file naming convention

The workflow would:
1. Use matrix strategy to generate each combination
2. Generate lock files using pip-compile
3. Create PR with changes (like devshim)
4. Add metadata comments in lock files about:
   - Generation timestamp
   - Platform details (OS, arch, libc)
   - Python implementation details

Would you like me to create a proof-of-concept workflow with this structure?

---

**User**



Thanks of for the proposal. I am somewhat against deep hierarchies, especially
as there may be multiple good ways to classify things. I would prefer a single
directory where the files have various segments (some possibly optional),
separated by `--`, in their names. I definitely agree with you about the
secondary factors; please read
`../python-devshim/sources/python3/devshim/platforms/identity.py` to see some
of the ones that I consider in various parts of Devshim. (There is also the
matter that CPython can be compiled with "tracerefs" support, which makes an
incompatible ABI since `PyObject_t` gains extra fields for memory tracing. And,
as of CPython 3.13, there is also an option to build a GIL-free, multithreaded
interpreter; this also breaks the ABI.)

---

**Assistant**




Yes, this shows many more platform considerations, including:
- CPU architecture (with normalization needs, e.g., aarch64/arm64)
- OS class (POSIX vs NT)
- Kernel details (name, address size)
- Python implementation specifics (tracerefs, PyPy version)
- System ABI (libc version, Windows version)

You're right about avoiding deep hierarchies. Let's use a flat structure with
descriptive filenames. Here's a revised naming scheme for
`.auxiliary/requirements/`:

```
requirements--{os}--{cpu}--{impl}-{version}[--{extra}].txt

Examples:
requirements--linux--x86_64--cpython-3.10.txt
requirements--linux--x86_64--cpython-3.10--tracerefs.txt
requirements--linux--aarch64--cpython-3.11.txt
requirements--linux--x86_64--pypy-3.10--pypy-7.3.txt
requirements--windows--x86_64--cpython-3.12.txt
requirements--macos--arm64--cpython-3.13.txt
```

The segments would be:
1. `os`: linux, windows, macos
2. `cpu`: x86_64, arm64, etc.
3. `impl-version`: cpython-3.10, pypy-3.10, etc.
4. `extra`: (optional) tracerefs, nogil, pypy version, etc.

The workflow would:
1. Use matrix strategy for primary factors (os, python-version)
2. Detect secondary factors during runtime
3. Generate appropriate filename based on all factors
4. Use pip-compile to create lock file
5. Add metadata header comments about:
   ```
   # Generated at: 2024-01-20 12:00:00 UTC
   # Platform: linux-x86_64 (kernel: 5.15.0, libc: glibc-2.31)
   # Python: CPython 3.10.4 (tracerefs)
   ```

Would you like me to create a proof-of-concept workflow with this naming
scheme?

---

**User**



Sure, that would be great. Ideally, we would use the Hatch integration with
`pip-compile`:
```
[tool.hatch.env]
requires = [
    "hatch-pip-compile"
]

[tool.hatch.envs.default]
type = "pip-compile"
```
```
[tool.hatch.envs.default]
type = "pip-compile"
```
For more configuration examples, please read
`https://raw.githubusercontent.com/juftin/hatch-pip-compile/refs/heads/main/docs/examples.md`.

---

**Assistant**




Great, this gives us good insight into hatch-pip-compile's capabilities. Let me
create a proof-of-concept that combines Hatch's pip-compile integration with
our platform-aware workflow.

Here's the proposed setup:

1. First, update pyproject.toml to add hatch-pip-compile:
```toml
[tool.hatch.env]
requires = ["hatch-pip-compile"]

[tool.hatch.envs.default]
type = "pip-compile"
pip-compile-hashes = true
pip-compile-resolver = "uv"  # Faster resolver
lock-filename = ".auxiliary/requirements/requirements--{platform_tag}.txt"

[tool.hatch.envs.qa]
type = "pip-compile"
inherit = ["default"]
[[tool.hatch.envs.qa.matrix]]
python = ["3.10", "3.11", "3.12", "3.13", "pypy3.10"]
```

2. Create the updater workflow:
```yaml
name: updater

on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  workflow_dispatch: {}

jobs:
  initialize:
    uses: ./.github/workflows/core--initializer.yaml

  update-deps:
    needs: [initialize]
    strategy:
      matrix:
        platform: ${{ fromJSON(needs.initialize.outputs.platforms) }}
        python-version: ${{ fromJSON(needs.initialize.outputs.python-versions) }}
        exclude: ${{ fromJSON(needs.initialize.outputs.matrix-exclusions) }}
    runs-on: ${{ matrix.platform }}
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install Hatch
        run: pip install hatch

      - name: Detect Platform Details
        id: platform
        run: |
          # Python script to detect platform details
          python -c '
          from platform import machine, system, libc_ver
          import sys

          os_name = system().lower()
          cpu = machine().lower()

          # Detect Python implementation details
          impl = sys.implementation.name
          version = ".".join(map(str, sys.version_info[:2]))
          extras = []

          if hasattr(sys, "getobjects"):
              extras.append("tracerefs")

          if impl == "pypy":
              pypy_ver = ".".join(map(str, sys.pypy_version_info[:2]))
              extras.append(f"pypy-{pypy_ver}")

          # Build platform tag
          platform_parts = [os_name, cpu, f"{impl}-{version}"]
          if extras:
              platform_parts.append("--".join(extras))

          platform_tag = "--".join(platform_parts)
          print(f"platform_tag={platform_tag}")
          ' >> $GITHUB_OUTPUT

      - name: Generate Lock File
        run: |
          hatch env create qa.py${{ matrix.python-version }}
          # The environment creation will trigger pip-compile with our platform-specific filename

      - name: Add Metadata Header
        run: |
          LOCK_FILE=".auxiliary/requirements/requirements--${{ steps.platform.outputs.platform_tag }}.txt"
          TMP_FILE="${LOCK_FILE}.tmp"

          # Create header
          cat > "${TMP_FILE}" << EOF
          # Generated at: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
          # Platform: ${{ steps.platform.outputs.platform_tag }}
          # Python: $(python -V)

          EOF

          # Append existing content
          cat "${LOCK_FILE}" >> "${TMP_FILE}"
          mv "${TMP_FILE}" "${LOCK_FILE}"

      - name: Upload Lock File
        uses: actions/upload-artifact@v4
        with:
          name: requirements-${{ steps.platform.outputs.platform_tag }}
          path: .auxiliary/requirements/requirements--${{ steps.platform.outputs.platform_tag }}.txt

  create-pr:
    needs: [update-deps]
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Download Lock Files
        uses: actions/download-artifact@v4
        with:
          pattern: requirements-*
          path: .auxiliary/requirements/
          merge-multiple: true

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v6
        with:
          title: '[GHA] Update dependency lock files'
          commit-message: '[GHA] Update dependency lock files'
          branch: gha-dependency-update
          delete-branch: true
```

Key features:
1. Uses Hatch's pip-compile integration for lock file generation
2. Detects platform details including:
   - OS and CPU architecture
   - Python implementation and version
   - Special features (tracerefs, PyPy version)
3. Adds metadata headers to lock files
4. Creates PR with all updated lock files

Would you like me to adjust any part of this approach?

---

**User**


Looks like a good first draft. Some feedback:
- I'm not sure how you get Hatch to honor `platform_tag` in the lock filename.
- Instead of executing a large inline Python script with `python -c`, why not
  make a separate Python source file, which we can test manually? Then, the
  step simply becomes `hatch --env <envname> run python <path-to-script>`.
- No need for the `Setup Python` or `Install Hatch` steps. GHA workflow runners
  have Python installed by default and Hatch acquires specific versions for
  virtual environments as needed. We have a separate action to setup in
  `../python-project-common/.github/actions/python-hatch/action.yaml`.

---

**Assistant**


Thanks for the feedback. Let me address each point:

1. You're right about the lock filename - looking at the hatch-pip-compile docs
   again, it doesn't support dynamic variables like that. We'll need to handle
   the file naming ourselves.

2. Good point about the Python script. Let's create
   `.auxiliary/scripts/platform_identity.py`:

```python
#!/usr/bin/env python3

'''Identifies platform characteristics for dependency locking.'''

from platform import machine, system, libc_ver
import sys
from typing import List


def get_platform_tag() -> str:
    '''Returns platform tag for dependency lock file naming.'''
    os_name = system().lower()
    cpu = machine().lower()

    # Detect Python implementation details
    impl = sys.implementation.name
    version = '.'.join(map(str, sys.version_info[:2]))
    extras = get_implementation_extras()

    # Build platform tag
    platform_parts = [os_name, cpu, f'{impl}-{version}']
    if extras:
        platform_parts.append('--'.join(extras))

    return '--'.join(platform_parts)


def get_implementation_extras() -> List[str]:
    '''Returns list of implementation-specific extra tags.'''
    extras = []

    if hasattr(sys, 'getobjects'):
        extras.append('tracerefs')

    if sys.implementation.name == 'pypy':
        pypy_ver = '.'.join(map(str, sys.pypy_version_info[:2]))
        extras.append(f'pypy-{pypy_ver}')

    return extras


if __name__ == '__main__':
    print(f'platform_tag={get_platform_tag()}')
```

3. Here's the revised workflow using the python-hatch action:

```yaml
name: updater

on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  workflow_dispatch: {}

jobs:
  initialize:
    uses: ./.github/workflows/core--initializer.yaml

  update-deps:
    needs: [initialize]
    strategy:
      matrix:
        platform: ${{ fromJSON(needs.initialize.outputs.platforms) }}
        python-version: ${{ fromJSON(needs.initialize.outputs.python-versions) }}
        exclude: ${{ fromJSON(needs.initialize.outputs.matrix-exclusions) }}
    runs-on: ${{ matrix.platform }}
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Prepare Python
        uses: emcd/python-project-common/.github/actions/python-hatch@v1.5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Detect Platform Details
        id: platform
        run: hatch run python .auxiliary/scripts/platform_identity.py >> $GITHUB_OUTPUT

      - name: Generate Lock File
        run: |
          # Generate requirements file with pip-compile
          hatch env create qa.py${{ matrix.python-version }}

          # Move to platform-specific name
          mkdir -p .auxiliary/requirements
          mv requirements.txt ".auxiliary/requirements/requirements--${{ steps.platform.outputs.platform_tag }}.txt"

      - name: Add Metadata Header
        run: |
          LOCK_FILE=".auxiliary/requirements/requirements--${{ steps.platform.outputs.platform_tag }}.txt"
          TMP_FILE="${LOCK_FILE}.tmp"

          # Create header
          cat > "${TMP_FILE}" << EOF
          # Generated at: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
          # Platform: ${{ steps.platform.outputs.platform_tag }}
          # Python: $(python -V)

          EOF

          # Append existing content
          cat "${LOCK_FILE}" >> "${TMP_FILE}"
          mv "${TMP_FILE}" "${LOCK_FILE}"

      - name: Upload Lock File
        uses: actions/upload-artifact@v4
        with:
          name: requirements-${{ steps.platform.outputs.platform_tag }}
          path: .auxiliary/requirements/requirements--${{ steps.platform.outputs.platform_tag }}.txt

  create-pr:
    needs: [update-deps]
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Download Lock Files
        uses: actions/download-artifact@v4
        with:
          pattern: requirements-*
          path: .auxiliary/requirements/
          merge-multiple: true

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v6
        with:
          title: '[GHA] Update dependency lock files'
          commit-message: '[GHA] Update dependency lock files'
          branch: gha-dependency-update
          delete-branch: true
```

Would you like me to make any other adjustments? For example:
1. Add more platform details to the identity script?
2. Add tests for the platform identity script?
3. Modify how we handle the lock file generation and renaming?

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
