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


''' Filesystem operations and utilities. '''


from . import __


@__.ctxl.contextmanager
def chdir( directory: __.Path ) -> __.cabc.Iterator[ __.Path ]:
    ''' Temporarily changes working directory.

        Not thread-safe or async-safe.
    '''
    # TODO: Python 3.11: contextlib.chdir
    original = __.os.getcwd( )
    __.os.chdir( directory )
    try: yield directory
    finally: __.os.chdir( original )
