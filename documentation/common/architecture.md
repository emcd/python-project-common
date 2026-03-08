<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->

<a id="architecture-documentation"></a>
# Architecture Documentation

This guide covers architectural documentation practices, including
architectural decision records (ADRs) and design documentation standards. For
Python-specific package-structure patterns, see the
[Python architecture guide](architecture-python.md).

<a id="architectural-decision-records"></a>
## Architectural Decision Records

Architectural Decision Records (ADRs) document the significant architectural decisions made during the project lifecycle. They capture the context, reasoning, and consequences of decisions to provide future teams with the rationale behind architectural choices.

<a id="purpose-and-benefits"></a>
### Purpose and Benefits

- **Historical context**: Preserve the reasoning behind architectural decisions for future reference and team onboarding.
- **Decision accountability**: Create a clear record of who made decisions and under what circumstances.
- **Alternative exploration**: Document what was considered but not chosen, providing valuable context for future architectural reviews.
- **Change management**: Track the evolution of architectural decisions over time through status updates and supersession.

<a id="adr-format"></a>
### ADR Format

Use the following format for all architectural decision records:

``` rst
*******************************************************************************
[Number]. [Title]
*******************************************************************************

Status
===============================================================================

[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

Context
===============================================================================

[Describe the forces at play, constraints, and business/technical situation
that led to this decision. What problem are we trying to solve? What are the
key requirements and limitations?]

Decision
===============================================================================

[State the decision clearly and concisely. This should be the response to the
forces described in the Context section.]

Alternatives
===============================================================================

[Document what other options were considered and why each was rejected. This
provides valuable context for future decisions and shows that alternatives
were properly evaluated.]

Consequences
===============================================================================

[Describe the positive, negative, and neutral consequences of this decision.
Be honest about trade-offs and potential risks. Include impacts on:
- Performance
- Maintainability
- Team productivity
- System complexity
- Future flexibility]
```

<a id="adr-lifecycle-management"></a>
### ADR Lifecycle Management

**Numbering Convention**

- Use sequential numbering: `001-initial-architecture.rst`, `002-database-selection.rst`, etc.
- Zero-pad numbers to three digits for consistent sorting.
- Use lowercase, hyphenated filenames.

**Status Workflow**

- **Proposed**: Decision is under consideration and review.
- **Accepted**: Decision has been approved and is being implemented.
- **Deprecated**: Decision is no longer relevant but kept for historical context.
- **Superseded**: Decision has been replaced by a newer ADR (reference the superseding ADR number).

**Immutability Principle**

- Once an ADR is accepted, do not edit its content.
- If circumstances change, create a new ADR that supersedes the previous one.
- This preserves the historical decision context and reasoning.

<a id="best-practices"></a>
### Best Practices

**Context Documentation**

- Focus on forces and constraints that drove the decision.
- Include relevant business context, technical limitations, etc....
- Avoid implementation details - focus on the decision-making environment.

**Clear Decision Statements**

- State decisions unambiguously.
- Avoid hedging language like "might" or "could".
- Be specific about what will be done.

**Comprehensive Alternatives**

- Document all seriously considered alternatives.
- Explain why each alternative was rejected with specific reasons.
- Include "do nothing" as an alternative when relevant.

**Honest Consequences**

- Document both positive and negative consequences.
- Include trade-offs and potential risks.
- Consider long-term implications, not just immediate benefits.

<a id="standard-filesystem-organization-patterns"></a>
## Standard Filesystem Organization Patterns

This section documents the standard filesystem organization patterns used across all projects in the template system. These patterns provide consistency, maintainability, and clear separation of concerns.

<a id="root-directory-organization-principles"></a>
### Root Directory Organization Principles

**Single Sources Directory Pattern**

All source code resides in a unified `sources/` directory, separate from other project artifacts:

- **Clear separation**: Source code is distinctly separated from documentation, tests, and configuration files
- **Build process clarity**: Build tools can target the entire source tree without ambiguity
- **Mixed-language support**: Multiple languages can coexist with appropriate subdirectories

**Top-level Structure Standards**

Essential project files remain at the top level for immediate visibility:

- `LICENSE.txt`, `README.{md,rst}`, and the primary build/configuration manifest provide project overview
- `documentation/` contains all documentation source
- `tests/` mirrors source structure for test organization
- `.auxiliary/` provides development workspace (excluded from distributions)

<a id="language-specific-structure-patterns"></a>
### Language-Specific Structure Patterns

Language-specific package-layout and import-hub patterns should be
documented in overlays so the core architecture guidance remains broadly
applicable. For Python-specific details (including the `__` import-hub
pattern), see the [Python architecture guide](architecture-python.md).

<a id="tests-organization"></a>
### Tests Organization

The test structure should follow the guidance in the
[testing guide](tests.md).

<a id="data-resources-organization"></a>
### Data Resources Organization

The `data/` directory contains resources which are intended to be distributed with the package. These can include configuration templates, webapp icons, etc....

<a id="development-workspace"></a>
### Development Workspace

Development-specific files are organized in \`.auxiliary/\`:

``` 
.auxiliary/
├── notes/                       # Development notes and TODO items
├── scribbles/                   # Temporary development files
└── instructions/                # Local development guide copies
```

This workspace is excluded from package distributions but provides session continuity for development tools and local documentation storage.

<a id="architecture-documentation-beyond-adrs"></a>
## Architecture Documentation Beyond ADRs

<a id="system-summary"></a>
### System Summary

The system summary (`architecture/summary.rst`) should provide a high-level overview of the system architecture including:

- **Major components**: Key system modules, services, or subsystems.
- **Component relationships**: How components interact and depend on each other.
- **Data flow**: Major data paths through the system.
- **Deployment architecture**: How components are distributed and deployed.
- **Key architectural patterns**: Major patterns employed (MVC, microservices, event-driven, etc.).

<a id="filesystem-documentation"></a>
### Filesystem Documentation

The filesystem documentation (`architecture/filesystem.rst`) implements the standard patterns documented above for the specific project configuration:

- **Project-specific structure**: Shows actual package names and feature-specific organization
- **Integration patterns**: Shows how optional components (CLI, Rust extensions, etc.) integrate with the standard structure

<a id="design-documents"></a>
### Design Documents

Detailed design documents (under `architecture/designs/`) capture implementation-level specifications:

- **Interface specifications**: API contracts, service interfaces, module APIs.
- **Data schemas**: Database schemas, message formats, configuration structures.
- **Algorithm specifications**: Detailed algorithmic approaches for complex processing.
- **Protocol definitions**: Communication protocols between components.

**Design Document Guidelines**

- Reference the architectural decisions that informed the design.
- Include enough detail for implementation without over-specifying.
- Use diagrams and examples to illustrate complex concepts.
- Version design documents when significant changes occur.

<a id="language-specific-overlays"></a>
## Language-Specific Overlays

- [Python architecture guide](architecture-python.md) - Python package
  structure and import-hub pattern.
