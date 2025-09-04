---
allowed-tools: Read, Write, Edit, MultiEdit, LS, Glob, Grep, Bash(find:*), Bash(ls:*), Bash(wc:*)
description: Systematically find, categorize, and analyze TODO comments for technical debt management
---

# Technical Debt Review

Systematically find, categorize, and analyze TODO comments across the project
codebase to provide actionable insights about technical debt and outstanding
work items.

Filter criteria and analysis focus: $ARGUMENTS
(if blank, then consider entire project)

## Context

- Notes: @.auxiliary/notes
- Project architecture: @documentation/architecture/summary.rst
- Project designs: @documentation/architecture/designs

## Prerequisites

Before running this analysis, ensure:
- Understanding of project structure and file organization
- Access to both source code and auxiliary documentation

## Process Summary

Key functional areas:
1. **Discovery**: Search for TODO/FIXME/XXX/HACK comments across all relevant files
2. **Categorization**: Organize findings by urgency, component, and type
3. **Analysis**: Assess technical debt impact and provide prioritization insights
4. **Reconciliation**: Compare source code TODOs with tracking documents
5. **Reporting**: Generate actionable summary with recommended next steps

## Safety Requirements

Stop and consult the user if:
- Large volume of TODOs (>100) found that may require batch processing
- Inconsistencies between tracking documents and source code require manual review
- File access permissions prevent comprehensive analysis

## Execution

Execute the following steps:

### 1. Comprehensive TODO Discovery

Search for all TODO-style comments across the project:
- Use Grep to find TODO, FIXME, XXX, HACK, NOTE patterns
- Search Python files, documentation, configuration files
- Include both inline comments and dedicated TODO sections
- Capture surrounding context (3-5 lines) for each finding

### 2. Pattern Analysis and Categorization

Analyze discovered TODOs for:
- **Urgency indicators**: Words like "urgent", "critical", "before release", "security"
- **Component classification**: Group by module, file, or functional area
- **Type classification**: Bug fix, feature enhancement, refactoring, documentation
- **Age estimation**: Check git blame for when TODO was introduced

### 3. Auxiliary Document Review

Examine TODO tracking files in `.auxiliary/notes/`:
- Read any existing TODO tracking documents
- Compare with source code findings
- Identify completed items that should be removed
- Note discrepancies between tracking and actual code state

### 4. Priority Assessment

Evaluate each TODO for:
- **Business impact**: Customer-facing vs. internal improvements
- **Technical risk**: Potential for bugs, security issues, or maintenance burden
- **Implementation complexity**: Quick fixes vs. architectural changes
- **Dependencies**: Items blocking other work vs. standalone improvements

### 5. Reporting and Recommendations

Generate structured output including:
- **Executive summary**: Total count, high-priority items, key themes
- **Categorized listings**: Organized by urgency, component, and type
- **Urgent actions**: Items requiring immediate attention
- **Cleanup opportunities**: Completed or obsolete TODOs to remove
- **Tracking reconciliation**: Sync recommendations between documents and code
- **Next steps**: Prioritized action plan for technical debt reduction

### 6. Documentation Updates

When appropriate:
- Update or create TODO tracking documents in `.auxiliary/notes/`
- Remove completed TODO comments from source code
- Add context or priority indicators to ambiguous TODOs
- Standardize TODO format across the project

### 7. Summary Report

Provide comprehensive analysis including:
- Total technical debt inventory
- Risk assessment of critical items
- Recommended prioritization for next development cycles
- Maintenance suggestions for keeping TODO management current
