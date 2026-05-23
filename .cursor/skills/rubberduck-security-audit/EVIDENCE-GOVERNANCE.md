# Evidence Governance

Evidence governance turns AI security output into auditable engineering output.

## Evidence classes

```text
Tier-2 runtime/fixture/loopback validation
source-confirmed
graph-confirmed
search-confirmed
manual review
unsupported
out of scope
```

## Evidence ledger

Record:

```text
source reads
search queries
search scopes
match counts
graph traces
control guards
call chains
taint flows
tool health
unsupported surfaces
runtime PoCs
prior-run reconciliation
```

## Negative claims

Every "no X found" claim needs:

```text
claim
patterns searched
scope
tool
match count
unsupported surfaces
confidence
invalidating condition
```

Example:

```text
Claim: no unsafe YAML loader found in supported Python surface.
Patterns: yaml.load|UnsafeLoader|FullLoader
Scope: all loaded Python analyses
Matches: 0 unsafe loaders, safe_load only
Unsupported: shell/YAML workflow files reviewed separately
Confidence: high for Python, not for external dependencies
```

## Prohibited unsupported claims

Do not say:

```text
no vulnerabilities found
no auth issue
no unsafe deserialization
no subprocess risk
no SSRF
no model-loader risk
```

unless evidence exists for the searched scope and unsupported surfaces are caveated.
