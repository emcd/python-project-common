.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+


*******************************************************************************
001. Three-Tier Architecture for Project Lifecycle Management
*******************************************************************************

Status
===============================================================================

Accepted

Context
===============================================================================

The Python Project Common system needs to address the complete project lifecycle from initial creation through ongoing maintenance. The system must support:

- **Project Creation**: Rapid scaffolding of new Python projects with consistent structure
- **Development Workflow**: Automated CI/CD pipelines with quality gates and cross-platform testing
- **Maintenance Operations**: Ongoing documentation updates, coverage reporting, and template synchronization

Key forces driving the architectural decision:

**Separation of Concerns**: Different lifecycle phases have distinct requirements, tools, and update frequencies. Template generation happens once per project, CI/CD runs on every commit, and maintenance operations occur periodically.

**Tool Integration**: Each phase integrates with different toolsets - Copier for templating, GitHub Actions for automation, Python packaging for maintenance tools.

**Deployment Flexibility**: Components should deploy independently and scale based on usage patterns.

**Maintenance Overhead**: Architecture must accommodate single-maintainer model with community contributions.

Decision
===============================================================================

Implement a three-tier architecture separating template generation, workflow automation, and maintenance tooling into distinct layers:

**Tier 1: Template Generation Layer**
- Copier-based project scaffolding system
- Jinja2 templating with conditional feature support  
- Configuration management via copier.yaml

**Tier 2: CI/CD Automation Layer**
- Reusable GitHub Actions workflow components
- Cross-platform testing matrix execution
- Quality gates and release automation

**Tier 3: Project Maintenance Layer**  
- Python package (emcd-projects) for runtime maintenance
- Static site generation and badge management
- Template synchronization and update tooling

Each tier operates independently with well-defined interfaces and can evolve at different rates based on requirements.

Alternatives
===============================================================================

**Monolithic Architecture**
- Single integrated tool handling all lifecycle phases
- Rejected due to complexity of integrating disparate toolsets (Copier, GitHub Actions, Python packaging)
- Would create tight coupling between template changes and maintenance operations
- Difficult to scale individual components based on usage patterns

**Microservices Architecture**
- Fine-grained services for each operation (templating, testing, documentation, etc.)
- Rejected due to operational complexity for single-maintainer model
- Network dependencies would reduce reliability for template generation
- Overhead of service orchestration outweighs benefits for this use case

**Two-Tier Architecture (Template + Runtime)**
- Combine CI/CD automation with maintenance tooling
- Rejected because CI/CD and maintenance have fundamentally different execution contexts
- GitHub Actions workflows require different deployment and versioning patterns than Python packages
- Would blur boundaries between build-time and runtime operations

Consequences
===============================================================================

**Positive Consequences**

**Clear Separation of Concerns**: Each tier has well-defined responsibilities and can evolve independently. Template changes don't require maintenance tool updates and vice versa.

**Tool Integration Flexibility**: Each tier can leverage best-of-breed tools for its specific domain without compromising other layers.

**Independent Scaling**: Template generation scales with new project creation, CI/CD scales with commit frequency, maintenance scales with project count.

**Maintainability**: Clear architectural boundaries make the system easier to understand, debug, and extend.

**Community Contribution**: Contributors can work on specific tiers without understanding the entire system.

**Negative Consequences**

**Integration Complexity**: Three separate systems require coordination for end-to-end workflows.

**Version Synchronization**: Changes affecting multiple tiers require careful coordination to maintain compatibility.

**Testing Overhead**: Integration testing must verify correct operation across all three tiers.

**Documentation Burden**: Each tier requires separate documentation and architectural decision tracking.

**Neutral Consequences**

**Deployment Diversity**: Each tier uses different deployment mechanisms (Git repository, GitHub Actions marketplace, PyPI), which matches their different execution contexts but requires diverse operational knowledge.

**Technology Stack Diversity**: Each tier uses appropriate technologies (Jinja2, GitHub Actions YAML, Python) rather than forcing a single technology across all tiers.