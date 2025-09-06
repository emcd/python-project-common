---
description: Analyze current project state and refresh manually-maintained sections of README.rst while preserving template content
---

# Update README Documentation

Analyze the current project state and refresh the manually-maintained sections
of README.rst files while preserving auto-generated template content and
ensuring accuracy with actual project capabilities.

User input: $ARGUMENTS

## Context

- Current git status: !`git status --porcelain`
- Project structure: !`ls -la`
- Current README: @README.rst
- Project metadata: @pyproject.toml
- Product requirements: @documentation/prd.rst
- Architecture overview: @documentation/architecture/filesystem.rst

## Prerequisites

Before updating README documentation, ensure:
- Current README.rst exists and is accessible
- Understanding of project's actual capabilities and features
- Access to project metadata and configuration files

## Process Summary

Key functional areas:
1. **Content Analysis**: Examine current README and identify TODO sections needing updates
2. **Project Assessment**: Analyze actual capabilities from code, CLI, and configuration
3. **Content Generation**: Create compelling descriptions, features, and examples based on real functionality
4. **Validation**: Ensure all claims and examples match actual project capabilities

## Safety Requirements

Stop and consult the user if:
- README.rst cannot be read or is missing critical structure
- Template boundaries are unclear or may be damaged
- Project capabilities cannot be determined from available sources
- Generated examples cannot be validated against actual implementation
- Significant structural changes to README are required beyond content updates

All template-rendered sections must be preserved without modification; these
include: badges, installation, contribution, flair


## Execution

Execute the following steps:

### 1. README Analysis
Read and analyze the current README structure:
- Examine existing README.rst for TODO markers and outdated content
- Identify template-generated sections that must be preserved
- Map sections that need manual content updates
- Note existing manual content that should be retained

### 2. Project Capability Assessment
Analyze the actual project functionality:
- Extract project metadata from pyproject.toml (name, description, dependencies)
- Read PRD document if available for project goals and features
- Examine source code structure to understand API capabilities
- Test CLI functionality if enabled to document actual usage patterns
- Review configuration files and scripts for additional capabilities

### 3. Content Generation Strategy
Plan content updates based on project analysis:
- Draft compelling project description with emoji prefix (e.g., 🔧, 📊, 🌐, 🎯) matching project purpose
- Identify key features based on actual implementation
- Plan 1-2 concise examples that whet appetites without overwhelming
- Avoid advanced showcase examples - focus on core value demonstration
- Consider additional sections (Use Cases, Motivation, Configuration) appropriate for project complexity
- Ensure content accuracy and professional tone

### 4. README Content Updates
Update manual sections while preserving template content:
- Replace ".. todo:: Provide project description" with emoji-prefixed compelling description
- Add or update "Key Features ⭐" section with bullet points of actual capabilities
- Generate concise "Examples 💡" section with 1-2 essential usage patterns only
- Keep examples minimal and focused on core value, not comprehensive showcase
- Add relevant sections like "Use Cases", "Motivation", or "Configuration" as appropriate
- Preserve all template-generated sections (badges, installation, contribution, flair)

### 5. Content Validation
Verify accuracy of all updated content:
- Test all code examples for correctness with current codebase
- Verify feature claims are supported by actual implementation
- Check that installation instructions match project configuration
- Ensure RST formatting is correct and consistent
- Validate examples are concise and appetite-whetting, not overwhelming
- Confirm README length is appropriate for project complexity

### 6. Final Review
Complete final validation and formatting:
- Review entire README for consistency and professional presentation
- Ensure all TODO markers have been appropriately addressed
- Verify template boundaries are intact and respected
- Confirm examples are executable and accurate
- Check that content maintains engaging tone while being factually correct

### 7. Summarize Updates
Provide concise summary of updates to the user.
