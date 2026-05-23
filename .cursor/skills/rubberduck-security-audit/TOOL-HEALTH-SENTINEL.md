# Tool Health Sentinel

Tool state is security evidence. A claim is only as strong as the tool state behind it.

## Track

```text
index freshness
commit match
instance_id
phase1/phase2 readiness
CI fusion availability
semantic load coverage
analysis-ID collisions
parser confidence
graph layer availability
tool output truncation
cache eviction
wrong-repo signs
fuzzy symbol corrections
unsupported file types
```

## Per-claim health labels

```text
source-confirmed, graph-confirmed
source-confirmed, graph-degraded
search-confirmed only
semantic-only clean, CI-fusion unavailable
manual review of unsupported surface
out of scope
```

## Degradation examples

```text
per-file assess clean but CI fusion failed -> not a negative finding
TypeScript parser failed -> source-read confirmation required
search output truncated -> rerun narrower
load_code wrong repo -> stop
cached detailed report for matching commit -> acceptable
cached report for wrong commit -> stop
```
