# Project Context

## Purpose

The project addresses the complete lifecycle of Python projects, from creation to maintenance. It provides:

1.  **Project Template**: A Copier-based template for rapid scaffolding of new Python projects with consistent structure and configuration.
2.  **Runtime Management**: A Python package (`emcdproj`) for ongoing project maintenance, including static site generation and badge management.
3.  **Automation**: A collection of reusable GitHub Actions workflows for CI/CD, testing, and documentation.

The goal is to facilitate a "single-maintainer model" while supporting community contributions, ensuring separation of concerns between template generation, workflow automation, and maintenance tooling.

## Tech Stack

-   **Language**: Python (>= 3.10)
-   **Project Management**: Hatch (build backend, environment management)
-   **Templating**: Copier, Jinja2
-   **Documentation**: Sphinx, myst-parser
-   **Testing**: Pytest, coverage
-   **Linting/Formatting**: Ruff, Pyright, isort, Vulture
-   **CLI**: Tyro
-   **CI/CD**: GitHub Actions
-   **Utilities**: `defusedxml`, `icecream-truck`, `absence`, `accretive`, `frigid`, `classcore`

## Project Conventions

### Filesystem Organization

The project follows a specific filesystem organization documented in:
-   `documentation/architecture/filesystem.rst`

This document details the root directory structure, source code organization (including the `__` subpackage pattern), template system structure, and component integration.

### Code Style

-   **Formatting**: Enforced by Ruff and isort. Line length is set to 79 characters.
-   **Typing**: Strict static typing checked by Pyright.
-   **Lints**: Comprehensive linting via Ruff and Vulture (dead code detection).

### Architecture Patterns

-   **Three-Tier Architecture**: The project is structured into three distinct tiers (Template Generation, CI/CD Automation, Project Maintenance) as detailed in:
    -   `documentation/architecture/decisions/001-three-tier-architecture.rst`
-   **Centralized Import Pattern**: A double underscore (`__`) subpackage pattern is used for centralized import management to prevent namespace pollution and duplications. Details in:
    -   `documentation/architecture/decisions/002-centralized-import-pattern.rst`
-   **CLI Structure**: The CLI uses `tyro` and separates command definition (`cli.py`, `website.py`) from the entry point (`__main__.py`).

### Testing Strategy

Testing follows the principles outlined in:
-   `documentation/architecture/testplans/summary.rst`

Key aspects include:
-   **Coverage**: High coverage requirements (near 100%) for core logic.
-   **Cross-platform**: Testing across multiple Python versions and operating systems via GitHub Actions.
-   **Types**: Doctests are run via Sphinx; unit tests via Pytest.

### Git Workflow

-   **Branching**:
    -   `master` (or `main`): Primary development branch.
    -   `publication`: Dedicated branch for hosting the versioned static website (documentation + coverage reports).
-   **Workflows**:
    -   `tester`: Runs on push/PR to verify code and tests.
    -   `docsgen`: Generates documentation.
    -   `linters`: Checks code style and static analysis.
    -   `packagers`: Builds the distribution packages.

## Domain Context

-   **emcdproj**: The CLI tool included in the project. It handles tasks like `website update` to manage the static documentation site, ensuring versioned docs and coverage badges are up-to-date without relying on external services like ReadTheDocs.
-   **Template Processing**: The `template/` directory contains the source for the Copier template. It mirrors the generated project structure but uses Jinja2 for customization.
-   **Auxiliary Workspace**: The `.auxiliary/` directory is used for local development artifacts, caches, and tool configurations, keeping the root clean.

## Important Constraints

-   **Single-Maintainer Focus**: The architecture is designed to minimize overhead for a single maintainer while still allowing for community input.
-   **No External Doc Hosting Services**: The project explicitly avoids services like ReadTheDocs or Codecov in favor of a self-managed static site on GitHub Pages (via the `publication` branch).

## External Dependencies

-   **GitHub Actions**: Heavily relied upon for all automation (testing, publishing, etc.).
-   **PyPI**: Target for package distribution.
-   **Copier**: Required for using and updating the project template.
