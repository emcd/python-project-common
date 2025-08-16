# Claude Code Hook Ideas

## Security & Safety Hooks

- **Pre-bash-dangerous-commands**: Block `rm -rf`, `sudo rm`, `format`, etc. with a stern warning
- **Pre-edit-secrets-check**: Prevent editing files with "secret", "key", "password" in the name
- **Post-edit-secret-scanner**: Scan edited files for potential secrets/API keys

## Code Quality Hooks

- **Pre-commit-todo-checker**: Count TODO/FIXME comments and warn if they're growing
- **Post-edit-auto-formatter**: Auto-run code formatters after file edits
- **Pre-commit-breaking-changes**: Detect API changes and require confirmation

## Development Workflow Hooks

- **Pre-commit-branch-checker**: Prevent commits to `main`/`master` without explicit confirmation
- **Post-commit-pr-reminder**: Suggest creating a PR after a certain number of commits
- **Pre-edit-production-warning**: Extra confirmation before editing production config files

## Fun/Motivational Hooks

- **Post-commit-encouragement**: Random encouraging messages after successful commits
- **Pre-bash-npm-install-warning**: "Are you sure? This will take 47 years..." before `npm install`
- **Post-successful-test-celebration**: ASCII art party when all tests pass

## Project Management

- **Pre-commit-ticket-checker**: Ensure commit messages reference issue numbers
- **Post-large-change-documentation**: Remind to update docs after big changes