---
allowed-tools: Read, Write, Edit, MultiEdit, LS, Glob, Grep
description: Manage product requirements documents and feature planning
---

# Product Requirements Management

Manage and update the Product Requirements Document (PRD) based on user input
about product requirements, feature planning, and related topics.

Request from user: $ARGUMENTS

## Context

- Current PRD state: @documentation/prd.rst
- Requirements guidelines: @.auxiliary/instructions/requirements.rst

## Prerequisites

Before managing PRD content, ensure:
- Understanding of current project scope and objectives
- Familiarity with existing functional and non-functional requirements
- @.auxiliary/instructions/requirements.rst guidelines are followed
- Changes align with overall project strategy

## Process Summary

Key functional areas:
1. **Analysis**: Review current PRD and understand requested changes
2. **Requirements Processing**: Apply requirements.rst standards to new content
3. **PRD Updates**: Make structured updates to documentation/prd.rst
4. **Validation**: Ensure consistency and completeness

### Process Restrictions

- Do not provide a timeline for deliverables.
- Do not plan sprints.

## Safety Requirements

Stop and consult the user if:
- Requested changes significantly expand or reduce product scope
- New requirements conflict with existing non-functional requirements
- Changes affect critical path features or constraints
- Requirements lack sufficient detail for implementation planning

## Execution

Execute the following steps:

### 1. Review Current State
Read and analyze the existing PRD to understand current scope.

### 2. Process User Requirements
Analyze the user input for:
- New functional requirements
- Changes to existing requirements
- Updates to goals, objectives, or success criteria
- Modifications to user personas or target users
- New constraints or assumptions

### 3. Apply Requirements Standards
Follow @.auxiliary/instructions/requirements.rst guidelines:
- Use specific, measurable, achievable, relevant, testable criteria
- Apply proper user story format when appropriate
- Assign requirement priorities (Critical/High/Medium/Low)
- Include acceptance criteria for functional requirements
- Maintain requirement traceability

### 4. Update PRD Structure
Make targeted updates to appropriate PRD sections:
- Executive Summary (if scope changes)
- Problem Statement (if new problems identified)
- Goals and Objectives (if success criteria change)
- Target Users (if new personas or needs identified)
- Functional Requirements (most common updates)
- Non-Functional Requirements (if technical requirements change)
- Constraints and Assumptions (if new limitations discovered)
- Out of Scope (if boundaries need clarification)

### 5. Maintain Consistency
Ensure all updates maintain PRD coherence:
- Requirements align with stated goals and objectives
- No conflicts between functional and non-functional requirements
- User stories trace back to identified user needs
- Acceptance criteria are testable and specific
- Priority assignments reflect user value

### 6. Summarize Updates
Provide concise summary of updates to the user.
