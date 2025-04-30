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


''' Copier template maintenance and validation. '''


from __future__ import annotations

import subprocess as _subprocess
import tempfile as _tempfile

from . import __
from . import interfaces as _interfaces


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
            ValidateCommand,
            __.tyro.conf.subcommand( 'validate', prefix_name = False ),
        ],
    ]

    async def __call__(
        self, auxdata: __.Globals, display: _interfaces.ConsoleDisplay
    ) -> None:
        ictr( 1 )( self.command )
        await self.command( auxdata = auxdata, display = display )


class SurveyCommand(
    _interfaces.CliCommand, decorators = ( __.standard_tyro_class, ),
):
    ''' Surveys available configuration variants. '''

    async def __call__(
        self, auxdata: __.Globals, display: _interfaces.ConsoleDisplay
    ) -> None:
        stream = await display.provide_stream( )
        for variant in survey_variants( auxdata ):
            print( variant, file = stream )


class ValidateCommand(
    _interfaces.CliCommand, decorators = ( __.standard_tyro_class, ),
):
    ''' Validates template against configuration variant. '''

    variant: __.typx.Annotated[
        str,
        __.typx.Doc( ''' Configuration variant to validate. ''' ),
        __.tyro.conf.Positional,
    ]

    async def __call__(
        self, auxdata: __.Globals, display: _interfaces.ConsoleDisplay
    ) -> None:
        ''' Copies new project from template for configuration variant. '''
        # TODO: Validate variant argument.
        validate_variant( auxdata, self.variant )


def copy_template( answers_file: __.Path, projectdir: __.Path ) -> None:
    ''' Copies template to target directory using answers. '''
    _subprocess.run( # noqa: S603
        (   'copier', 'copy', '--data-file', str( answers_file ),
            '--defaults', '--overwrite', '--vcs-ref', 'HEAD',
            '.', str( projectdir ) ),
        cwd = __.Path( ), check = True )


def survey_variants( auxdata: __.Globals ) -> __.cabc.Sequence[ str ]:
    ''' Surveys available configuration variants. '''
    location = auxdata.distribution.provide_data_location( 'copier' )
    return tuple(
        fsent.stem.lstrip( 'answers-' )
        for fsent in location.glob( 'answers-*.yaml' )
        if fsent.is_file( ) )


def validate_variant( auxdata: __.Globals, variant: str ) -> None:
    ''' Validates configuration variant. '''
    answers_file = (
        auxdata.distribution.provide_data_location(
            'copier', f"answers-{variant}.yaml" ) )
    if not answers_file.is_file( ):
        # TODO: Raise error.
        return
    with _tempfile.TemporaryDirectory( ) as tmpdir:
        projectdir = __.Path( tmpdir ) / variant
        copy_template( answers_file, projectdir )
        validate_variant_project( projectdir )


def validate_variant_project( projectdir: __.Path ) -> None:
    ''' Validates standard project as generated from template. '''
    for command in (
        (   'hatch', '--env', 'develop', 'run',
            'python', '-m', 'pip', 'install',
            '--upgrade', 'pip', 'build' ),
        (   'hatch', '--env', 'develop', 'run', 'make-all' ),
    ): _subprocess.run( command, cwd = str( projectdir ), check = True ) # noqa: S603
