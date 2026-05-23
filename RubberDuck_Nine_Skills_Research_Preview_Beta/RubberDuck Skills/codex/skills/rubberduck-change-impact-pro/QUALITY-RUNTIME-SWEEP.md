# Quality and Runtime Sweep

This sweep maximizes correctness, data quality, rare feature discovery, and runtime optimization opportunities.

## Correctness maximization

Before final output:

```text
reconcile contradictory tool outputs
source-read top-impact callers
confirm public/internal classification
confirm tests/mocks
confirm comments/contracts
confirm unsupported surfaces
```

## Data-quality scorecard

Report:

```text
target resolution confidence
caller coverage confidence
callee coverage confidence
shared-state confidence
test discovery confidence
mock discovery confidence
public API confidence
tool health confidence
unsupported-surface caveat
```

## Rare / high-value signals

Search for:

```text
shadow implementations
comment contracts
mock factories
barrel exports
path aliases
feature flags
migration/deprecation notes
runtime env vars
TOCTOU/race comments
unsupported language references
silent dependency on string names
```

## Evidence reuse ledger

Record where evidence was reused instead of rerunning equivalent calls:

```text
evidence source
claims supported
tool calls saved
risk of reuse
```

Do not skip required evidence in DEEP mode merely to save calls.
