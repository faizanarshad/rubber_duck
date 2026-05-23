# CLAUDE.md Snippet for Claude Code

```markdown
<!-- RUBBERDUCK-SKILLS:START -->
## RubberDuck Skills

Before any RubberDuck-backed workflow, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and run `detailed_repo_analysis(..., semantic_mode="full")` on that `owner/repo` until the complete CI semantic full report exists. Local indexing is only a post-CI fallback for semantic loading gaps, not a substitute for Codebase Intelligence Phase 2.

When a response is primarily powered by a RubberDuck skill, start the response with `🦆` as described in `RUBBERDUCK-RESPONSE-MARKER.md`.

When the user is unsure which RubberDuck skill to use, or the task likely needs multiple RubberDuck skills, read `RUBBERDUCK-SKILL-ADVISOR.md`, recommend an ordered skill sequence, and ask the user to approve review-each-phase, planning-with-signoff, or bounded autonomous mode before long-running execution. For builds, also ask whether the scope is local-only, step-by-step GitHub-validated, or autonomous bounded GitHub-validated unless already clear.

When starting a fresh repo session and the user asks for setup, initialization, or onboarding after installation, use `START_REPO_SESSION_PROMPT.md` as the human-facing bootstrap prompt for the Skill Advisor.

For GitHub-validated builds, autonomous builds, and final PR security sweeps, read `RUBBERDUCK-SECURITY-DELTA-GATE.md`. Compare RubberDuck base vs PR-head findings, fix true-positive new Critical/High findings in changed/new code, adjudicate false positives, and keep pre-existing findings separate from the PR readiness gate.

Use `rubberduck-codebase-atlas-pro` for codebase understanding, architecture mapping, entry points, call chains, data flows, and onboarding reports.

Use `rubberduck-change-impact-pro` for change impact analysis, affected callers/callees, blast radius, tests to run, safe change order, and runtime-preserving optimization opportunities for a change.

Use `rubberduck-doppelganger-hunt-pro` for semantic duplicate-intent discovery, behavioral twins, doppelganger hunts, hidden canonical helpers, inline reimplementations, and unification/refactor planning.

Use `rubberduck-mirror-pro` for bounded behavioral equivalence checks, refactor safety, AI patch replacement verification, and before/after behavior drift analysis.

Use `rubberduck-schema-code-api-drift-pro` for schema drift, API contract drift, DB/type/API consistency, model-field mismatch, nullability/default/validation drift, generated-client breakage, migration risk, and schema-code-api comparison.


Use `rubberduck-feature-planner-pro` for tests-first feature planning, sealed_plan.json creation, Fit Pack + semantic enrichment, integration point selection, and signoff-ready plans.

Use `rubberduck-feature-builder-pro` for consuming sealed plans and building production code under a machine-readable Spec Heartbeat, worktree safety, regression revert, drift/doppelganger gates, and PR_READY.diff emission.

Use `rubberduck-autonomous-feature-mode` for bounded autonomous Plan + Build orchestration under an explicit autonomy envelope.

Use `rubberduck-security-audit` for repository security audits, vulnerability hunts, pentest-style reviews, scanner finding validation, and defensible security reports.

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

Before running any workflow, read the installed skill's `SKILL.md` and follow it exactly.
<!-- RUBBERDUCK-SKILLS:END -->
```
