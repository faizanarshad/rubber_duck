---
name: rubberduck-mirror-pro
description: RubberDuck Mirror Pro: an evidence-governed Codex/Claude/Cursor skill for bounded behavioral equivalence checks. Use to compare before/after implementations, sibling functions, AI-generated replacements, refactors, and candidate duplicate implementations. Uses RubberDuck codebase intelligence and semantic intelligence with semantic_mode="full", import-context analysis, path reconciliation, side-effect and exception-envelope diffs, witness generation, test-suite generation, verdict taxonomy, evidence packs, and strict validators.
trigger: when the user asks whether two implementations are equivalent, whether a refactor preserves behavior, whether an AI patch is safe, whether a duplicate/helper can replace another, or whether before/after code has behavioral drift
version: 2026-05-22-rubberduck-mirror-pro
---

# RubberDuck Mirror Pro

RubberDuck Mirror Pro answers one question:

```text
Can implementation B safely replace implementation A under an explicit preserved contract?
```

This skill is not a duplicate detector. It is an **equivalence checker** for candidate replacements.

Use it after Codebase Atlas, Change Impact, Doppelganger Hunt, code review, or AI patch generation when you need to know whether two implementations actually preserve behavior.

## Core principle

Do not say "equivalent" without a contract.

Every verdict must be framed as:

```text
Equivalent / not equivalent / undecidable under <preserved_contract>
```

Allowed contracts:

```text
observable-behavior
outputs-only
side-effects-only
exception-envelope
full-functional
test-suite-compatible
```

## Required modes

Declare exactly one mode:

```text
rename-refactor
  Same symbol across commits/branches or a direct rename.

sibling-equivalence
  Two different functions/helpers claimed to be interchangeable.

ai-patch-verify
  Original implementation vs AI-generated or manually edited replacement.

cross-language
  Same intent across languages; advisory only unless semantics are strictly bounded.
```

Cross-language mode must be labeled `HEURISTIC_ONLY` or `UNDECIDABLE` unless the report proves a narrow shared contract.

## RubberDuck CI bootstrap gate

Before any RubberDuck Codebase Intelligence or Semantic Intelligence call for a repo-backed comparison, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and run `detailed_repo_analysis(..., semantic_mode="full")` on that `owner/repo` until the complete CI semantic full report exists.

Local indexing, scratch loads, and `local/...` aliases are only post-CI fallbacks for semantic loading gaps. They are not Codebase Intelligence Phase 2 and must be labeled as degraded evidence. Direct scratch/snippet comparisons may proceed only as source/scratch evidence, not as a completed RubberDuck CI comparison.

## RubberDuck response marker

When this skill produces a RubberDuck-powered status, blocker, validation summary, evidence report, or final answer, start the response with `🦆`. The marker is required only for RubberDuck-powered skill output; ordinary package maintenance or non-RubberDuck responses should not use it. See `RUBBERDUCK-RESPONSE-MARKER.md`.

## RubberDuck skill advisor

If the user is unsure which RubberDuck skill to use, or an equivalence result should continue into change impact, planning, build, or autonomous mode, use `RUBBERDUCK-SKILL-ADVISOR.md` to recommend the next skill order and ask for approval before multi-skill execution.

## Non-negotiable rules

1. Use RubberDuck codebase intelligence and semantic intelligence with `semantic_mode="full"` when available.
2. Do not interrupt halfway after target resolution unless target specs are missing or RubberDuck blocks the primary report.
3. Read import/module context before body comparison.
4. Enumerate comparable paths before rendering verdict.
5. Compare outputs, side effects, exceptions, resource lifecycle, async/concurrency behavior, and observable state when in scope.
6. Generate witness inputs or explain why witness synthesis is blocked.
7. Generate regression tests or explain why test generation is blocked.
8. Never claim formal proof unless all required paths and dimensions are computed and no blockers remain.
9. Do not let similarity imply equivalence. Doppelganger Hunt finds candidates; Mirror validates or rejects replacement safety.
10. Run validators before final response.

## Verdict taxonomy

Use exactly one:

```text
PROVEN_EQUIVALENT_UNDER_CONTRACT
NOT_EQUIVALENT
CONDITIONALLY_EQUIVALENT
EQUIVALENT_WITH_STRUCTURAL_DRIFT
UNDECIDABLE
HEURISTIC_ONLY
```

## Required report sections

```text
§0 Envelope
§1 Verdict
§2 Headline Divergence or Equivalence Basis
§3 Input / Contract / Scope
§4 Import and Module Context
§5 Path Catalogue
§6 Path-Match Table
§7 Divergences
§8 Side-Effect Manifest Diff
§9 Exception Envelope Diff
§10 Witness Inputs
§11 Generated Regression Tests
§12 Undecidable Blockers
§13 Structural Drift
§14 Falsification Recipes
§15 Tool Health and Coverage
§16 Evidence Pack Status
```

## Required evidence pack

DEEP reports must produce or explicitly block:

```text
evidence/mirror-summary.json
evidence/before-source.md
evidence/after-source.md
evidence/import-context.md
evidence/path-catalogue-before.md
evidence/path-catalogue-after.md
evidence/path-match-table.md
evidence/side-effect-manifest.md
evidence/exception-envelope.md
evidence/witness-inputs.md
evidence/generated-tests.md
evidence/undecidable-blockers.md
evidence/structural-drift.md
evidence/falsification-recipes.md
evidence/tool-health.md
evidence/protocol-completion.md
```

If a file cannot be generated, create it with:

```text
Status: unavailable
Reason:
Impact on verdict:
```

## Skill files

Read as needed:

```text
RUBBERDUCK-WORKFLOW.md
MIRROR-WORKFLOW.md
INPUT-CONTRACTS.md
IMPORT-CONTEXT.md
PATH-ENUMERATION.md
SIDE-EFFECT-MANIFEST.md
EXCEPTION-ENVELOPE.md
WITNESS-GENERATION.md
TEST-SUITE-GENERATION.md
VERDICT-TAXONOMY.md
EVIDENCE-GOVERNANCE.md
CLAIM-FIREWALL.md
TOOL-HEALTH-SENTINEL.md
REPORT-TEMPLATE.md
```

## Default use prompt

```text
Use rubberduck-mirror-pro.
Target repo/path/commit:
Before implementation:
After implementation:
Preserved contract:
Mode:
```

If mode or contract is omitted, infer the safest candidate and state it, but do not invent target implementations.
