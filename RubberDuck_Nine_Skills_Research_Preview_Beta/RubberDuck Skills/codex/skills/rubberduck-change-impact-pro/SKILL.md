---
name: rubberduck-change-impact-pro
description: Evidence-governed RubberDuck change impact analysis skill. Uses codebase intelligence + semantic intelligence with semantic_mode="full" to analyze what breaks when a target function/file/symbol changes. Produces an impact report, evidence pack, impact-summary.json, risk score, affected callers/callees/shared state, tests to run, change order, mock/comment/public-API impacts, rare-signal discoveries, and runtime optimization opportunities.
trigger: when the user asks what breaks if a function/file/symbol/API changes, wants change impact analysis, blast radius, affected callers/callees, shared state, tests to run, migration order, safe change plan, or runtime-preserving optimization opportunities for a change
version: 2026-05-22-change-impact-pro-v3.2
---

# RubberDuck Change Impact Pro

Use this skill for UC-05 Change Impact Analysis.

This is not a generic "grep usages" prompt. It is an evidence-governed impact workflow:

```text
target/change request
  -> RubberDuck codebase + semantic intelligence
  -> target resolution
  -> repo-specific impact prompt
  -> dual-source caller/callee adjudication
  -> shadow/doppelganger preflight
  -> shared-state and data-flow trace
  -> mock/comment/public-API/test impact
  -> quality and rare-signal sweep
  -> runtime optimization opportunity pass
  -> evidence pack + impact-summary.json
  -> final impact report
```

## Dual-Source Adjudication banner

Dual-Source adjudication is load-bearing. Do not trust a single impact channel when caller/callee/source/search evidence can be reconciled.

## RubberDuck CI bootstrap gate

Before any RubberDuck Codebase Intelligence or Semantic Intelligence call, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and run `detailed_repo_analysis(..., semantic_mode="full")` on that `owner/repo` until the complete CI semantic full report exists.

Local indexing, scratch loads, and `local/...` aliases are only post-CI fallbacks for semantic loading gaps. They are not Codebase Intelligence Phase 2 and must be labeled as degraded evidence.

## RubberDuck response marker

When this skill produces a RubberDuck-powered status, blocker, validation summary, evidence report, or final answer, start the response with `🦆`. The marker is required only for RubberDuck-powered skill output; ordinary package maintenance or non-RubberDuck responses should not use it. See `RUBBERDUCK-RESPONSE-MARKER.md`.

## RubberDuck skill advisor

If the user is unsure which RubberDuck skill to use, or impact analysis should continue into duplicate discovery, equivalence validation, feature planning, build, or autonomous mode, use `RUBBERDUCK-SKILL-ADVISOR.md` to recommend the next skill order and ask for approval before multi-skill execution.

## Non-negotiable operating rules

1. **Use RubberDuck codebase intelligence and semantic intelligence.**
2. **Use `semantic_mode="full"` for codebase intelligence.**
3. **Do not silently fall back to generic source reading.** Source-read fallback is allowed only when explicitly approved or when labeled as degraded.
4. **Do not interrupt halfway.** Ask once up front for truly missing target/change information, then proceed.
5. **Do not trust one tool result alone.** Caller/callee impact must use dual-source adjudication when possible.
6. **Do not mark `assess(mode="impact")`, `plan_change`, or `call_chain` as authoritative if `search_code` / source reads contradict them.**
7. **Every major claim needs an evidence label.**
8. **Every negative claim needs search pattern, scope, match count, and caveat.**
9. **Every report must include impact-summary.json in DEEP mode.**
10. **Every report must include runtime optimization opportunities for the target and high-impact affected functions, while preserving exact observable behavior or documented ±5% tolerance.**

## Default budget

Default mode is **DEEP**.

```text
DEEP: up to 200 tool calls if needed.
STANDARD: ~60 calls.
QUICK: ~30 calls.
```

Do not reduce DEEP evidence collection to save tool calls. Optimize tool usage only through batching, deduping equivalent searches, and reusing evidence.

## Required inputs

Minimum useful input:

```text
target function/class/symbol/file
desired change description
```

Optional:

```text
change type: rename / signature / behavior / deprecate / remove / move / optimize / unknown
branch/commit/diff
migration window
public/internal classification
known constraints
must-not-change list
```

If required information is missing:

```text
Ask once at the start.
If the target can be resolved from the description, proceed and document target-resolution confidence.
Do not ask mid-run unless multiple plausible production targets remain unresolved.
```

## Change type playbooks

Load `CHANGE-TYPE-PLAYBOOKS.md`.

Default inference:

```text
rename      -> imports, exports, mocks, docs/comments, aliases, test names
signature   -> call shapes, optional/default params, overloads, interface contracts
behavior    -> invariants, state, tests, comments, runtime optimization, edge cases
deprecate   -> public API, downstream consumers, migration window, warning path
remove      -> public API, dead-code proof, external usage, semver/migration
move        -> barrel exports, path aliases, imports, circular dependencies
optimize    -> exactness/tolerance, benchmarking/profiling plan, equivalence tests
unknown     -> run generic impact + classify likely change type
```

## Mandatory report sections

Final report must include:

```text
§0 Impact Summary
§0.5 Shadow / Doppelganger Pre-flight
§1 Target Resolution
§2 Proposed Change Understanding
§3 Caller Impact
§4 Callee / Downstream Impact
§5 Shared State / Data Flow
§6 Public API / Export / Config / Deploy Impact
§7 Mock Breakage Taxonomy
§8 Test Impact Matrix
§9 Risk Score
§10 ★ Comment Contract
§11 Rare / High-Value Signals
§12 Runtime Optimization Opportunities
§13 Recommended Change Order
§14 Tests to Run
§15 Rollback / Migration Plan
§16 Unknowns / Unsupported Surfaces
§17 Claim Ledger and Negative Claims
§18 Falsification Recipes
§19 Paste-Ready PR Description
```

## Required evidence pack

DEEP mode must produce:

```text
REPORT.md
impact-summary.json

evidence/
  tool-health.md
  tool-calls.md
  target-resolution.md
  dual-source-adjudication.md
  search-results.md
  source-snippets.md
  callers.md
  callees.md
  shared-variables.md
  data-flows.md
  module-state.md
  comment-contracts.md
  mock-breakage.md
  public-api-proof.md
  test-coverage-matrix.md
  rare-signals.md
  runtime-optimization.md
  quality-scorecard.md
  evidence-reuse-ledger.md
  unsupported-surfaces.md
  claim-ledger.md
  negative-claims.md
  falsification-recipes.md
```

If a file is not applicable, create it with an explicit "Not applicable" reason.

## Key success criteria

A good Change Impact Pro report should answer:

```text
What exactly is being changed?
Who calls it?
What does it call?
What state does it share?
What variables/data flow through it?
What tests and mocks break?
What comments/contracts become stale?
Is it public API?
Are there shadow implementations?
What rare/signature-impacting signals exist?
Can the target or affected functions be optimized without changing behavior?
What is the safe change order?
What tests should run?
What should the PR description say?
What claims are unsupported or tool-degraded?
```

## Quality and runtime optimization

Every run must include:

```text
Correctness Maximization pass
Data-Quality Scorecard
Rare / High-Value Feature Discovery pass
Runtime Optimization Opportunity pass
Evidence Reuse Ledger
```

Runtime optimization rule:

```text
Ask whether the target function and high-impact affected functions can be optimized.
Require same observable result.
Use 0% tolerance for deterministic exact outputs.
Use ±5% only when approximate equivalence is explicitly appropriate.
Do not let optimization analysis replace impact analysis.
```

## Files to read

Start with this file, then load only the references needed:

```text
RUBBERDUCK-WORKFLOW.md
TARGET-RESOLUTION.md
IMPACT-PROMPT-COMPILER.md
IMPACT-WORKFLOW.md
DUAL-SOURCE-ADJUDICATION.md
SHADOW-PREFLIGHT.md
CHANGE-TYPE-PLAYBOOKS.md
COMMENT-CONTRACTS.md
MOCK-BREAKAGE.md
IMPACT-RISK-SCORING.md
RUNTIME-OPTIMIZATION.md
EVIDENCE-PACK.md
REPORT-TEMPLATE.md
```

Always apply:

```text
EVIDENCE-GOVERNANCE.md
CLAIM-FIREWALL.md
TOOL-HEALTH-SENTINEL.md
UNSUPPORTED-SURFACE-ROUTER.md
VALIDATION-REPORTING.md
```
