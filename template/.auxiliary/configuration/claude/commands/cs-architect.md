---
allowed-tools: [Read, Write, Edit, MultiEdit, LS, Glob, Grep]
description: Architectural analysis, system design decisions, and ADR creation
---

# System Architecture Analysis

Analyze architectural decisions, system design patterns, component
relationships, and technical trade-offs to provide guidance on high-level
system structure.

Request from user: $ARGUMENTS

Stop and consult if:
- Implementation details are requested instead of architectural guidance
- Specific code changes are needed
- Requirements analysis is needed

## Context

- Product requirements: @documentation/prd.rst
- Architecture overview: @documentation/architecture/summary.rst
- Filesystem patterns: @documentation/architecture/filesystem.rst
- Architecture guidelines: @.auxiliary/instructions/architecture.rst
- Current project state: !`find documentation/architecture -name "*.rst" | head -10`

## Prerequisites

Before providing architectural analysis, ensure:
- Understanding of current system architecture and constraints
- Familiarity with architectural decision record (ADR) format
- Knowledge of standard filesystem organization patterns
- @.auxiliary/instructions/architecture.rst guidelines are followed

## Process Summary

Key functional areas:
1. **Analysis**: Examine architectural context and design forces
2. **Decision Framework**: Apply architectural principles and trade-off analysis
3. **Documentation**: Create ADRs or update architectural documentation
4. **Validation**: Ensure decisions align with project constraints and goals

## Safety Requirements

Stop and consult the user if:
- Architectural decisions have significant impact on existing system components
- Decision conflicts with existing architectural patterns or constraints
- Decision requires changes to fundamental system assumptions

## Execution

Execute the following steps:

### 1. Architectural Context Analysis
Review current architecture and identify relevant patterns:
- Examine existing architectural documentation
- Understand system boundaries and component relationships
- Identify architectural forces and constraints
- Assess alignment with project goals and requirements

### 2. Design Forces Assessment
Analyze the forces driving the architectural decision:
- Technical constraints (performance, scalability, compatibility)
- Quality attributes (maintainability, testability, security)
- Integration requirements with existing components
- Future flexibility and evolution needs

### 3. Alternative Evaluation
Consider multiple architectural approaches:
- Document all seriously considered alternatives
- Analyze trade-offs for each option (benefits, costs, risks)
- Consider "do nothing" as a baseline alternative
- Evaluate alignment with established architectural patterns
- Assess implementation complexity and maintenance burden

### 4. Decision Recommendation
Provide clear architectural guidance:
- State recommended approach with clear rationale
- Explain how decision addresses the identified forces
- Document expected positive and negative consequences
- Include specific architectural patterns or principles applied
- Provide text-based diagrams or examples when helpful

### 5. Documentation Creation
When appropriate, create or update architectural documentation:
- Generate ADRs following the standard format
- Update architecture summary for significant system changes
- Ensure consistency with filesystem organization patterns
- Reference related architectural decisions and dependencies

### 6. Implementation Guidance
Provide high-level implementation direction without specific code:
- Suggest component organization and interfaces
- Recommend integration patterns with existing system
- Identify key architectural boundaries and abstractions
- Highlight critical implementation considerations

### 7. Summarize Updates
Provide concise summary of updates to the user.
