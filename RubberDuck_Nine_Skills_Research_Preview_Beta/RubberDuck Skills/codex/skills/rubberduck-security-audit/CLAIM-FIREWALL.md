# Claim Firewall

Before final answer, build a claim ledger and block unsupported claims.

## Claim ledger format

```text
Claim | Evidence class | Evidence pointer | Scope | Caveat | Allowed?
```

## Allowed evidence classes

```text
Tier-2 confirmed
source-confirmed
graph-confirmed
search-confirmed
manual review
unsupported
out of scope
```

## Blocking rules

Block or caveat claims that:

```text
exceed tool coverage
ignore parser/tool degradation
lack source evidence
make negative claims without searches
drop prior-run findings silently
downgrade team-reviewed High/Critical prior findings without a dedicated downgrade note
classify supply-chain code execution on artifact-producing hosts below High without proving no credential access and no artifact influence
call a report complete after failed Tier-2 on P0/P1
merge variants without preserving variant rows
say "clean" after semantic-only degraded results
```

## Final answer rule

The final report may include only:

```text
allowed claims
claims with caveats
out-of-scope statements
open/incomplete status
```

Unsupported claims must be removed or marked unsupported.
