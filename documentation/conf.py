# vim: set filetype=python fileencoding=utf-8:
# -*- mode: python ; coding: utf-8 -*-

''' Configuration file for the Sphinx documentation builder.

    This file only contains a selection of the most common options.
    For a full list, see the documentation:
        https://www.sphinx-doc.org/en/master/usage/configuration.html
    Also, see this nice article on Sphinx customization:
        https://jareddillard.com/blog/common-ways-to-customize-sphinx-themes.html
'''


def _calculate_copyright_notice( ):
    from datetime import datetime as DateTime, timezone as TimeZone
    first_year = 2024
    now_year = DateTime.now( TimeZone.utc ).year
    if first_year < now_year: year_range = f"{first_year}-{now_year}"
    else: year_range = str( first_year )
    return f"{year_range}, Eric McDonald"


def _import_version( ):
    from importlib import import_module
    from pathlib import Path
    from sys import path
    project_location = Path( __file__ ).parent.parent
    path.insert( 0, str( project_location / 'sources' ) )
    module = import_module( 'emcdproj' )
    return module.__version__


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'python-project-common'
author = 'Eric McDonald'
copyright = ( # noqa: A001
    _calculate_copyright_notice( ) )
release = version = _import_version( )

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.graphviz',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_inline_tabs',
]

templates_path = [ '_templates' ]

exclude_patterns = [ ]

rst_prolog = f'''
.. |project| replace:: {project}
'''

nitpicky = True
nitpick_ignore = [
    # Workaround for https://bugs.python.org/issue11975
    # Found on Stack Overflow (credit to Astropy project):
    #   https://stackoverflow.com/a/30624034
    ( 'py:class', "D[k] if k in D, else d.  d defaults to None." ),
    ( 'py:class', "None.  Remove all items from D." ),
    ( 'py:class', "a set-like object providing a view on D's items" ),
    ( 'py:class', "a set-like object providing a view on D's keys" ),
    ( 'py:class', "an object providing a view on D's values" ),
    ( 'py:class', "functools.partial" ),
    ( 'py:class', "mappingproxy" ),
    ( 'py:class', "module" ),
    ( 'py:class',
      "v, remove specified key and return the corresponding value." ),
    # Type annotation weirdnesses.
    ( 'py:class', "Doc" ),
    ( 'py:class', "Positional" ),
    ( 'py:class', "absence.objects.AbsentSingleton" ),
    ( 'py:class', "emcdproj.__.state.Globals" ),
    ( 'py:class', "frigid.classes.Class" ),
    ( 'py:class', "frigid.classes.Dataclass" ),
    ( 'py:class', "frigid.classes.ProtocolDataclass" ),
    ( 'py:class', "platformdirs.unix.Unix" ),
    ( 'py:class', "types.Annotated" ),
    ( 'py:class', "typing_extensions.Any" ),
    ( 'py:class', "typing_extensions.Self" ),
    ( 'py:class', "typing_extensions.TypeIs" ),
    ( 'py:class', "tyro.conf._markers.CallableType" ),
]
nitpick_ignore_regex = [
    ( 'py:class', r'''.*\.Annotated\[.*?\]''' ),
]

# -- Options for linkcheck builder -------------------------------------------

linkcheck_ignore = [
    # Circular dependency between building HTML and publishing it.
    r'https://emcd\.github\.io/python-project-common/.*',
    # Stack Overflow rate limits too aggressively, which breaks matrix builds.
    r'https://stackoverflow\.com/help/.*',
    # Repository does not exist during initial development.
    r'https://github\.com/emcd/python-project-common',
    r'https://github\.com/emcd/python-project-common/.*',
    # Package does not exist during initial development.
    r'https://pypi.org/project/emcdproj/',
    # Github aggressively rate-limits access to certain blobs.
    r'https://github\.com/.*/.*/blob/.*',
    # Avoid timeouts for slow sites.
    r'http://www\.catb\.org/~esr/faqs/smart-questions\.html',
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.
# https://github.com/pradyunsg/furo
html_theme = 'furo'
html_theme_options = {
    'navigation_with_keys': True,
    'sidebar_hide_name': True,
}

html_static_path = [ '_static' ]

# -- Options for autodoc extension -------------------------------------------

autodoc_default_options = {
    'member-order': 'groupwise',
    'members': True,
    'show-inheritance': True,
    # 'special-members': '__call__',
}

autodoc_typehints = 'none'
autodoc_use_type_comments = False

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    'python': (
        'https://docs.python.org/3', None),
    'typing-extensions': (
        'https://typing-extensions.readthedocs.io/en/latest', None),
  # --- BEGIN: Injected by Copier ---
    'absence': (
        'https://emcd.github.io/python-absence/stable/sphinx-html', None),
    'dynadoc': (
        'https://emcd.github.io/python-dynadoc/stable/sphinx-html', None),
    'frigid': (
        'https://emcd.github.io/python-frigid/stable/sphinx-html', None),
  # --- END: Injected by Copier ---
}

# -- Options for Myst extension ----------------------------------------------

# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    # 'amsmath',
    # 'attrs_inline',
    'colon_fence',      # ::: blocks
    'deflist',          # Definition lists
    # 'dollarmath',
    # 'fieldlist',
    # 'html_admonition',
    # 'html_image',
    # 'linkify',
    # 'replacements',
    # 'smartquotes',
    # 'strikethrough',
    # 'substitution',
    'tasklist',         # - [ ] tasks
]

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True
