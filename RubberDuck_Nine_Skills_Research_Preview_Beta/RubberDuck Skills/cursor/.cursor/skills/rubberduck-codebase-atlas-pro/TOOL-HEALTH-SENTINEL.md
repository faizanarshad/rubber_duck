# Tool Health Sentinel

Track tool health throughout.

Mirror tool health in `evidence/tool-health.md` for DEEP mode. The evidence manifest must state whether tool-health evidence is raw, normalized, or report-derived.

## Required table

```markdown
| Tool / Layer | Status | Evidence | Impact on claims | Workaround |
|---|---|---|---|---|
```

## Health dimensions

```text
index freshness
commit match
instance_id
semantic phase readiness
codebase-intelligence availability
load coverage
analysis_id collisions
parser degradation
CI/codebase fusion degradation
output truncation
wrong-repo signs
unsupported languages
```

## Claim impact

Examples:

```text
TypeScript parser degraded; source read confirms symbol table but call-chain confidence reduced.
Codebase metrics unavailable; structural ranking omitted.
Semantic tools unavailable; primary atlas blocked.
```
