# Custom Slash Command Ideas

Collection of potential custom slash commands to implement based on focused role specialization.

## Core Specialized Role Commands

### Requirements and Planning
- `cs-manage-prd` - **IMPLEMENTED** - Manage product requirements documents and feature planning
- `cs-analyze-requirements` - Analyze and validate existing requirements for completeness
- `cs-trace-requirements` - Map requirements to implementation and test coverage

### Architecture and Design  
- `cs-architect` - **IMPLEMENTED** - High-level system design, architectural decisions, and ADR creation
- `cs-design-python` - **IMPLEMENTED** - Python API design, module hierarchies, interface design
- `cs-integrator` - System boundaries, integration patterns, dependency analysis

### Implementation and Code Quality
- `cs-code-python` - **IMPLEMENTED** - Python code implementation, refactoring, and quality assurance
- `cs-conform-python` - **IMPLEMENTED** - Review Python code for compliance with project practices
- `cs-conform-toml` - **IMPLEMENTED** - Review TOML files for formatting and standards

### Testing and Validation
- `cs-plan-pytests` - **IMPLEMENTED** - Plan comprehensive Python test strategies
- `cs-develop-pytests` - **IMPLEMENTED** - Implement Python test cases and validation logic

## Project Analysis
- `cs-analyze-dependencies` - Review and report on dependency health/updates
- `cs-audit-codebase` - Comprehensive code quality and structure analysis
- `cs-find-todos` - Collect and organize TODO comments across the project
- `cs-inquire` - **IMPLEMENTED** - Interactive project exploration and analysis

## Development Workflow
- `cs-prepare-pr` - Pre-PR checklist (tests, linting, docs, etc.)
- `cs-update-version` - Handle version bumping with changelog integration
- `cs-copier-update` - **IMPLEMENTED** - Update project from its Copier template

## Documentation
- `cs-generate-api-docs` - Create API documentation from code
- `cs-update-readme-rst` - **IMPLEMENTED** - Refresh README based on current project state
- `cs-document-examples-rst` - **IMPLEMENTED** - Create practical, testable examples documentation
- `cs-document-changes` - Generate release notes from recent commits

## Quality Assurance
- `cs-security-scan` - Run security checks and vulnerability scans
- `cs-performance-profile` - Analyze performance bottlenecks
- `cs-coverage-report` - Generate and analyze test coverage

## Release Management
- `cs-release-checkpoint` - **IMPLEMENTED** - Create release checkpoints
- `cs-release-final` - **IMPLEMENTED** - Handle final release preparation
- `cs-release-maintenance` - **IMPLEMENTED** - Manage maintenance releases
- `cs-annotate-release` - **IMPLEMENTED** - Add release annotations and notes

## Utilities
- `cs-obtain-instructions` - **IMPLEMENTED** - Retrieve and display project instructions
- `cs-create-command` - **IMPLEMENTED** - Generate new custom slash commands
- `cs-update-command` - **IMPLEMENTED** - Update existing slash commands with improvements

## Implementation Priority

**Phase 1** (Core Roles - Proof of Concept): ✅ **COMPLETED**
1. `cs-architect` - Architecture and system design decisions ✅
2. `cs-code-python` - Python implementation and quality assurance ✅
3. `cs-design-python` - API design and module structure ✅

**Phase 2** (Extended Workflow):
4. `cs-analyze-requirements` - Requirements validation and traceability
5. `cs-integrator` - System integration and boundaries
6. `cs-prepare-pr` - Pre-commit workflow automation

**Phase 3** (Analysis and Maintenance):
7. `cs-analyze-dependencies` - Dependency management and health
8. `cs-audit-codebase` - Comprehensive project analysis
9. `cs-sync-template` - Template synchronization and updates

These commands follow the "focused roles with just the documentation they need" philosophy, where each command loads specific `@`-references relevant to its domain and avoids context pollution.
