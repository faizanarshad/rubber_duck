# Tool Health Sentinel

Record:

```text
get_started status
detailed_repo_analysis status
semantic_mode
commit
instance_id
phase1/phase2 readiness
load coverage
cache_stats
pending eviction notices
analysis_id map
tool spillovers
parser degradation
CI fusion availability
```

## Cache warning

If cache utilization is high or eviction notices exist, do not call the cache "empty." Report exact values and confirm the target analysis_id after load.

## Degraded output

Semantic-only clean is not a security/impact negative if CI fusion failed.

## Tool health table

| Tool | Status | Evidence | Impact |
|---|---|---|---|
