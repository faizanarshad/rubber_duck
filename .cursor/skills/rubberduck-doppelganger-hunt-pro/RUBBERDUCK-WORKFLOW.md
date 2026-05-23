# RubberDuck Workflow

## Required start

Run the strongest codebase-intelligence path first:

Read `RUBBERDUCK-CI-BOOTSTRAP.md` before setup. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and use that `owner/repo` for all Codebase Intelligence calls. Local indexing is only a post-CI fallback for semantic loading gaps; it is not a substitute for Codebase Intelligence Phase 2.

```python
get_started(repo="<owner/repo or authorized mirror>")

detailed_repo_analysis(
    repo="<owner/repo or authorized mirror>",
    branch="<branch>",
    semantic_mode="full",
)
```

Poll readiness:

```python
get_started(repo="<owner/repo or authorized mirror>")
```

Load semantic source:

```python
load_code(
    repo="<owner/repo or authorized mirror>",
    instance_id="<instance_id>",
    max_files=2000,
    file_pattern="*.ts",
)
```

Repeat for supported languages.

## Required tool families

Use available equivalents:

```text
search_code
read_source
query_action(symbols_overview)
query_action(call_chain)
query_action(trace_variable)
query_action(control_guards)
query_action(def_sites / reaching_defs when available)
assess(mode="repo_detailed")
assess(mode="security")
logic_analysis
analyze_code
get_evidence_pack
```

## Tool limits and fallbacks

If cross-file `analyze_code` fuzzy-matches to the wrong analysis:

```text
Run analyze_code separately per analysis_id and compose pair comparison client-side.
Do not claim cross-analysis compare from one fuzzy tool call.
```

If per-function centrality/dominator metrics are unavailable:

```text
Use repo_detailed graph metrics when possible.
Otherwise use caller-count/fan-in/fan-out proxy and label F4 as approximated.
```

If line-by-line CDG or reaching-defs is too expensive:

```text
Run them only on the short-list of candidate pairs that already pass prefilter.
Mark F5/F6 skipped/unavailable if not computed.
Do not include them in composite score.
```

If `load_code` overflows or truncates:

```text
Record truncation.
Use targeted file loads and source reads.
Build candidate ledger from search_code + local grep only if user approved local fallback.
```

## Tool health

Every run must record:

```text
commit
instance_id
loaded analyses
files loaded by language
codebase-intelligence status
semantic-intelligence status
parser failures
output truncation
cache/eviction signs
unsupported surfaces
```
