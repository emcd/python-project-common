# Documentation Sunset Notice

This directory (`documentation/common/`) is a frozen mirror of shared
guidance whose canonical home is now `documentation-common`. It is kept
only so that floating `stable/.../common/...` URLs on our GitHub Pages
keep resolving for old downstream documentation. It is not linked from
the project index and receives no updates.

## Deletion condition

This directory will be deleted once every downstream project based on
this template, of which we are aware or about which we care, has
released at least one new major or minor version built on template
v1.63.7 or later (the release that repointed shared-documentation
links at `documentation-common`). Adoption is tracked by the Template
Owner; no date is set.

## Effect of deletion

- Floating `stable/.../common/...` URLs will stop resolving at the
  next stable publication after deletion. Old downstream documentation
  pointing at them will 404.
- Version-pinned URLs for already-published releases keep working;
  published output is static and is not touched by this deletion.
- Downstream projects on current templates link to
  `documentation-common` directly and are unaffected.
