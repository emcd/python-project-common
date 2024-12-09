# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

''' Extra configuration for Sphinx documentation builder. '''


linkcheck_ignore = [
    # Circular dependency between building HTML and publishing it.
    r'https://emcd\.github\.io/python-project-common/.*',
    # Stack Overflow rate limits too aggressively, which breaks matrix builds.
    r'https://stackoverflow\.com/help/.*',
    # Repository does not exist during initial development.
    r'https://github\.com/emcd/python-project-common',
    r'https://github\.com/emcd/python-project-common/.*',
    # Package does not exist during initial development.
    r'https://pypi.org/project/emcd_projects/',
]
