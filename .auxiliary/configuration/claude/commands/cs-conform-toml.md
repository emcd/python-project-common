---
allowed-tools: Bash(git:*), LS, Read, Glob, Grep, Edit, MultiEdit, Write
description: Systematically conform TOML files to project style and practice standards
---

# TOML Configuration Conformance

For bringing existing TOML configuration files into full compliance with project standards.

Target files: $ARGUMENTS

Focus on style/practice conformance, not functionality changes.

## Prerequisites

- Read project documentation guides first:
  - @.auxiliary/instructions/practices.rst
  - @.auxiliary/instructions/practices-toml.rst
  - @.auxiliary/instructions/style.rst
  - @.auxiliary/instructions/nomenclature.rst
- Understand target files to be conformed
- Have read `CLAUDE.md` for project-specific guidance

## Context

- Current git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`

## Execution Structure

**Phase 1: Comprehensive Review**
Perform complete analysis and generate detailed compliance report before making any changes.

**Phase 2: Systematic Remediation**
Apply all identified fixes in systematic order, validating changes after completion.

## Compliance Standards

### Configuration Design Standards

#### 1. Table Organization

- Prefer table arrays with `name` fields over proliferating custom subtables.
- Table arrays scale better and reduce configuration complexity.

**❌ Avoid - custom subtables:**
```toml
[database]
host = 'localhost'

[database.primary]
port = 5432
timeout = 30

[database.replica]
port = 5433
timeout = 15
```

**✅ Prefer - table arrays with name field:**
```toml
[[database]]
name = 'primary'
host = 'localhost'
port = 5432
timeout = 30

[[database]]
name = 'replica'
host = 'localhost'
port = 5433
timeout = 15
```

#### 2. Key Naming Conventions

- Use hyphens instead of underscores in key names for better ergonomics.
- Apply nomenclature guidelines to key and table names.
- Use Latin-derived words when they are the established norm in the domain.

**❌ Avoid:**
```toml
max_connections = 100
retry_count = 3
database_url = 'postgresql://localhost/db'
```

**✅ Prefer:**
```toml
max-connections = 100
retry-count = 3
database-url = 'postgresql://localhost/db'
```

### Style Standards

#### 1. String Values

- Use single quotes for string values unless escapes are needed.
- Use double quotes when escapes are required.
- Use triple single quotes for multi-line strings (consistency with Python docstrings).

**❌ Avoid:**
```toml
name = "example-service"
description = "A service for processing data"
pattern = "user-.*"
```

**✅ Prefer:**
```toml
name = 'example-service'
description = 'A service for processing data'  
pattern = 'user-.*'

# Use double quotes when escapes are needed
windows-path = "C:\\Program Files\\Example"
message = "Line 1\nLine 2"

# Use triple single quotes for multi-line strings
description = '''
This is a longer description
that spans multiple lines.
'''
```

#### 2. Array and Table Formatting

- Keep arrays and inline tables on single lines when they fit within reasonable length.
- For longer arrays, place each element on its own line with proper indentation.

**✅ Prefer:**
```toml
ports = [ 8080, 8443, 9090 ]
database = { host = 'localhost', port = 5432 }

# For longer arrays
allowed-origins = [
    'https://example.com',
    'https://api.example.com', 
    'https://admin.example.com',
]
```

### Comprehensive Example: Configuration with Multiple Violations

Here is a TOML configuration that demonstrates many compliance violations:

```toml
[server_config]
host_name = "localhost"
port_number = 8080
max_connections = 100

[server_config.database_primary]
host = "localhost"
port = 5432
connection_timeout = 30
retry_attempts = 3

[server_config.database_replica]  
host = "localhost"
port = 5433
connection_timeout = 15
retry_attempts = 2

allowed_hosts = ["https://example.com", "https://api.example.com", "https://admin.example.com"]

description = "This is a multi-line description that explains what this service does and how it should be configured."
```

Violations identified:
1. **Underscore key names**: `server_config`, `host_name`, `port_number`, `max_connections` should use hyphens
2. **Custom subtables**: `[server_config.database_primary]` and `[server_config.database_replica]` should be table arrays
3. **Double quotes**: String values using double quotes without escapes needed
4. **Array formatting**: Long array on single line should be split across multiple lines
5. **Multi-line string**: Long description should use triple single quotes

Corrected version:
```toml
[[server-config]]
name = 'main'
host-name = 'localhost'
port-number = 8080
max-connections = 100

[[database]]
name = 'primary'
host = 'localhost'
port = 5432
connection-timeout = 30
retry-attempts = 3

[[database]]
name = 'replica'
host = 'localhost'
port = 5433
connection-timeout = 15
retry-attempts = 2

allowed-hosts = [
    'https://example.com',
    'https://api.example.com',
    'https://admin.example.com',
]

description = '''
This is a multi-line description that explains what this service does 
and how it should be configured.
'''
```

## Review Report Format

Phase 1 Output:
1. **Compliance Summary**: Overall assessment with file-by-file breakdown
2. **Standards Violations**: Categorized list with specific line references and explanations
3. **Configuration Analysis**: Table organization and key naming assessments
4. **Remediation Plan**: Systematic order of fixes to be applied
5. **Risk Assessment**: Any changes that require careful validation

Phase 2 Output:
1. **Applied Fixes**: Summary of all changes made, categorized by standard
2. **Files Modified**: Complete list with brief description of changes
3. **Manual Review Required**: Any issues requiring human judgment

## Conformance Process

### 1. Analysis Phase (PHASE 1)
- Examine target files to understand current state
- Identify configuration design patterns that need updating
- Generate comprehensive compliance report
- **Requirements**: Complete review and report before any remediation
- **Focus**: Reference specific lines with concrete examples and explain reasoning

### 2. Systematic Correction (PHASE 2)
Apply fixes in systematic order:
1. **Key Naming**: Convert underscores to hyphens in key names
2. **Table Organization**: Convert custom subtables to table arrays with `name` fields
3. **String Quoting**: Change double quotes to single quotes (unless escapes needed)
4. **Multi-line Strings**: Convert to triple single quotes format
5. **Array Formatting**: Split long arrays across multiple lines with proper indentation
6. **Nomenclature**: Apply naming guidelines to keys and table names

**Requirements**: 
- Maintain exact functionality while improving standards adherence
- Validate that configuration files remain syntactically valid
- Preserve all semantic meaning of configuration values

## Safety Requirements

Stop and consult if:
- Configuration structure changes would alter application behavior
- Complex nested configurations require architectural decisions
- File contains domain-specific conventions that conflict with general guidelines
- Syntax errors occur during modification

Your responsibilities:
- Maintain exact functionality while improving practices/style
- Use project patterns consistently per the guides
- Reference TOML documentation guides for complex cases
- Verify all changes preserve configuration semantics

## Success Criteria

- [ ] All key names use hyphens instead of underscores
- [ ] Custom subtables converted to table arrays where appropriate
- [ ] String values use single quotes (double only when escapes needed)
- [ ] Multi-line strings use triple single quotes
- [ ] Long arrays are properly formatted across multiple lines
- [ ] Nomenclature guidelines applied to keys and table names
- [ ] No functionality changes to configuration behavior
- [ ] Files remain syntactically valid TOML

## Final Report

Upon completion, provide a brief report covering:
- Specific conformance issues corrected (categorized by the priority issues above)
- Number of files modified
- Any patterns that required manual intervention
- Any deviations from guides and justification