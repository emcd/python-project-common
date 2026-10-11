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


''' Publication filesystem locations. '''


from . import __


class Locations( __.immut.DataclassObject ):
    ''' Locations associated with website maintenance. '''

    project: __.Path
    auxiliary: __.Path
    publications: __.Path
    archive: __.Path
    artifacts: __.Path
    website: __.Path
    coverage: __.Path
    index: __.Path
    versions: __.Path
    templates: __.Path

    @classmethod
    def from_project_anchor(
        selfclass,
        auxdata: __.Globals,
        anchor: __.Absential[ __.Path ] = __.absent,
    ) -> __.typx.Self:
        ''' Produces locations from project anchor, if provided.

            If project anchor is not given, then attempt to discover it.
        '''
        if __.is_absent( anchor ):
            # TODO: Discover missing anchor via directory traversal,
            #       seeking VCS markers.
            project = __.Path( ).resolve( strict = True )
        else: project = anchor.resolve( strict = True )
        auxiliary = project / '.auxiliary'
        publications = auxiliary / 'publications'
        templates = auxdata.distribution.provide_data_location( 'templates' )
        return selfclass(
            project = project,
            auxiliary = auxiliary,
            publications = publications,
            archive = publications / 'website.tar.xz',
            artifacts = auxiliary / 'artifacts',
            website = auxiliary / 'artifacts/website',
            coverage = auxiliary / 'artifacts/website/coverage.svg',
            index = auxiliary / 'artifacts/website/index.html',
            versions = auxiliary / 'artifacts/website/versions.json',
            templates = templates )
