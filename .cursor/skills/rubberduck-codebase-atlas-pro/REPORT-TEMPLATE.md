# Codebase Atlas Report Template

```markdown
# <Repo> — RubberDuck UC1 Codebase Atlas

This is a Codebase Atlas, not a vulnerability report.
Security-sensitive flows are included as architecture boundaries.
They are not security-validated findings unless explicitly labeled.

## §0 Atlas Envelope / One-Screen Brief

| Field | Value |
|---|---|
| Repo/path | |
| Commit/branch | |
| Atlas mode | WHOLE_REPO_ATLAS / FEATURE_ATLAS |
| Feature target | none / <feature, file, endpoint, class, function, journey, behavior> |
| Budget | DEEP / STANDARD / QUICK |
| RubberDuck codebase intelligence | OK / degraded / unavailable |
| RubberDuck semantic intelligence | OK / degraded / unavailable |
| Supported semantic surface | |
| Codebase-intelligence surface | |
| Unsupported surfaces | |
| Runtime/deployment proof | proven by <tool> / not proven |
| Evidence pack | generated / report-only requested |
| Evidence level | raw tool output / normalized evidence / report-derived evidence |
| Evidence manifest | evidence/evidence-manifest.md |
| Raw tool output | evidence/raw-tool-output/ present / not exported |
| Machine summary | evidence/atlas-summary.json |
| Confidence summary | |

### Atlas coverage statement

- Semantic surface covered:
- Codebase-intelligence surface covered:
- Unsupported surfaces:
- Runtime/deployment behavior:

### What this repo does
...

### How to get oriented fast
...

### Feature focus

For FEATURE_ATLAS only:

- Feature description:
- Entry points:
- Symbols involved:
- Call chains:
- Data flow:
- State/config involved:
- External integrations:
- Tests related to the feature:
- Unresolved edges:
- Files to read first:
- Falsification recipes: see `evidence/falsification-recipes.md` or section below.

## §A Architectural Surprises

<At least 3 when evidence supports them; otherwise write: "This codebase contains no architectural surprises detectable by the selected rules and available evidence.">

Falsification recipe: <inline recipe or link to evidence/falsification-recipes.md>

## §1 Major Symbols

This is a curated major-symbol map. Full or near-full symbol evidence is in `evidence/symbols-overview.md`. If raw/complete symbol output is unavailable, say that explicitly and label the evidence level.

| Subsystem | File | Symbol | Kind | Line | Role | Evidence |
|---|---|---|---|---:|---|---|

Uninspected or unsupported files must be listed before claiming broad symbol coverage.

## §2 Entry Points

| Entry point | Type | File:line | Evidence | Call-chain status | Notes |
|---|---|---|---|---|---|

Falsification recipe: <inline recipe or link to evidence/falsification-recipes.md>

## §3 Call-Chain Atlas

```text
entry -> orchestrator -> subsystem -> output
```

Include exact RubberDuck calls and unresolved edges.

Falsification recipe: <inline recipe or link to evidence/falsification-recipes.md>

## §4 Data-Flow Atlas

```text
source object -> transform -> state/domain object -> output
```

Falsification recipe: <inline recipe or link to evidence/falsification-recipes.md>

## §5 Architectural Spine

Core files/functions ranked by evidence.

Falsification recipe: <inline recipe or link to evidence/falsification-recipes.md>

## §6 Articulation Points & Bridges

## §7 Communities / Subsystems

## §8 Cross-Package Coupling Map

### Cross-Package Coupling Evidence

| Edge | Source package/file | Target package/file | Tag | Evidence tool | Evidence detail | Confidence |
|---|---|---|---|---|---|---|

Tags: INTRA-PACKAGE, CROSS-PACKAGE, CROSS-LANGUAGE, EXTERNAL, UNKNOWN. Evidence tool must be one of: RubberDuck call-chain, RubberDuck search, source-read, package metadata, manual synthesis with caveat. Manual synthesis must be labeled and backed by source/search evidence.

Evidence file: `evidence/cross-package-coupling.md`.

Falsification recipe: <inline recipe or link to evidence/falsification-recipes.md>

## §9 God Nodes / Hot Files

## §10 Refactor Leverage

Only evidence-backed suggestions.

## §10.5 Bus-Factor Function

| Field | Value |
|---|---|
| Function / method | |
| File:line | |
| Why this is the bus-factor function | |
| Evidence | |
| Callers | |
| Callees | |
| Fan-in / fan-out | |
| Complexity / centrality / hot-file status | |
| Data-flow or taint-flow involvement | |
| What breaks if changed | |
| Tests to run before changing | |
| Safe modification plan | |
| Confidence | |

If unavailable, state: `Bus-Factor Function unavailable: <reason and missing evidence>`.

Evidence file: `evidence/bus-factor-function.md`. If exact graph centrality is unavailable, label the score as approximate / manual synthesis / RubberDuck metric-backed.

Falsification recipe: <inline recipe or link to evidence/falsification-recipes.md>

## §11 Dead / Duplicated / Untested / Unsupported

### Unsupported Surfaces

| Surface | Count/scope | Privilege | Coverage status | Review path | Claims exclude it? |
|---|---:|---|---|---|---|

Falsification recipe: <inline recipe or link to evidence/falsification-recipes.md>

## §12 Anti-Claims and Caveats

What this atlas does not claim.

## §13 30 / 60 / 180-Minute Reading Plan

### 30 minutes
...

### 60 minutes
...

### 180 minutes
...

## §14 Tool Health & Coverage Gaps

## §15 What RubberDuck Proved That Prose Would Guess

| Claim | RubberDuck evidence | Why generic reading would be weaker |
|---|---|---|

## Falsification Recipes

Use this section or link to `evidence/falsification-recipes.md`.

| Claim / section | Tool call or check to refute | Expected contradiction | Evidence file |
|---|---|---|---|
| Main entrypoint is X | query_action(call_chain, method=...) | different root caller or no path | call-chains.md |

## Evidence Ledger

| Claim | Evidence type | Tool/query | Scope | Confidence | Caveat |
|---|---|---|---|---|---|

## Appendix A — Full Symbol Inventory

Link to `evidence/symbols-overview.md` or include full/near-full `symbols_overview` inventory.

Distinguish:
- curated major symbols,
- full/near-full raw `symbols_overview` inventory when present,
- normalized or report-derived symbol evidence when raw output is absent,
- uninspected or unsupported files.

## Evidence Pack

```text
evidence/
  evidence-manifest.md
  tool-calls.md
  symbols-overview.md
  entry-points.md
  call-chains.md
  data-flows.md
  source-snippets.md
  structural-metrics.md
  unsupported-surfaces.md
  claim-ledger.md
  negative-claims.md
  tool-health.md
  falsification-recipes.md
  cross-package-coupling.md
  bus-factor-function.md
  atlas-summary.json
```

## Evidence Manifest

Link: `evidence/evidence-manifest.md`

```markdown
| Evidence file | Type | Source | Raw or derived? | Supports sections | Limitations |
|---|---|---|---|---|---|
| tool-calls.md | tool ledger | RubberDuck calls | raw / normalized / report-derived | §13, claim ledger | |
| symbols-overview.md | symbol evidence | symbols_overview | raw / normalized / report-derived | §1 | |
| falsification-recipes.md | falsification ledger | verifier plan | raw / normalized / report-derived | major sections | |
| atlas-summary.json | machine summary | report + evidence pack | normalized / report-derived | downstream consumers | |
```

Evidence levels:

```text
raw tool output
normalized evidence
report-derived evidence
```

Required `evidence/atlas-summary.json` in DEEP mode:

```json
{
  "repo": "",
  "commit": "",
  "mode": "WHOLE_REPO_ATLAS | FEATURE_ATLAS",
  "budget": "DEEP",
  "rubberduck": {
    "codebase_intelligence": "ok|degraded|unavailable",
    "semantic_intelligence": "ok|degraded|unavailable",
    "semantic_mode": "full",
    "coverage": {}
  },
  "repo_class": "",
  "primary_languages": [],
  "unsupported_surfaces": [],
  "entry_points": [],
  "major_symbols": [],
  "call_chains": [],
  "data_flows": [],
  "architectural_surprises": [],
  "bus_factor_function": {},
  "cross_package_edges": [],
  "reading_plan": {
    "30_min": [],
    "60_min": [],
    "180_min": []
  },
  "claims": {
    "supported": [],
    "negative": [],
    "unsupported": []
  },
  "evidence_files": [],
  "caveats": []
}
```
```
