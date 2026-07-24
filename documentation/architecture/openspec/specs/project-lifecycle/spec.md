# Project Lifecycle Management

## Purpose

This specification defines the behavioral contracts for the Python Project
Common system: Copier template generation, reusable GitHub Actions workflows,
and the emcd-projects maintenance package. It captures still-current
configuration-sensitive capabilities rather than aspirational product goals.

Capabilities are described relative to template configuration. Not all
features are active in every generated project; behavior depends on the
Copier answers selected during project creation.

## Requirements

### Requirement: Project Bootstrapping
The template SHALL enable developers to create configured Python projects with
sources, tests, documentation, and packaging tooling through Copier prompts.

#### Scenario: Generate a new project from template
- **WHEN** a developer provides project configuration via Copier prompts
- **THEN** the system generates a project structure including sources/, tests/,
  documentation/, pyproject.toml, and quality assurance tool configuration

#### Scenario: Hatch build backend selection
- **WHEN** a developer generates a project without Rust extension support
- **THEN** the generated project uses Hatch as the PEP 517 build backend

#### Scenario: Maturin build backend selection
- **WHEN** a developer enables Rust extension support during generation
- **THEN** the generated project uses Maturin as the PEP 517 build backend
  with PyO3 integration

#### Scenario: Optional feature selection
- **WHEN** a developer enables optional features (CLI, Rust extensions,
  property testing, executables, data resources) during generation
- **THEN** the generated project includes the selected features with
  appropriate configuration and scaffolding

#### Scenario: Standalone executable generation
- **WHEN** a developer enables CLI and executable support
- **THEN** the generated project includes PyInstaller configuration for
  building standalone executables on Linux, macOS (arm64 and x86_64),
  and Windows

### Requirement: Quality Validation
The template SHALL configure quality validation tooling (Ruff, Pyright, isort,
pytest) in generated projects. Pre-commit and pre-push hooks are available
for installation but are not enforced by default; merge policy is a
repository-level concern outside the template's scope.

#### Scenario: Generated project configures quality tools
- **WHEN** a generated project is created from the template
- **THEN** it includes configuration for linting (Ruff), type checking
  (Pyright), import sorting (isort), and test execution (pytest) without
  manual setup

#### Scenario: Validation via CI/CD workflows
- **WHEN** code is pushed to branches included in the CI workflow
  configuration
- **THEN** the CI/CD workflow executes the configured quality validation
  suite

#### Scenario: Hook-based local validation
- **WHEN** a developer installs the generated pre-commit and pre-push hooks
- **THEN** local commits and pushes are validated against the configured
  quality checks before reaching the repository

### Requirement: Self-Contained Documentation
The template SHALL configure Sphinx-based documentation infrastructure in
generated projects. Documentation and reports are portable to static hosting;
no specialized documentation or reporting SaaS (such as ReadTheDocs or Codecov)
is required.

#### Scenario: Documentation site generation
- **WHEN** a maintainer builds documentation for a generated project
- **THEN** Sphinx generates documentation with API references and
  cross-linked navigation from the project's own documentation sources

#### Scenario: Coverage badge generation
- **WHEN** test coverage data is available from CI/CD execution
- **THEN** the maintenance package generates coverage badges without
  requiring Codecov or similar external reporting services

### Requirement: Multi-Platform CI/CD
The template SHALL provide reusable GitHub Actions workflows for cross-platform
testing, documentation generation, and reporting.

#### Scenario: Cross-platform test execution
- **WHEN** code is pushed to branches included in the workflow configuration
- **THEN** the CI/CD workflow executes tests across the configured Python
  versions (from the project's selected subset of 3.10-3.14) on Linux,
  macOS, and Windows

#### Scenario: Reusable workflow composition
- **WHEN** a generated project is configured
- **THEN** cross-repository workflows (xrepo--*) provide standardized
  testing, reporting, documentation, and packaging automation that
  downstream projects can reference

### Requirement: Release Automation
The template SHALL provide a release workflow that builds distributions and
conditionally publishes them. Publication behavior depends on template
configuration and tag/package version alignment.

#### Scenario: Tag-triggered release with publication enabled
- **WHEN** `enable_publication` is true and a version tag matching the
  package version is pushed
- **THEN** the release workflow builds wheel and sdist distributions,
  publishes to PyPI via trusted publishing, creates a GitHub release with
  attestations, and generates release notes from changelog fragments

#### Scenario: Tag-triggered release with publication disabled
- **WHEN** `enable_publication` is false and a version tag is pushed
- **THEN** the release workflow builds distributions and runs quality gates
  but does not publish to PyPI or create a GitHub release

#### Scenario: Version mismatch safety gate
- **WHEN** a tag version does not match the built package version
- **THEN** the release workflow skips PyPI and GitHub release publication

#### Scenario: Prerelease handling
- **WHEN** `enable_publication` is true, a matching prerelease tag (alpha,
  beta, rc) is pushed, and release creation is eligible
- **THEN** the release workflow marks the GitHub release as prerelease and
  sets `--latest=false`

#### Scenario: Release security
- **WHEN** a release is published
- **THEN** the workflow uses OIDC trusted publishing (no stored API keys),
  generates artifact attestations, and produces SHA256 integrity checksums

### Requirement: Static Website Management
The maintenance package SHALL provide static site tooling for documentation and
coverage reporting. Output is portable to static hosting platforms (such as
GitHub Pages); no specialized documentation or reporting SaaS is required.

#### Scenario: Site update with versioned content
- **WHEN** a maintainer invokes the site update command after a release
- **THEN** the package updates the static site with versioned documentation,
  coverage reports, and badge images, maintaining stable and development
  aliases

### Requirement: Template Synchronization
The template SHALL enable projects to be updated when the template evolves,
using Copier's update mechanism.

#### Scenario: Template update with conflict resolution
- **WHEN** a maintainer runs copier update on an existing project
- **THEN** Copier applies template changes and reports conflicts for files
  that were modified locally, requiring manual resolution

#### Scenario: Template validation
- **WHEN** a maintainer runs template validation
- **THEN** the system renders the template with default and maximum
  configurations and runs quality checks against the generated output
