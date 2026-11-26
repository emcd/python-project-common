## MODIFIED Requirements

### Requirement: Multi-Platform CI/CD
The template SHALL provide reusable GitHub Actions workflows for cross-platform
testing, documentation generation, and reporting. Reusable workflow
references are version-pinned per family (`gha-1`); contract additions
that change no shared interface reuse existing pins.

#### Scenario: Cross-platform test execution
- **WHEN** code is pushed to branches included in the workflow configuration
- **THEN** the CI/CD workflow executes tests across the configured Python
  versions (from the project's selected subset of supported Python
  versions, currently 3.12-3.15) on Linux,
  macOS, and Windows

#### Scenario: Reusable workflow composition
- **WHEN** a generated project is configured
- **THEN** cross-repository workflows (xrepo--*) provide standardized
  testing, reporting, documentation, and packaging automation that
  downstream projects can reference

#### Scenario: Contract addition without family cut
- **WHEN** a template change adds generated-code behavior without
  changing any shared reusable-workflow input or output
- **THEN** existing family pins are retained and no new family is cut;
  flag-off renders remain behavior-identical
