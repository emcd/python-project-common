# TODO Items

## Future Enhancements

### Documentation URL Support for docs-* Tags

**Goal:** Enable pointing to published HTML documentation around specific `docs-*` tags instead of always referencing `/stable/` documentation.

**Current State:** Common documentation URLs in templates currently point to `/stable/sphinx-html/common/` paths at the `python-project-common` GitHub pages.

**Desired State:** Support referencing documentation at specific tag-based URLs (e.g., `/docs-1/sphinx-html/common/`) to allow for version-specific documentation linking.

**Implementation Requirements:**
- Modify `sources/emcdproj/website.py` to support publishing documentation for `docs-*` tags
- Update template URL patterns to support configurable documentation versions
- Consider backward compatibility with existing `/stable/` references

**Priority:** Future enhancement - current `/stable/` approach is functional for immediate needs.

## Post-1.29 Development Ideas

### High Priority

#### Create tests/README.rst
**Goal:** Document testing conventions and architecture for contributors.
**Details:** Create comprehensive README consistent with write-tests command and documentation/common/tests.rst guidance. Include coverage expectations, test organization, and examples.
**Why:** Complements our new write-tests command and improves developer experience.

#### Add Github Release Poller to Release Workflow
**Goal:** Improve release workflow reliability by ensuring Github release is registered before artifact publication.
**Details:** Add polling step to wait for Github API to register new release before attempting to publish artifacts. Current workflow occasionally fails due to API delays.
**Why:** Solves real production reliability issue we've experienced.

### Medium Priority

#### Improve Test Coverage
**Goal:** Increase test coverage while avoiding integration test hazards.
**Details:** Carefully add tests for uncovered code paths, being mindful of integration tests that might clobber production state. Focus on unit tests and safe integration scenarios.
**Challenges:** Need to identify safe vs. risky integration test scenarios.

#### Add MCP Server Support to Claude GitHub Workflow
**Goal:** Enhance automated code analysis and testing capabilities.
**Details:** Add useful MCP servers (text-editor, ruff, pyright, context7) to the claude GitHub workflow to improve code quality and analysis automation.
**Why:** Could significantly improve automated testing and code analysis capabilities.

### Lower Priority

#### Enhance Write-Tests Command
**Goal:** Improve write-tests command based on usage experience.
**Details:** Add features like coverage gap analysis, test template generation, or integration with specific testing frameworks based on real usage patterns.

#### Add More Custom Slash Commands
**Goal:** Expand Claude Code integration with project-specific workflows.
**Ideas:** 
- `/analyze-coverage` - Deep dive into coverage gaps
- `/update-template` - Streamlined copier template updates
- `/validate-release` - Pre-release validation checklist

#### Documentation Improvements
**Goal:** Enhance project documentation and developer experience.
**Ideas:**
- API documentation improvements
- Architecture decision records (ADRs)
- Contributing guide enhancements
- Tutorial content for template usage

#### Release Workflow Enhancements
**Goal:** Further improve release automation and reliability.
**Ideas:**
- Automated release notes generation improvements
- Multi-stage release validation
- Rollback procedures documentation
- Release metrics and monitoring