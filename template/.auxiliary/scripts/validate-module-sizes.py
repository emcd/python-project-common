#!/usr/bin/env python3
"""Enforce maximum Python module size to preserve readability.

Restores the Pylint C0302 (max-module-lines) enforcement lost in the
Pylint-to-Ruff migration. Modules exceeding the limit must be split
into a same-named subpackage that preserves the original interface:
move the module contents into the package directory and re-export
the public names from its __init__.py. See the subpackage pattern
in the Python architecture guide:
https://emcd.github.io/documentation-common/v1/sphinx-html/common/architecture-python.html#the-subpackage-pattern
"""

import sys as _sys
from pathlib import Path as _Path

_LIMIT = 1000
_SCOPE = ( 'sources', 'tests' )


def find_oversize_modules(
    root: _Path, limit: int = _LIMIT,
) -> list[ tuple[ _Path, int ] ]:
    ''' Returns (path, line count) for Python modules over the limit. '''
    oversize: list[ tuple[ _Path, int ] ] = [ ]
    for scope in _SCOPE:
        base = root / scope
        if not base.is_dir( ):
            continue
        for path in sorted( base.rglob( '*.py' ) ):
            with path.open( encoding = 'utf-8' ) as f:
                count = sum( 1 for _ in f )
            if count > limit:
                oversize.append( ( path, count ) )
    return oversize


def main( ) -> None:
    ''' Fails if any module exceeds the line limit. '''
    oversize = find_oversize_modules( _Path.cwd( ) )
    if not oversize:
        print( f'All modules within {_LIMIT} lines.' )
        return
    for path, count in oversize:
        print(
            f'{path}: {count} lines exceeds the {_LIMIT}-line limit. '
            f'Split it into a same-named subpackage, re-exporting '
            f'the public names from __init__.py so imports keep '
            f'working: '
            f'https://emcd.github.io/documentation-common/v1/'
            f'sphinx-html/common/architecture-python.html'
            f'#the-subpackage-pattern' )
    _sys.exit( 1 )


if __name__ == '__main__':
    main( )
