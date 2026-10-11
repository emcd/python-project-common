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


''' Static website maintenance utilities for projects. '''


from ..exceptions import (
    PublicationSourceInvalidity,
    TrackConfigurationInvalidity,
)
from .cli import CommandDispatcher, SurveyCommand, UpdateCommand
from .inventory import (
    extract_element_ids,
    validate_legacy_inventory,
    verify_retained_history,
)
from .locations import Locations
from .publication import (
    copy_version_to_alias,
    extract_coverage,
    fetch_publication_branch_and_tarball,
    record_provenance,
    reject_symlinks_in_tree,
    safe_extractall,
    update_available_species,
    update_coverage_badge,
    update_index_html,
    update_publication_branch,
    update_version_coverage_badge,
    update_versions_json,
    validate_version_label,
    survey,
    update,
)
from .tracks import (
    TrackConfiguration,
    TrackMap,
    DEFAULT_TRACKS,
    load_default_configuration,
    load_track_configuration,
    matches_namespace,
    validate_track_configuration,
)
