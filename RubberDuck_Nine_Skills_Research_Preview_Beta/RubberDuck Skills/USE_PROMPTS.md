Before first use, run the package verifier from the extracted package root:

```bash
python3 verification/run_all_checks.py . --write verification/package_verification_results.json
```

Before any RubberDuck-backed skill run, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible, or stale in RubberDuck CI, mirror/push it to an authorized GitHub repo first and run `detailed_repo_analysis(..., semantic_mode="full")` on that `owner/repo` until the complete CI semantic full report exists. Local indexing is only a post-CI fallback for semantic loading gaps, not the main path.

When the selected skill produces a status/result/report, start the response with `🦆` according to `RUBBERDUCK-RESPONSE-MARKER.md`.

# Use Prompts

## Setup Prompt

The first-time installer prompt lives in `SETUP_PROMPT.md`. Use it when someone receives the zip and needs an agent to install the skills correctly.

The repo-session advisor prompt lives in `START_REPO_SESSION_PROMPT.md`. Use it after the skills are installed and visible to the agent.

In the clean shareable zip, these two prompts are the only top-level files. The installable package and detailed documentation are inside `RubberDuck Skills/`.

Canonical advisor activation phrase:

```text
I need help from the RubberDuck Advisor.
```

## Skill Advisor

```text
Use the RubberDuck Skill Advisor. Read RUBBERDUCK-SKILL-ADVISOR.md first.

Target: <repo/path/branch/commit>
Task: <what I want to accomplish>

Recommend the best RubberDuck skill order for this repository and task. Include whether the repo needs GitHub mirror/CI bootstrap, then ask me to approve:
A. review each phase,
B. planning then signoff before build,
C. bounded autonomous mode.
If this will mutate code, also ask me to approve:
1. local build only,
2. GitHub-validated build, step-by-step,
3. GitHub-validated build, autonomous bounded.
Also ask whether to run the Security Delta Gate before PR-ready status.
```

## Codebase Atlas

```text
Use the rubberduck-codebase-atlas-pro skill. Read the installed SKILL.md first, then follow it without stopping halfway.

Target: <repo/path/commit>

Mode: DEEP.
Use RubberDuck codebase intelligence and semantic intelligence with semantic_mode="full".
Produce the full Codebase Atlas with architectural surprises, symbols, entry points, call chains, data/request flows, graph intelligence, unsupported surfaces, anti-claims, reading plan, tool health, and evidence ledger.
```

## Security Audit

```text
Use the rubberduck-security-audit skill. Read the installed SKILL.md first, then follow it without stopping halfway.

Target: <repo/path/commit>

Run the evidence-governed RubberDuck security audit with semantic_mode="full", full file inventory, deterministic sink census, repo-specific audit prompt, capability graph, universal and specialist playbooks, evidence ledgers, claim firewall, prior-run reconciliation if applicable, Tier-2 validation planning for high-risk claims, root-cause de-duplication, and consistency checks.
```


## Change Impact

```text
Use the rubberduck-change-impact-pro skill. Read the installed SKILL.md first, then follow it without stopping halfway.

Target: <repo/path/commit>
Change: <function/file/symbol and desired change>

Run the evidence-governed RubberDuck change impact analysis with semantic_mode="full", target resolution, shadow/doppelganger preflight, dual-source caller/callee adjudication, shared state and data-flow tracing, mock/comment/public API impact, quality and rare-signal sweep, runtime optimization opportunity pass, impact-summary.json, evidence pack, risk score, tests to run, change order, rollback, and paste-ready PR description.
```
## Doppelganger Hunt

```text
Use the rubberduck-doppelganger-hunt-pro skill. Read the installed SKILL.md first, then follow it without stopping halfway.

Target: <repo/path/commit>
Hunt request: <seed function, behavior concept, or unconstrained repo-wide hunt>

Use RubberDuck codebase intelligence and semantic intelligence with semantic_mode="full".
Declare mode as SEEDED, CONCEPT, or UNCONSTRAINED.
Produce REPORT.md plus the full evidence pack: candidate-generator ledger, function inventory, graph-dimension coverage, cluster-summary.json, cluster roles, inline implementations, comment contracts, mergeability, change-impact preflight, unification plan, negative results, tool health, and falsification recipes.
Run all validators before final response.
```

## Mirror Pro

```text
Use the rubberduck-mirror-pro skill. Read the installed SKILL.md first, then follow it without stopping halfway.

Target: <repo/path/commit>
Mode: <rename-refactor | sibling-equivalence | ai-patch-verify | cross-language>
Preserved contract: <observable-behavior | outputs-only | side-effects-only | exception-envelope | full-functional | test-suite-compatible>
Before implementation: <file:function, analysis_id:function, branch/commit/path/function, or snippet>
After implementation: <file:function, analysis_id:function, branch/commit/path/function, or snippet>

Use RubberDuck codebase intelligence and semantic intelligence with semantic_mode="full".
Produce REPORT.md plus the full evidence pack: mirror-summary.json, before/after source, import context, path catalogues, path-match table, side-effect manifest, exception envelope, witness inputs, generated tests, undecidable blockers, structural drift, tool health, protocol completion, and falsification recipes.
Run all validators before final response.
```


## Schema-Code-API Drift Pro

```text
Use the rubberduck-schema-code-api-drift-pro skill. Read the installed SKILL.md first, then follow it without stopping halfway.

Target: <repo/path/commit>
Mode: <ANCHORED_CONCEPT | SCOPE_DRIFT | UNCONSTRAINED>
Concept/scope: <field/entity/scope, if applicable>

Use RubberDuck codebase intelligence and semantic intelligence with semantic_mode="full".
Inventory schema/code/API/validator/client layers, fuse concepts with confidence, build a drift matrix, predict runtime failures only from specific drift cells, trace round-trip paths when possible, produce remediation diffs, and emit the full evidence pack including schema-drift-summary.json.
Run all validators before final response.
```


## Feature Planner Pro

```text
Use the rubberduck-feature-planner-pro skill. Read the installed SKILL.md first, then follow it without stopping halfway.

Feature: <describe the feature>
Target: <repo/path/commit>

Run the tests-first planning workflow: start/resume a codegen session, acquire the Fit Pack, run RubberDuck codebase and semantic enrichment, discover existing patterns, select integration points, design tests first, validate the test diff, write sealed_plan.json and SIGNOFF_TEMPLATE.json, then halt for signoff. Do not write production implementation code.
```

## Feature Builder Pro

```text
Use the rubberduck-feature-builder-pro skill. Read the installed SKILL.md first, then follow it without stopping halfway.

sealed_plan_path: <path>
signoff_path or auto_authorization_path: <path>
invoked_under: USER or AUTO_MODE
tier: STANDARD

Run Worktree Safety, verify sealed-plan hash, apply tests first, then build through the Spec Heartbeat loop. Do not emit PR_READY.diff unless heartbeat, validate_generated_diff, and final command gates pass.
If this is GitHub-validated, read RUBBERDUCK-SECURITY-DELTA-GATE.md and run the Security Delta Gate before PR-ready status: fix or adjudicate new Critical/High findings in changed or newly created code, and leave pre-existing repo findings separate from PR-introduced findings.
```

## Autonomous Feature Mode

```text
Use the rubberduck-autonomous-feature-mode skill. Read the installed SKILL.md first, then follow it without stopping halfway.

Feature: <describe the feature>
Target: <repo/path/commit>
Autonomy envelope: <limits for files, iterations, dependencies, schema/API changes, and final review>

Run Feature Planner Pro then Feature Builder Pro inside the autonomy envelope. Never bypass off-limits files, drift/doppelganger gates, regression reverts, final validation, audit logging, or max-iteration limits.
```
