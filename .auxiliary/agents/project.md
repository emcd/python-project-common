# Project Guidance

Project-owned knowledge the generated `AGENTS.md` entrypoint must not own.
Structured tracking stays in `nb`.

## Purpose

The project addresses the complete lifecycle of Python projects, from
creation to maintenance. It provides:

1. A Copier-based template for rapid scaffolding of new Python projects
   with consistent structure and configuration.
2. A Python package (`emcdproj`) for ongoing project maintenance,
   including static site generation and badge management.
3. A collection of reusable GitHub Actions workflows for CI/CD,
   testing, and documentation.

## Tech Stack

- Language: Python (>= 3.12)
- Project Management: Hatch
- Templating: Copier
- Documentation: Sphinx, `myst-parser`
- Testing: Pytest, coverage
- Linting/Formatting/Static Analysis: Ruff, Pyright, isort, Vulture
- CLI: Tyro
- CI/CD: GitHub Actions

## Notes

<!-- Accumulate project-specific knowledge, constraints, deviations, and durable
     links here. For structured items, use `nb`.

     TODO: If this project uses multiple agent/worktree roles, create a stable
     team-organization note in `nb`, modeled after one of the examples at:
     https://raw.githubusercontent.com/emcd/agents-common/master/examples/nb-notes/team-organization/README.md
     Then link the note here, for example:
     - Team org, role ownership, signoff policy, and merge workflow: `coordination/general/<n>` -->
