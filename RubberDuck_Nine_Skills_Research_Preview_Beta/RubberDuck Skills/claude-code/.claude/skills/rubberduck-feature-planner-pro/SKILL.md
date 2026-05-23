---
name: rubberduck-feature-planner-pro
description: RubberDuck Feature Planner Pro creates immutable tests-first sealed feature plans. It uses RubberDuck codebase intelligence and semantic intelligence with semantic_mode="full", Fit Pack evidence, repo-specific pattern discovery, semantic enrichment, negative scope, tests-first design, duplicate-risk adjudication, and validation before halting for signoff. It does not write production code.
trigger: when the user wants to plan a new feature, design tests first, identify where a feature belongs, create a sealed implementation plan, produce a test-first feature plan, or prepare a build contract for Feature Builder Pro
version: 2026-05-feature-planner-pro
---

# RubberDuck Feature Planner Pro

This skill produces a **sealed, tests-first feature plan**. It does not write production implementation code.

The output is a contract consumed by `rubberduck-feature-builder-pro`.

```text
feature request
  -> codegen session + Fit Pack
  -> RubberDuck codebase/semantic enrichment
  -> pattern discovery
  -> integration point selection
  -> tests-first design
  -> sealed_plan.json
  -> halt for signoff
```

## RubberDuck CI bootstrap gate

Before any RubberDuck Codebase Intelligence or Semantic Intelligence call, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and run `detailed_repo_analysis(..., semantic_mode="full")` on that `owner/repo` until the complete CI semantic full report exists.

Local indexing, scratch loads, and `local/...` aliases are only post-CI fallbacks for semantic loading gaps. They are not Codebase Intelligence Phase 2 and must be labeled as degraded evidence.

## RubberDuck response marker

When this skill produces a RubberDuck-powered status, blocker, validation summary, evidence report, or final answer, start the response with `🦆`. The marker is required only for RubberDuck-powered skill output; ordinary package maintenance or non-RubberDuck responses should not use it. See `RUBBERDUCK-RESPONSE-MARKER.md`.

## RubberDuck skill advisor

If the user is unsure which RubberDuck skill to use, or planning should continue into user-controlled build or bounded autonomous mode, use `RUBBERDUCK-SKILL-ADVISOR.md` to recommend the next skill order and ask for approval before multi-skill execution.

## Hard rules

1. Use RubberDuck codebase intelligence and semantic intelligence with `semantic_mode="full"` when available.
2. Create or resume a codegen session before sealing.
3. Acquire and persist a Fit Pack, but treat it as starting evidence, not the whole truth.
4. Semantic enrichment must challenge Fit Pack bias.
5. Do not write production implementation code.
6. Produce tests first as `test_diff.patch`.
7. Declare planned files, off-limits files, reusable symbols, pattern anchors, acceptance criteria, effect manifest, command plan, and negative scope.
8. `sealed_plan.json` is immutable after PLAN mode.
9. Do not put mutable user signoff in `sealed_plan.json`.
10. Generate `SIGNOFF_TEMPLATE.json` separately.
11. Halt after producing the plan; BUILD owns code generation.

## Required inputs

```text
feature_description
repo/path
optional base_commit
optional constraints
optional tier: QUICK / STANDARD / DEEP
```

If repo/path or feature description is missing, ask once. Otherwise proceed without halfway interruption.

## Mandatory phases

```text
P0  Scope and source-of-truth pinning
P1  Codegen session start/resume
P2  Fit Pack acquisition and persistence
P3  RubberDuck codebase full scan and semantic loading
P4  Fit Pack gap analysis and semantic corrections
P5  Pattern discovery
P6  Integration point selection
P7  Negative scope / off-limits files
P8  Reusable symbol map
P9  Doppelganger / duplicate-risk preflight
P10 Tests-first design
P11 validate_generated_diff on test_diff
P12 sealed_plan.json generation
P13 SIGNOFF_TEMPLATE.json generation
P14 Halt for signoff
```

## Fit Pack bias rule

Fit Pack is a seed. The plan must include:

```text
Fit Pack suggested:
Semantic enrichment added:
Fit Pack missed:
Decision:
```

## Sealed plan immutability

`sealed_plan.json` must include `plan_sha256` over the canonical plan fields and must not be edited for signoff.

Use `SIGNOFF.json` later:

```text
sealed_plan_path
sealed_plan_sha256
approved
approved_by
approved_at
invoked_under
```

## Deliverable

```text
uc06/<slug>/
  PLAN.md
  sealed_plan.json
  plan-summary.json
  fit_pack.json
  test_diff.patch
  SIGNOFF_TEMPLATE.json
  evidence/
    tool-calls.md
    fit-pack-summary.md
    fit-pack-gaps.md
    pattern-discovery.md
    semantic-enrichment.md
    integration-point-selection.md
    off-limits.md
    reusable-symbols.md
    doppelganger-preflight.md
    negative-scope.md
    test-plan.md
    validation-result.md
    tool-health.md
    falsification-recipes.md
```

## Completion gate

PLAN mode is complete only when:

```text
sealed_plan.json exists
test_diff.patch exists
fit_pack.json exists or Fit Pack unavailability is documented
validate_generated_diff was run on the test diff or tool unavailability is documented
SIGNOFF_TEMPLATE.json exists
PLAN.md says BUILD has not started
end_codegen_session was not called
```
