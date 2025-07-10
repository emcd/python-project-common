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


''' Family of exceptions for package API. '''


from . import __


class Omniexception( __.immut.Object, BaseException ):
    ''' Base for all exceptions raised by package API. '''
    # TODO: Class and instance attribute concealment.

    _attribute_visibility_includes_: __.cabc.Collection[ str ] = (
        frozenset( ( '__cause__', '__context__', ) ) )


class Omnierror( Omniexception, Exception ):
    ''' Base for error exceptions raised by package API. '''


class DataAwol( Omnierror, AssertionError ):
    ''' Unexpected data absence. '''

    def __init__( self, source: str, label: str ):
        super( ).__init__(
            f"Necessary data with label '{label}' is missing from {source}." )


class FileDataAwol( DataAwol ):
    ''' Unexpected data absence from file. '''

    def __init__( self, file: str | __.Path, label: str ):
        super( ).__init__( source = f"file '{file}'", label = label )


class FileAwol( Omnierror, AssertionError ):
    ''' Unexpected file absence. '''

    def __init__( self, file: str | __.Path ):
        super( ).__init__( f"Necessary file is missing at '{file}'." )


class FileEmpty( Omnierror, AssertionError ):
    ''' Unexpectedly empty file. '''

    def __init__( self, file: str| __.Path ):
        super( ).__init__( f"Unexpectedly empty file at '{file}'." )
