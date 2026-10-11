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


''' Static website maintenance utilities for projects. '''


from .. import __
from .. import exceptions as _exceptions
from .. import interfaces as _interfaces
from ..exceptions import (
    PublicationSourceInvalidity,
    TrackConfigurationInvalidity,
)
from .inventory import (
    _extract_element_ids,
    _validate_legacy_inventory,
    _verify_retained_history,
)
from .locations import Locations
from .publication import (
    _copy_version_to_alias,
    _extract_coverage,
    _fetch_publication_branch_and_tarball,
    _record_provenance,
    _reject_symlinks_in_tree,
    _safe_extractall,
    _update_available_species,
    _update_coverage_badge,
    _update_index_html,
    _update_publication_branch,
    _update_version_coverage_badge,
    _update_versions_json,
    _validate_version_label,
    survey,
    update,
)
from .tracks import (
    TrackConfiguration,
    TrackMap,
    _DEFAULT_TRACKS,
    _load_default_configuration,
    load_track_configuration,
    matches_namespace,
    validate_track_configuration,
)


class SurveyCommand(
    _interfaces.CliCommand, decorators = ( __.standard_tyro_class, ),
):
    ''' Surveys release versions published in static website. '''

    use_extant: __.typx.Annotated[
        bool,
        __.typx.Doc( ''' Fetch publication branch and use tarball. ''' ),
    ] = False

    async def __call__(
        self, auxdata: __.Globals, display: _interfaces.ConsoleDisplay
    ) -> None:
        survey( auxdata, use_extant = self.use_extant )


class UpdateCommand(
    _interfaces.CliCommand, decorators = ( __.standard_tyro_class, ),
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
        self, auxdata: __.Globals, display: _interfaces.ConsoleDisplay
    ) -> None:
        configuration: __.Absential[ __.Path | str ] = __.absent
        if self.configuration:
            configuration = self.configuration
        inventory: __.Absential[ __.Path ] = __.absent
        if self.legacy_inventory:
            inventory = __.Path( self.legacy_inventory )
        update(
            auxdata, self.version,
            use_extant = self.use_extant,
            production = self.production,
            configuration = configuration,
            legacy_inventory = inventory )


class CommandDispatcher(
    _interfaces.CliCommand, decorators = ( __.standard_tyro_class, ),
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
        self, auxdata: __.Globals, display: _interfaces.ConsoleDisplay
    ) -> None:
        ictr( 1 )( self.command )
        await self.command( auxdata = auxdata, display = display )
