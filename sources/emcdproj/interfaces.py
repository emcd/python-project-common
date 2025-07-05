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


''' Abstract bases and interfaces. '''


from . import __


class DisplayStreams( __.enum.Enum ): # TODO: Python 3.11: StrEnum
    # TODO: Protected class attributes.
    ''' Stream upon which to place output. '''

    Stderr =    'stderr'
    Stdout =    'stdout'


class ConsoleDisplay( __.immut.DataclassObject ):
    silence: __.typx.Annotated[
        bool,
        __.tyro.conf.arg(
            aliases = ( '--quiet', '--silent', ), prefix_name = False ),
    ] = False
    file: __.typx.Annotated[
        __.typx.Optional[ __.Path ],
        __.tyro.conf.arg(
            name = 'console-capture-file', prefix_name = False ),
    ] = None
    stream: __.typx.Annotated[
        DisplayStreams,
        __.tyro.conf.arg( name = 'console-stream', prefix_name = False ),
    ] = DisplayStreams.Stderr

    async def provide_stream( self ) -> __.io.TextIOWrapper:
        ''' Provides output stream for display. '''
        # TODO: register file stream as a process-lifetime exit
        if self.file: return open( self.file, 'w' )
        # TODO: async context manager for async file streams
        # TODO: return async stream - need async printers
        # TODO: handle non-TextIOWrapper streams
        match self.stream:
            case DisplayStreams.Stdout:
                return __.sys.stdout # pyright: ignore[reportReturnType]
            case DisplayStreams.Stderr:
                return __.sys.stderr # pyright: ignore[reportReturnType]


class CliCommand(
    __.immut.DataclassProtocol, __.typx.Protocol,
    decorators = ( __.typx.runtime_checkable, ),
):
    ''' CLI command. '''

    @__.abc.abstractmethod
    async def __call__(
        self, auxdata: __.Globals, display: ConsoleDisplay
    ) -> None:
        ''' Executes command with global state. '''
        raise NotImplementedError

    # TODO: provide_configuration_edits
