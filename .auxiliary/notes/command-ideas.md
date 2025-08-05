# Custom Slash Command Ideas

Collection of potential custom slash commands to implement.

## Project Analysis
- `cs-analyze-dependencies` - Review and report on dependency health/updates
- `cs-audit-codebase` - Comprehensive code quality and structure analysis
- `cs-find-todos` - Collect and organize TODO comments across the project

## Development Workflow
- `cs-prepare-pr` - Pre-PR checklist (tests, linting, docs, etc.)
- `cs-update-version` - Handle version bumping with changelog integration
- `cs-sync-template` - Update project from its Copier template

## Documentation
- `cs-generate-api-docs` - Create API documentation from code
- `cs-update-readme` - Refresh README based on current project state
- `cs-document-changes` - Generate release notes from recent commits

## Quality Assurance
- `cs-security-scan` - Run security checks and vulnerability scans
- `cs-performance-profile` - Analyze performance bottlenecks
- `cs-coverage-report` - Generate and analyze test coverage

## Communication & Analysis
- `cs-inquire` - Request analytical responses rather than immediate code changes (see draft below)

---

## Draft: cs-inquire Command

**Purpose**: Request analytical discussion and opinions rather than immediate code changes. Prevents misinterpretation of questions as hints for code modifications.

**Key behaviors**:
- Respond to questions with rationale, pros/cons, alternatives
- Provide pushback and disagreement when appropriate
- Offer better alternatives if they exist
- Focus on analysis and discussion before any code changes
- Avoid deference - give honest technical opinions
- Ask clarifying questions if the request is ambiguous

**Example usage scenarios**:
- "What do you think about this architecture decision?"
- "Are there any issues with this approach?"
- "How would you handle error cases here?"
- "What are the tradeoffs of using X vs Y?"

**Instruction draft for cs-create-command**:
```
cs-inquire.md - A process for providing analytical responses and technical opinions rather than immediately modifying code. When users ask questions about code or architecture, respond with analysis, rationale, pros/cons, and alternatives. Provide honest pushback and better alternatives when appropriate. Focus on discussion and technical reasoning before any code changes.
```