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
System Overview
*******************************************************************************

The Python Project Common system implements a three-tier architecture providing comprehensive project lifecycle management through template generation, workflow automation, and maintenance tooling.

System Architecture
===============================================================================

Major Components
-------------------------------------------------------------------------------

**Template Generation Layer (Copier Integration)**

The template system serves as the foundation for project creation:

* **Template Engine**: Copier-based project scaffolding with conditional feature support
* **Configuration Management**: Context-driven template customization via copier.yaml
* **Feature Matrix**: Optional integrations (CLI, Rust extensions, GUI frameworks, property testing)
* **Development Environment**: Pre-configured Hatch environments with quality assurance tooling

**CI/CD Automation Layer (GitHub Actions Workflows)**

Reusable workflow components provide standardized automation:

* **Cross-platform Testing**: Matrix execution across Python 3.9+ on Linux/macOS/Windows  
* **Quality Gates**: Integrated linting (Ruff), type checking (Pyright), and test execution
* **Documentation Pipeline**: Sphinx-based documentation generation with versioned deployment
* **Release Automation**: Package building, PyPI publication, and GitHub release management
* **Reporting System**: Coverage analysis and badge generation without external dependencies

**Project Maintenance Layer (emcd-projects Package)**

Runtime tooling for ongoing project management:

* **Static Site Generation**: Self-contained documentation and reporting infrastructure
* **Badge Management**: Dynamic coverage badge generation from test results  
* **Version Management**: Documentation indexing and cross-linking across releases
* **Template Synchronization**: Copier-based project updates with conflict resolution

Component Relationships
-------------------------------------------------------------------------------

**Sequential Dependency Chain**

.. code-block:: text

    Template Generation → Project Scaffolding → CI/CD Integration → Maintenance Tooling
           ↓                      ↓                    ↓                    ↓
    Copier Template         Hatch Environment     GitHub Actions      emcd-projects
    Feature Selection       QA Tool Config        Workflow Matrix     Site Management

**Integration Patterns**

* **Template → CI/CD**: Generated projects include pre-configured workflow references
* **CI/CD → Maintenance**: Workflows invoke maintenance tooling for reporting and site updates  
* **Maintenance → Template**: Tools support template updates via Copier synchronization
* **Cross-cutting**: All layers share common filesystem organization patterns and quality standards

Data Flow Architecture
-------------------------------------------------------------------------------

**Project Creation Flow**

1. **User Input**: Developer provides project configuration via Copier prompts
2. **Template Processing**: Jinja2 templating engine generates project structure
3. **Environment Setup**: Hatch configuration enables immediate development workflow
4. **CI/CD Integration**: GitHub Actions workflows activate on repository creation
5. **Quality Validation**: Automated testing and quality gates validate project integrity

**Maintenance Flow**

1. **CI/CD Execution**: Automated workflows generate test coverage and documentation
2. **Site Generation**: emcd-projects processes results into static site content
3. **Badge Updates**: Coverage badges reflect current test coverage metrics
4. **Documentation Indexing**: Versioned documentation maintains cross-version navigation
5. **Template Synchronization**: Projects can update from template changes via Copier

**Information Architecture**

* **Configuration**: Declarative project settings via pyproject.toml and copier.yaml
* **Documentation**: Structured documentation hierarchy with architectural decision records
* **Test Data**: Coverage metrics and test results flow through CI/CD to static site generation
* **Release Data**: Version information propagates from Git tags through build systems to deployment

Deployment Architecture
-------------------------------------------------------------------------------

**Development Environment**

* **Local Development**: Hatch environment management with isolated Python environments
* **Quality Assurance**: Pre-commit hooks integrate linting, formatting, and type checking
* **Documentation**: Local Sphinx builds for documentation development and testing

**CI/CD Environment**  

* **GitHub Actions**: Matrix-based execution across platform and Python version combinations
* **Workflow Composition**: Reusable workflow components enable consistent automation patterns
* **Artifact Management**: Build artifacts, test results, and documentation flow through workflow stages

**Deployment Targets**

* **PyPI Distribution**: Automated package publication with semantic versioning
* **Static Site Hosting**: GitHub Pages or similar static hosting for documentation and reports
* **Template Repository**: Centralized template distribution via GitHub repository

Key Architectural Patterns
-------------------------------------------------------------------------------

**Template Method Pattern**

The system employs template method pattern across all layers:

* **Project Templates**: Standardized structure with customizable components
* **Workflow Templates**: Reusable CI/CD patterns with project-specific configuration
* **Documentation Templates**: Consistent documentation structure across projects

**Repository Pattern**

Centralized resource management through repository abstractions:

* **Template Repository**: Single source of truth for project scaffolding
* **Workflow Repository**: Reusable workflow components shared across projects
* **Documentation Repository**: Common documentation standards and patterns

**Pipeline Pattern**

Sequential processing stages with clear handoff points:

* **Generation Pipeline**: Template processing → Environment setup → CI/CD integration
* **CI/CD Pipeline**: Source checkout → Quality gates → Testing → Documentation → Deployment
* **Maintenance Pipeline**: Results collection → Processing → Site generation → Deployment

**Plugin Architecture**

Extensible component system supporting optional features:

* **Template Plugins**: Optional features (CLI, Rust, GUI) activated via configuration
* **Workflow Plugins**: Specialized workflows (release, documentation, validation) composed as needed
* **Tool Integration**: Quality assurance tools integrated via standardized interfaces

Quality Attributes
-------------------------------------------------------------------------------

**Maintainability**

* **Separation of Concerns**: Clear architectural boundaries between template, workflow, and maintenance layers
* **Standard Patterns**: Consistent filesystem organization and naming conventions across all projects
* **Documentation Standards**: Comprehensive architectural decision records and design documentation

**Reliability** 

* **Quality Gates**: Multiple validation layers prevent defective releases
* **Self-contained Infrastructure**: No external service dependencies reduce failure points
* **Graceful Degradation**: Optional components fail safely without affecting core functionality

**Scalability**

* **Template Extensibility**: New features integrate through established plugin patterns
* **Workflow Reusability**: Common automation patterns scale across multiple projects  
* **Documentation Automation**: Self-maintaining documentation reduces manual overhead

**Security**

* **Minimal Permissions**: GitHub Actions workflows use least-privilege access patterns
* **No Secret Exposure**: Template generation avoids embedding sensitive information
* **Supply Chain Security**: Pinned workflow versions provide reproducible security posture

System Constraints and Assumptions
-------------------------------------------------------------------------------

**Technical Constraints**

* **GitHub Platform Dependency**: CI/CD automation designed specifically for GitHub Actions
* **Python Ecosystem Focus**: Template system targets Python packaging and tooling standards
* **Static Site Requirement**: Documentation must be hostable without server-side processing

**Operational Assumptions**

* **Single Maintainer Model**: Architecture accommodates limited maintenance resources
* **Community Contribution**: Template improvements flow back through standard open source patterns
* **Semantic Versioning**: Projects follow semantic versioning for template synchronization compatibility