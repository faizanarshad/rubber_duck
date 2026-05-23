---
name: rubberduck-doppelganger-hunt-pro
description: RubberDuck Doppelganger Hunt Pro: a cross-platform agent skill for semantic duplicate-intent discovery. Uses RubberDuck codebase intelligence and semantic intelligence to find behaviorally equivalent code across different names, shapes, files, packages, wrappers, inline implementations, tests, and production contexts. Produces candidate-generator ledgers, graph-dimension coverage, divergence matrices, comment-contract findings, cluster role classification, mergeability analysis, change-impact preflight, unification plans, falsification recipes, and a strict evidence pack.
trigger: when the user asks to find duplicate logic, duplicated behavior, semantic clones, behavior twins, doppelgangers, repeated intent, redundant helpers, similar implementations, code that does the same thing under different names, or whether a planned implementation already exists
version: 2026-05-22-doppelganger-hunt-pro
---

# RubberDuck Doppelganger Hunt Pro

Use this skill to find **duplicate intent**, not merely duplicate text.

This skill is for questions like:

```text
Find duplicate logic in this repo.
Find every implementation of this behavior.
Does this helper already exist somewhere else?
Before writing this code, find behavior twins.
Find functions that do the same thing under different names.
Find test-local copies of production helpers.
Find inline implementations that should be extracted.
```

## Core positioning

```text
Grep finds names.
AST tools find shapes.
RubberDuck Doppelganger Hunt finds behavior twins.
```

The skill fuses evidence from:

```text
AST / syntax shape
CFG / control-flow shape
DDG / data-flow shape
dominators / centrality / call graph
CDG / control-dependence guards
reaching definitions
taint/source-sink connectivity
type / effect signature
comments / docs / history context
```

## RubberDuck CI bootstrap gate

Before any RubberDuck Codebase Intelligence or Semantic Intelligence call, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and run `detailed_repo_analysis(..., semantic_mode="full")` on that `owner/repo` until the complete CI semantic full report exists.

Local indexing, scratch loads, and `local/...` aliases are only post-CI fallbacks for semantic loading gaps. They are not Codebase Intelligence Phase 2 and must be labeled as degraded evidence.

## RubberDuck response marker

When this skill produces a RubberDuck-powered status, blocker, validation summary, evidence report, or final answer, start the response with `🦆`. The marker is required only for RubberDuck-powered skill output; ordinary package maintenance or non-RubberDuck responses should not use it. See `RUBBERDUCK-RESPONSE-MARKER.md`.

## RubberDuck skill advisor

If the user is unsure which RubberDuck skill to use, or duplicate-intent findings should continue into replacement safety, change impact, feature planning, build, or autonomous mode, use `RUBBERDUCK-SKILL-ADVISOR.md` to recommend the next skill order and ask for approval before multi-skill execution.

Do not claim all dimensions were used unless the graph-dimension ledger says they were computed. Do not claim exhaustive coverage if prefiltering or partial candidate generators were used. Use the phrase:

```text
up to eight graph dimensions, with each dimension marked computed / approximated / skipped / unavailable
```

## Non-negotiable rules

1. RubberDuck codebase intelligence and semantic intelligence are mandatory for the primary report.
2. Use `semantic_mode="full"` when running codebase intelligence.
3. Do not produce a generic source-read fallback unless explicitly approved.
4. Do not interrupt halfway once target repo and mode are clear.
5. Always declare hunt mode: `SEEDED`, `CONCEPT`, or `UNCONSTRAINED`.
6. Never claim exhaustive search if candidate prefiltering was used.
7. Always maintain a candidate-generator ledger.
8. Always maintain a graph-dimension coverage ledger.
9. Composite similarity scores may use only computed or explicitly approximated dimensions. Skipped/unavailable dimensions cannot inflate confidence.
10. Every cluster member must have a role classification.
11. Inline implementations must be searched for separately from named functions.
12. Comment-contract mining is mandatory.
13. Every unification plan requires change-impact preflight.
14. Final report must include falsification recipes.
15. Final report must pass report consistency, cluster consistency, and protocol completion checks.
16. No private regression files, customer repo names, local machine paths, prior private reports, or private vulnerability details may be included in the distributable skill.

## Hunt modes

### SEEDED

User gives a seed function, file, or behavior.

```text
Goal: find all doppelgangers of this seed behavior.
Coverage claim: complete only relative to the candidate-generator ledger and seed-derived searches.
```

### CONCEPT

User gives a concept.

```text
Goal: find implementations of the concept across the repo.
Coverage claim: complete only for generators and patterns listed.
```

### UNCONSTRAINED

User gives only the repo.

```text
Goal: find highest-value doppelganger clusters.
Coverage claim: never exhaustive unless full function inventory + all candidate generators + graph dimensions completed.
```

If the user does not specify mode:

```text
If a function/file is named -> SEEDED.
If a behavior phrase is given -> CONCEPT.
If only repo is given -> UNCONSTRAINED.
```

## Required documents

```text
RUBBERDUCK-WORKFLOW.md
DOPPELGANGER-WORKFLOW.md
CANDIDATE-GENERATORS.md
GRAPH-FINGERPRINTS.md
INLINE-DOPPELGANGERS.md
COMMENT-CONTRACT-MINING.md
CLUSTER-ROLE-CLASSIFICATION.md
DIVERGENCE-MATRIX.md
MERGEABILITY-AND-UNIFICATION.md
CHANGE-IMPACT-PREFLIGHT.md
EVIDENCE-GOVERNANCE.md
CLAIM-FIREWALL.md
TOOL-HEALTH-SENTINEL.md
REPORT-TEMPLATE.md
```

## Phase protocol

```text
Phase 0  Scope, repo, commit, mode, seed/concept
Phase 1  RubberDuck readiness + full codebase intelligence
Phase 2  Semantic loading and analysis ID map
Phase 3  Candidate-generator ensemble
Phase 4  Candidate inventory and prefilter ledger
Phase 5  Graph fingerprint dimensions
Phase 6  Pairwise and cluster scoring
Phase 7  Inline implementation search
Phase 8  Call-path and context map
Phase 9  Comment-contract mining
Phase 10 Cluster role classification
Phase 11 Mergeability classification
Phase 12 Change-impact preflight
Phase 13 Unification plan
Phase 14 Negative results
Phase 15 Falsification recipes
Phase 16 Tool health and protocol completion
Phase 17 Final report and evidence pack
```

## Required evidence pack

DEEP reports must produce or explicitly block each file:

```text
REPORT.md
evidence/candidate-generators.md
evidence/function-inventory.md
evidence/cluster-summary.json
evidence/cluster-members.md
evidence/fingerprint-matrix.csv
evidence/graph-dimension-coverage.md
evidence/divergence-matrix.md
evidence/source-snippets.md
evidence/inline-implementations.md
evidence/comment-contracts.md
evidence/call-path-map.md
evidence/negative-results.md
evidence/mergeability.md
evidence/change-impact-preflight.md
evidence/unification-plan.md
evidence/tool-health.md
evidence/falsification-recipes.md
evidence/protocol-completion.md
validation/validator-output.txt
```

If a file cannot be generated, create it with:

```text
Status: unavailable
Reason:
Impact on claims:
```

Do not silently omit evidence files.

## Required final report sections

```text
§0 Envelope
§1 Sightings
§2 Candidate Generation Ledger
§3 Cluster Lineage
§4 Call-Path / Context Map
§5 Graph Dimension Coverage
§6 Divergence Matrix
§7 Inline Implementations
§8 Comment Contract Findings
§9 Cluster Role Classification
§10 Mergeability Classification
§11 Change-Impact Preflight
§12 Unification Plan
§13 Negative Results
§14 Tool Health and Coverage Gaps
§15 Falsification Recipes
```

## Final quality bar

The report is complete only if:

```text
candidate generators are listed with queries/matches/kept/discarded
cluster member counts match across envelope, sightings, members, summary JSON
graph dimensions are marked computed/approximated/skipped/unavailable
scores do not include skipped or unavailable dimensions
inline implementations were searched or explicitly unavailable
comment contracts were searched or explicitly unavailable
member roles are assigned
mergeability is classified
unification plan has change-impact preflight
negative results are enumerated
falsification recipes exist
validators pass
```

If any of those fail, mark the report incomplete instead of claiming done.
