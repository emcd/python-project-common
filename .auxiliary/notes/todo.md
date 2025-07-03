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