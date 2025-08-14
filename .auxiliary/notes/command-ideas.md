# Custom Slash Command Ideas

Collection of potential custom slash commands to implement based on focused role specialization.

## Implementation Priority

### **Phase 1 - High Value, Ready to Implement:**
1. **`cs-review-todos`** - Collect, organize, and analyze TODO comments across the project
2. **`cs-audit-security`** - Deep security review with threat modeling, attack surface analysis, credential handling patterns

### **Phase 2 - Medium Priority:**
3. **`cs-reconcile-prd`** - Analyze and validate existing requirements for completeness, conflicts, and traceability gaps
4. **`cs-audit-designs`** - Architectural coherence, design pattern consistency, component relationships

### **Phase 3 - Lower Priority:**
5. **`cs-audit-practices`** - Code practices beyond linters - naming consistency, error handling patterns, immutability adherence
6. **`cs-performance-profile`** - Analyze performance bottlenecks (useful in specific cases)

## Rejected/Deferred Ideas

### Covered by Existing Tools
- `cs-prepare-pr` - Pre-commit and pre-push hooks handle this
- `cs-coverage-report` - Already handled via automated tooling
- `cs-analyze-dependencies` - Better served as automated GitHub workflow

### Redundant with Existing Commands
- `cs-integrator` - Covered by cs-architect (system boundaries) and cs-design-python (module interfaces)
- `cs-trace-requirements` - Should be unnecessary if other commands are used correctly

These commands follow the "focused roles with just the documentation they need"
philosophy, where each command loads specific `@`-references relevant to its
domain and avoids context pollution.
