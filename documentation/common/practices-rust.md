<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->

<a id="rust-development-guide"></a>
# Rust Development Guide

This guide covers **comprehensive Rust development guidance including
code organization, patterns, architectural decisions, and formatting
standards**. For general guidance applicable to all languages, see the main
[practices guide](practices.md). For cross-language formatting and shared
workflow guidance, see the [code style guide](style.md),
[environment guide](environment.md), [validation guide](validation.md),
[testing guide](tests.md), and [release guide](releases.md).

<a id="module-organization"></a>
## Module Organization

- Follow standard Rust module organization patterns:
  - `src/lib.rs` or `src/main.rs` as the crate root
  - Use `src/module.rs` files with `src/module/` directories for submodules
  - Organize related functionality into logical modules
  - Re-export important items at appropriate levels using `pub use`
- Apply project nomenclature guidelines from the
  [nomenclature guide](nomenclature.md) when naming modules, following Rust's
  `snake_case` convention for module names.

<a id="naming-conventions"></a>
## Naming Conventions

- Follow standard Rust naming conventions as defined in the Rust API Guidelines:
  - **Types, traits, enums**: `PascalCase`
  - **Functions, variables, modules**: `snake_case`
  - **Constants, statics**: `SCREAMING_SNAKE_CASE`
  - **Macros**: `snake_case` (by convention, though not enforced)
- Apply project nomenclature guidelines from the
  [nomenclature guide](nomenclature.md) when naming types, functions, and
  variables.

<a id="documentation"></a>
## Documentation

<a id="content-standards"></a>
### Content Standards

- Write documentation comments in narrative mood (third person) consistent with project documentation standards.

- Use standard Rust documentation patterns:

  - `///` for public API documentation
  - `//!` for module-level documentation
  - Include examples in documentation when helpful

- Document error conditions using the standard `# Errors` section:

  ``` rust
  /// Validates user configuration.
  ///
  /// # Errors
  ///
  /// Returns `CrateError::Validation` if the configuration is invalid.
  pub fn validate_config(config: &Config) -> Result<(), CrateError> {
      // implementation
  }
  ```

<a id="visual-formatting"></a>
### Visual Formatting

- Use standard Rust documentation comments (`///` for items, `//!` for modules).

- Write documentation in narrative mood (third person) consistent with project documentation conventions.

  **✅ Prefer:**

  ``` rust
  /// Validates the configuration data.
  /// 
  /// Returns the validated configuration or an error if validation fails.
  pub fn validate_configuration(config: &Config) -> Result<Config, ConfigError> {
      // implementation
  }
  ```

  **❌ Avoid:**

  ``` rust
  /// Validate the configuration data.
  pub fn validate_configuration(config: &Config) -> Result<Config, ConfigError> {
      // implementation  
  }
  ```

<a id="formatting-standards"></a>
## Formatting Standards

- Follow the standard Rust formatting conventions enforced by `rustfmt`. The project's `.rustfmt.toml` configuration defines the specific formatting rules.
- Use `cargo fmt` to automatically format code according to project standards.
- Maximum line length follows the general project standard of 79 columns, which may be configured in `.rustfmt.toml` if different from Rust defaults.

<a id="testing"></a>
## Testing

Language-neutral public-contract rules live in the
[testing guide](tests.md#public-contracts-and-internal-visibility). This
section states how those rules apply in Rust crates.

<a id="test-layout"></a>
### Test Layout

- Prefer tests under `tests/unit` and `tests/integration` over inline
  `#[cfg(test)]` modules in `src/**`.
- Prefer tests that exercise public interfaces. Avoid source-inclusion
  patterns used only to reach private internals.
- External unit tests are still unit tests. Requiring public contracts does
  not mean every test must be a multi-crate integration or end-to-end check.

<a id="inline-cfg-test"></a>
### Inline `#[cfg(test)]` Modules

Inline `#[cfg(test)]` modules used to access crate-private items are a last
resort for behavior that cannot reasonably be tested through public
contracts or a clean injection seam. They are not a convenience escape
hatch.

Permit an inline `#[cfg(test)]` block only when **all** of the following
hold:

1. The tested item is crate-private **by design** (not by oversight or
   laziness), and making it testable externally would require widening its
   visibility or adding a `#[doc(hidden)] pub` escape hatch that would
   itself become unintended API surface.
2. No existing public interface exercises the same code path.
3. The inline test block contains at most **one** `#[test]` function.

If a candidate inline test fails any of these conditions, move it to
`tests/unit` and introduce a narrow seam, restructure ownership, or
otherwise keep the public surface intentional. Do not default to inline
access to avoid that conversation; the friction is intentional.

<a id="private-algorithms"></a>
### Private Algorithms

Genuinely private algorithms may still deserve focused coverage. Prefer, in
order:

1. Exercise the algorithm through the public capability that owns it.
2. Inject a narrow collaborator or strategy so the private path becomes
   reachable without exporting internals.
3. Only then use a tightly scoped inline `#[cfg(test)]` test that meets the
   criteria above.

Do not widen `pub` visibility or add test-only re-exports merely to satisfy
coverage tooling.

<a id="future-development"></a>
## Future Development

<!--
TODO: Expand Rust practices with comprehensive coverage including:
- Error handling patterns and hierarchies
- Type design (wide/narrow principle, newtype patterns)
- Immutability and ownership best practices
- Async/await patterns and best practices
- Trait design and implementation guidelines
- Macro definition patterns
- FFI and unsafe code guidelines
- Performance optimization patterns
- Concurrent programming patterns
-->
