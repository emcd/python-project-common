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


from . import __
from . import interfaces as _interfaces
from . import template as _template
from . import website as _website


class VersionCommand(
    _interfaces.CliCommand,
    decorators = ( __.standard_tyro_class, ),
):
    ''' Prints version information. '''

    async def __call__(
        self, auxdata: __.Globals, display: _interfaces.ConsoleDisplay
    ) -> None:
        from . import __version__
        print( f"{__package__} {__version__}" )
        raise SystemExit( 0 )


class Cli(
    __.immut.DataclassObject,
    decorators = ( __.simple_tyro_class, ),
):
    ''' Various utilities for projects by Github user '@emcd'. '''

    # configfile: __.typx.Optional[ str ] = None
    display: _interfaces.ConsoleDisplay
    command: __.typx.Union[
        __.typx.Annotated[
            _template.CommandDispatcher,
            __.tyro.conf.subcommand( 'template', prefix_name = False ),
        ],
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
            await self.command( auxdata = auxdata, display = self.display )

    def prepare_invocation_args(
        self,
    ) -> __.cabc.Mapping[ str, __.typx.Any ]:
        ''' Prepares arguments for initial configuration. '''
        args: dict[ str, __.typx.Any ] = dict(
            environment = True,
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
    except BaseException as exc:
        print( exc, file = __.sys.stderr )
        raise SystemExit( 1 ) from None


async def _prepare(
    environment: bool,
    exits: __.ctxl.AsyncExitStack,
) -> __.Globals:
    ''' Configures logging based on verbosity. '''
    import ictruck
    # TODO: Finetune Icecream truck installation from CLI arguments.
    ictruck.install( trace_levels = 9 )
    return await __.appcore.prepare(
        environment = environment, exits = exits )
