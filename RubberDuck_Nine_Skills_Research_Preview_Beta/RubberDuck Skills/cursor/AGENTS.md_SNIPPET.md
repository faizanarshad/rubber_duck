# AGENTS.md Snippet for Cursor

```markdown
<!-- RUBBERDUCK-SKILLS:START -->
## RubberDuck Skills

Cursor rules are installed under `.cursor/rules/`.

Before any RubberDuck-backed workflow, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, mirror/push it to an authorized GitHub repository and run `detailed_repo_analysis(..., semantic_mode="full")` on that `owner/repo` until the complete CI semantic full report exists. Local indexing is only a post-CI fallback for semantic loading gaps, not a substitute for Codebase Intelligence Phase 2.

When a response is primarily powered by a RubberDuck skill, start the response with `🦆` as described in `RUBBERDUCK-RESPONSE-MARKER.md`.

When the user is unsure which RubberDuck skill to use, or the task likely needs multiple RubberDuck skills, read `RUBBERDUCK-SKILL-ADVISOR.md`, recommend an ordered skill sequence, and ask the user to approve review-each-phase, planning-with-signoff, or bounded autonomous mode before long-running execution. For builds, also ask whether the scope is local-only, step-by-step GitHub-validated, or autonomous bounded GitHub-validated unless already clear.

When starting a fresh repo session and the user asks for setup, initialization, or onboarding after installation, use `START_REPO_SESSION_PROMPT.md` as the human-facing bootstrap prompt for the Skill Advisor.

For GitHub-validated builds, autonomous builds, and final PR security sweeps, read `RUBBERDUCK-SECURITY-DELTA-GATE.md`. Compare RubberDuck base vs PR-head findings, fix true-positive new Critical/High findings in changed/new code, adjudicate false positives, and keep pre-existing findings separate from the PR readiness gate.

When the user asks to understand a codebase, map architecture, identify entry points, trace request/data flow, or produce a Codebase Atlas, apply `.cursor/rules/rubberduck-codebase-atlas-pro.mdc`.

When the user asks for change impact analysis, affected callers/callees, blast radius, tests to run, safe change order, or runtime-preserving optimization opportunities for a change, apply `.cursor/rules/rubberduck-change-impact-pro.mdc`.

When the user asks for duplicate intent discovery, behavioral twins, doppelganger hunts, hidden canonical helpers, inline reimplementations, or unification/refactor planning, apply `.cursor/rules/rubberduck-doppelganger-hunt-pro.mdc`.

When the user asks whether two implementations are equivalent, whether a refactor preserves behavior, whether an AI patch is safe, or whether before/after code has behavior drift, apply `.cursor/rules/rubberduck-mirror-pro.mdc`.

When the user asks for schema drift, API contract drift, DB/type/API consistency, model-field mismatch, nullability/default/validation drift, generated-client breakage, migration risk, or schema-code-api comparison, apply `.cursor/rules/rubberduck-schema-code-api-drift-pro.mdc`.


When the user asks to plan a new feature, design tests first, create a sealed plan, or produce sealed_plan.json, apply `.cursor/rules/rubberduck-feature-planner-pro.mdc`.

When the user asks to build from a sealed plan, run Spec Heartbeat build mode, or produce PR_READY.diff, apply `.cursor/rules/rubberduck-feature-builder-pro.mdc`.

When the user asks for autonomous plan-and-build mode under an autonomy envelope, apply `.cursor/rules/rubberduck-autonomous-feature-mode.mdc`.

When the user asks for a security audit, vulnerability hunt, pentest-style review, CWE/CVE-style report, scanner finding validation, or defensible security report, apply `.cursor/rules/rubberduck-security-audit.mdc`.

Routing precedence for ambiguous prompts:
1. `sealed_plan.json` plus a build request -> `.cursor/rules/rubberduck-feature-builder-pro.mdc`
2. autonomy envelope / autonomous plan and build -> `.cursor/rules/rubberduck-autonomous-feature-mode.mdc`
3. equivalence or replacement -> `.cursor/rules/rubberduck-mirror-pro.mdc`
4. duplicate intent or duplicate behavior -> `.cursor/rules/rubberduck-doppelganger-hunt-pro.mdc`
5. schema / type / API drift -> `.cursor/rules/rubberduck-schema-code-api-drift-pro.mdc`
6. security audit -> `.cursor/rules/rubberduck-security-audit.mdc`
7. change impact -> `.cursor/rules/rubberduck-change-impact-pro.mdc`
8. tests-first feature planning -> `.cursor/rules/rubberduck-feature-planner-pro.mdc`
9. architecture / codebase understanding -> `.cursor/rules/rubberduck-codebase-atlas-pro.mdc`

The source of truth is the copied skill folder under `.cursor/skills/<skill>/SKILL.md`.
<!-- RUBBERDUCK-SKILLS:END -->
```
