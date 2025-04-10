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


''' Command-line interface. '''


from __future__ import annotations

from . import __
from . import interfaces as _interfaces
from . import website as _website


class VersionCommand(
    _interfaces.CliCommand,
    decorators = ( __.standard_tyro_class, ),
):
    ''' Prints version information. '''

    async def __call__( self, auxdata: __.Globals ) -> None:
        from . import __version__
        print( f"{__package__} {__version__}" )
        raise SystemExit( 0 )


class Cli(
    metaclass = __.ImmutableDataclass,
    decorators = ( __.simple_tyro_class, ),
):
    ''' Various utilities for projects by Github user '@emcd'. '''

    application: __.ApplicationInformation
    # configfile: __.typx.Optional[ str ] = None
    # display: ConsoleDisplay
    command: __.typx.Union[
        __.typx.Annotated[
            _website.CommandDispatcher,
            __.tyro.conf.subcommand( 'website', prefix_name = False ),
        ],
        __.typx.Annotated[
            VersionCommand,
            __.tyro.conf.subcommand( 'version', prefix_name = False ),
        ],
    ]

    async def __call__( self ):
        ''' Invokes command after library preparation. '''
        nomargs = self.prepare_invocation_args( )
        async with __.ctxl.AsyncExitStack( ) as exits:
            auxdata = await _prepare( exits = exits, **nomargs )
            ictr( 0 )( self.command )
            await self.command( auxdata = auxdata )
            # await self.command( auxdata = auxdata, display = self.display )

    def prepare_invocation_args(
        self,
    ) -> __.cabc.Mapping[ str, __.typx.Any ]:
        ''' Prepares arguments for initial configuration. '''
        # configedits: __.DictionaryEdits = (
        #     self.command.provide_configuration_edits( ) )
        args: dict[ str, __.typx.Any ] = dict(
            application = self.application,
            # configedits = configedits,
            # environment = True,
        )
        # if self.configfile: args[ 'configfile' ] = self.configfile
        return args


def execute( ) -> None:
    ''' Entrypoint for CLI execution. '''
    from asyncio import run
    config = (
        __.tyro.conf.HelptextFromCommentsOff,
    )
    try: run( __.tyro.cli( Cli, config = config )( ) )
    except SystemExit: raise
    except BaseException:
        # TODO: Log exception.
        raise SystemExit( 1 ) from None


async def _prepare(
    application: __.ApplicationInformation,
    # configedits: __.DictionaryEdits,
    # environment: bool,
    exits: __.ctxl.AsyncExitStack,
) -> __.Globals:
    ''' Configures logging based on verbosity. '''
    import ictruck
    # TODO: Finetune Icecream truck installation from CLI arguments.
    ictruck.install( trace_levels = 9 )
    return await __.prepare(
        application = application,
        # configedits = configedits,
        # environment = environment,
        exits = exits )
