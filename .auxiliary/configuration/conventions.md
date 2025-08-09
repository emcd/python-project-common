# Context



- Project overview and quick start: README.rst
- Product requirements and goals: documentation/prd.rst
- System architecture and design: @documentation/architecture/
- Development practices and style: @.auxiliary/instructions/
- Current session notes and TODOs: @.auxiliary/notes/

- Use the 'context7' MCP server to retrieve up-to-date documentation for any SDKs or APIs.
- Check README files in directories you're working with for insights about architecture, constraints, and TODO items.
- Update files under `.auxiliary/notes` during conversation, removing completed tasks and adding emergent items.

# Operation

- Use `rg --line-number --column` to get precise coordinates for MCP tools that require line/column positions.
- Choose appropriate editing tools based on the task complexity and your familiarity with the tools.
- Batch related changes together when possible to maintain consistency.
- Use relative paths rather than absolute paths when possible.
- Do not write to paths outside the current project unless explicitly requested.
- Use the `.auxiliary/scribbles` directory for scratch space instead of `/tmp`.

# Commits

- Use `git status` to ensure all relevant changes are in the changeset.
- Use the `python-conformer` agent to review changes that include Python code before committing.
- Do **not** commit without explicit user approval. Ask: "Do the changes that I am about to commit look good to you?"
- Use present tense, imperative mood verbs (e.g., "Fix" not "Fixed").
- Write sentences with proper punctuation.
- Include a `Co-Authored-By:` field as the final line. Should include the model name and a no-reply address.

# Project Notes

<!-- This section accumulates project-specific knowledge, constraints, and deviations.
     For structured items, use documentation/architecture/decisions/ and .auxiliary/notes/todo.md -->
