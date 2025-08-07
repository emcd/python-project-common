# Claude Code Agent Ideas

## Specialized Architectural Agents

### Core Architecture Agents

#### `architect`
**Purpose**: High-level system design and architectural decisions
**Capabilities**:
- Create and review ADRs using our refined format (no date field, with Alternatives section)
- Analyze system boundaries and component relationships
- Evaluate architectural trade-offs (performance, maintainability, scalability)
- Review architecture/summary.rst for consistency and completeness
- Suggest architectural patterns based on requirements

#### `python-designer`
**Purpose**: Python-specific design decisions and API design
**Capabilities**:
- Design module hierarchies following practices.rst patterns
- Create clean APIs with proper wide/narrow parameter patterns
- Design exception hierarchies using Omniexception/Omnierror
- Review code for adherence to style guidelines
- Suggest refactoring strategies for better separation of concerns

#### `requirements-analyst`
**Purpose**: Requirements gathering and PRD creation
**Capabilities**:
- Create comprehensive PRDs using our template format
- Break down high-level goals into specific, testable requirements
- Design user stories with proper acceptance criteria
- Analyze requirement dependencies and conflicts
- Bridge business needs with technical constraints

#### `system-integrator`
**Purpose**: Integration patterns and system boundaries
**Capabilities**:
- Design integration patterns between components
- Create interface specifications for architecture/designs/
- Analyze dependency injection patterns
- Review system cohesion and coupling
- Suggest communication protocols between services

### Specialized Domain Agents

#### `data-modeler`
**Purpose**: Data architecture and modeling
**Capabilities**:
- Design data schemas and relationships
- Create data flow diagrams
- Model domain entities and their interactions
- Review data consistency and normalization

#### `toml-data-modeler`
**Purpose**: TOML-specific configuration and data modeling
**Capabilities**:
- Design TOML configuration schemas
- Create validation patterns for TOML data
- Model hierarchical configuration structures
- Review TOML data consistency

#### `rust-designer`
**Purpose**: Rust-specific design patterns and architecture
**Capabilities**:
- Design Rust module hierarchies and crate structure
- Apply Rust ownership and borrowing patterns
- Create error handling strategies with Result types
- Design trait-based architectures

## Model-Specific Variants

### Strategic Model Selection

**Architectural Reasoning Variants**:
- `architect-opus-ultrathink` - Complex system design requiring deep trade-off analysis
- `architect-sonnet-deepthink` - Routine architectural reviews with solid reasoning
- `architect-haiku-quickthink` - Simple ADR reviews or pattern validation

**Python Design Variants**:
- `python-designer-sonnet-deepthink` - API design leveraging Sonnet's Python expertise
- `python-designer-opus-ultrathink` - Complex domain modeling intersecting with Python design
- `python-designer-haiku-quickthink` - Routine code reviews against practices.rst

**Requirements Analysis Variants**:
- `requirements-analyst-opus-ultrathink` - Complex domain requirements with many stakeholders
- `requirements-analyst-sonnet-deepthink` - Standard PRD creation and requirements analysis

### Naming Convention

`{base-agent}-{model}-{thinking-level}`

**Thinking Levels**:
- `quickthink` - Standard reasoning
- `deepthink` - Enhanced reasoning
- `ultrathink` - Maximum reasoning depth

### Strategic Benefits

**Quality Matching**: Match reasoning complexity to task complexity
**Cost Optimization**: Use appropriate model and thinking level for each task
**Speed Optimization**: Quick decisions when appropriate, deep analysis when needed
**Specialization**: Leverage each model's strengths for optimal results

## Integration with Documentation Framework

These agents would work seamlessly with our new architecture documentation structure:

- **ADR Creation**: `architect` agents can populate `architecture/decisions/` 
- **Design Specifications**: `python-designer` can create content for `architecture/designs/`
- **Requirements**: `requirements-analyst` can maintain and update `prd.rst`
- **System Overview**: `architect` can keep `architecture/summary.rst` current

## Experimentation Opportunities

**Haiku Exploration**: Test Haiku for lightweight tasks like:
- Pattern validation against established guidelines
- Quick code review for style compliance
- Simple template completions
- Routine documentation updates

**Model Comparison**: Compare outputs across models for similar tasks to optimize agent-model pairings.

## Future Considerations

- Integration with MCP servers (ruff, pyright, text-editor) for enhanced capabilities
- Automated handoffs between agents (e.g., requirements-analyst → architect → python-designer)
- Template-specific agent configurations
- Project-specific agent customizations