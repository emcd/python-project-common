# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");          #
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


''' Command-line interface for website maintenance. '''


from . import __
from .publication import survey as _survey
from .publication import update as _update


class SurveyCommand(
    __.interfaces.CliCommand, decorators = ( __.standard_tyro_class, ),
):
    ''' Surveys release versions published in static website. '''

    use_extant: __.typx.Annotated[
        bool,
        __.typx.Doc( ''' Fetch publication branch and use tarball. ''' ),
    ] = False

    async def __call__(
        self, auxdata: __.Globals, display: __.interfaces.ConsoleDisplay
    ) -> None:
        _survey( auxdata, use_extant = self.use_extant )


class UpdateCommand(
    __.interfaces.CliCommand, decorators = ( __.standard_tyro_class, ),
):
    ''' Updates static website for particular release version. '''

    version: __.typx.Annotated[
        str,
        __.typx.Doc( ''' Release version to update. ''' ),
        __.tyro.conf.Positional,
    ]

    use_extant: __.typx.Annotated[
        bool,
        __.typx.Doc( ''' Fetch publication branch and use tarball. ''' ),
    ] = False

    production: __.typx.Annotated[
        bool,
        __.typx.Doc( ''' Update publication branch with new tarball.
                     Implies --use-extant to prevent data loss. ''' ),
    ] = False

    configuration: __.typx.Annotated[
        str,
        __.typx.Doc( ''' Track configuration TOML file for publication. ''' ),
    ] = ''

    legacy_inventory: __.typx.Annotated[
        str,
        __.typx.Doc( ''' Legacy-link inventory TOML file for validation. ''' ),
    ] = ''

    async def __call__(
        self, auxdata: __.Globals, display: __.interfaces.ConsoleDisplay
    ) -> None:
        configuration: __.Absential[ __.Path | str ] = __.absent
        if self.configuration:
            configuration = self.configuration
        inventory: __.Absential[ __.Path ] = __.absent
        if self.legacy_inventory:
            inventory = __.Path( self.legacy_inventory )
        _update(
            auxdata, self.version,
            use_extant = self.use_extant,
            production = self.production,
            configuration = configuration,
            legacy_inventory = inventory )


class CommandDispatcher(
    __.interfaces.CliCommand, decorators = ( __.standard_tyro_class, ),
):
    ''' Dispatches commands for static website maintenance. '''

    command: __.typx.Union[
        __.typx.Annotated[
            SurveyCommand,
            __.tyro.conf.subcommand( 'survey', prefix_name = False ),
        ],
        __.typx.Annotated[
            UpdateCommand,
            __.tyro.conf.subcommand( 'update', prefix_name = False ),
        ],
    ]

    async def __call__(
        self, auxdata: __.Globals, display: __.interfaces.ConsoleDisplay
    ) -> None:
        ictr( 1 )( self.command )
        await self.command( auxdata = auxdata, display = display )
