# AGENTS.md Snippet for Codex

```markdown
<!-- RUBBERDUCK-SKILLS:START -->
## RubberDuck Skills

Before any RubberDuck-backed workflow, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and run `detailed_repo_analysis(..., semantic_mode="full")` on that `owner/repo` until the complete CI semantic full report exists. Local indexing is only a post-CI fallback for semantic loading gaps, not a substitute for Codebase Intelligence Phase 2.

When a response is primarily powered by a RubberDuck skill, start the response with `🦆` as described in `RUBBERDUCK-RESPONSE-MARKER.md`.

When the user is unsure which RubberDuck skill to use, or the task likely needs multiple RubberDuck skills, read `RUBBERDUCK-SKILL-ADVISOR.md`, recommend an ordered skill sequence, and ask the user to approve review-each-phase, planning-with-signoff, or bounded autonomous mode before long-running execution. For builds, also ask whether the scope is local-only, step-by-step GitHub-validated, or autonomous bounded GitHub-validated unless already clear.

When starting a fresh repo session and the user asks for setup, initialization, or onboarding after installation, use `START_REPO_SESSION_PROMPT.md` as the human-facing bootstrap prompt for the Skill Advisor.

For GitHub-validated builds, autonomous builds, and final PR security sweeps, read `RUBBERDUCK-SECURITY-DELTA-GATE.md`. Compare RubberDuck base vs PR-head findings, fix true-positive new Critical/High findings in changed/new code, adjudicate false positives, and keep pre-existing findings separate from the PR readiness gate.

When the user asks to understand a codebase, map architecture, identify entry points, trace request/data flow, or produce a Codebase Atlas, use `rubberduck-codebase-atlas-pro`.

When the user asks what will break if a function/file/symbol/API changes, wants change impact analysis, affected callers/callees, blast radius, tests to run, safe change order, or runtime-preserving optimization opportunities for a change, use `rubberduck-change-impact-pro`.

When the user asks to find duplicate intent, semantic duplicates, behavioral twins, doppelgangers, hidden canonical helpers, inline reimplementations, duplicate behavior under different names/shapes, or PR-ready unification/refactor plans, use `rubberduck-doppelganger-hunt-pro`.

When the user asks whether two implementations are equivalent, whether a refactor preserves behavior, whether an AI patch is safe, whether one helper can replace another, or whether before/after code has behavioral drift, use `rubberduck-mirror-pro`.

When the user asks for schema drift, API contract drift, DB/type/API consistency, model-field mismatch, nullability/default/validation drift, generated-client breakage, migration risk, or schema-code-api comparison, use `rubberduck-schema-code-api-drift-pro`.


When the user asks to plan a new feature, design tests first, create a sealed plan, produce sealed_plan.json, find where a feature belongs, or prepare a Feature Builder contract, use `rubberduck-feature-planner-pro`.

When the user provides sealed_plan.json plus SIGNOFF.json/AUTO_AUTHORIZATION.json, asks to build from a sealed plan, generate production code under Spec Heartbeat, or produce PR_READY.diff, use `rubberduck-feature-builder-pro`.

When the user asks for autonomous plan-and-build mode, auto mode, bounded autonomous feature implementation, or Plan plus Build orchestration under an autonomy envelope, use `rubberduck-autonomous-feature-mode`.

When the user asks for a security audit, vulnerability hunt, pentest-style review, CWE/CVE-style report, scanner finding validation, or defensible security report, use `rubberduck-security-audit`.

Routing precedence for ambiguous prompts:
1. `sealed_plan.json` plus a build request -> `rubberduck-feature-builder-pro`
2. autonomy envelope / autonomous plan and build -> `rubberduck-autonomous-feature-mode`
3. equivalence or replacement -> `rubberduck-mirror-pro`
4. duplicate intent or duplicate behavior -> `rubberduck-doppelganger-hunt-pro`
5. schema / type / API drift -> `rubberduck-schema-code-api-drift-pro`
6. security audit -> `rubberduck-security-audit`
7. change impact -> `rubberduck-change-impact-pro`
8. tests-first feature planning -> `rubberduck-feature-planner-pro`
9. architecture / codebase understanding -> `rubberduck-codebase-atlas-pro`

Before running any workflow, read the installed skill's `SKILL.md` and follow it exactly. Do not interrupt halfway after setup/loading/discovery unless the target is missing or RubberDuck tooling blocks the primary report.
<!-- RUBBERDUCK-SKILLS:END -->
```
