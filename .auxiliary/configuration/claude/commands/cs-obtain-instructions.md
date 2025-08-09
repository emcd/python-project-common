---
allowed-tools: Bash(curl:*), Bash(mkdir:*), LS, Read
description: Download all project documentation guides locally for offline reference
---

# Download Project Documentation Guides

You need to download all project documentation guides to `.auxiliary/instructions/` for local reference.

## Your Task

1. **Create the local directory:**
   ```bash
   mkdir -p .auxiliary/instructions
   ```

2. **Download all guides using curl (overwrite existing files):**

   Base URL: `https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/`

   **Download these files:**
   - `nomenclature.rst` - Naming conventions and terminology standards
   - `nomenclature-germanic.rst` - Conversion between Germanic-derived and Latin-derived nomenclature
   - `practices.rst` - Core development practices and architectural patterns
   - `style.rst` - Code formatting and stylistic conventions
   - `tests.rst` - Test development and validation patterns

   Use `curl` with `-o` flag to overwrite existing files in `.auxiliary/instructions/[filename]`

3. **Verify the downloads:**
   - Check that all four files were created and have reasonable sizes
   - Briefly inspect content to ensure they're not error pages
   - Report what was downloaded successfully

## Expected Outcome

After completion:
- All four guide files available locally in `.auxiliary/instructions/`
- Other commands can use `@.auxiliary/instructions/practices.rst` instead of WebFetch
- Faster, offline access to project documentation during conformance tasks
