---
name: rubberduck-autonomous-feature-mode
description: RubberDuck Autonomous Feature Mode orchestrates Feature Planner Pro and Feature Builder Pro under an explicit autonomy envelope. It can bypass manual plan signoff only inside approved bounds, but it never bypasses worktree safety, off-limits files, doppelganger gates, drift detector, regression reverts, validation, security delta gates, command gates, audit logging, or max-iteration limits.
trigger: when the user wants autonomous plan-and-build mode, auto mode, autonomous feature implementation, Plan plus Build orchestration, or a bounded agent loop that plans, builds, validates, and emits a PR-ready package
version: 2026-05-autonomous-feature-mode
---

# RubberDuck Autonomous Feature Mode

This is an automation controller, not an unconstrained coding agent.

It orchestrates:

```text
Feature Planner Pro
  -> AUTO_AUTHORIZATION.json
  -> Feature Builder Pro
  -> Security Delta Gate when GitHub-validated or security-sensitive
  -> final validation
  -> PR-ready package
```

## RubberDuck CI bootstrap gate

When Auto invokes Planner/Builder or any RubberDuck-backed validation, read `RUBBERDUCK-CI-BOOTSTRAP.md`. If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, or stuck in stale/pending CI state, repo-backed RubberDuck evidence must use an authorized GitHub repo or mirror with completed `detailed_repo_analysis(..., semantic_mode="full")` before semantic graph claims are made.

Local indexing, scratch loads, and `local/...` aliases are only post-CI fallbacks for semantic loading gaps. They are not Codebase Intelligence Phase 2 and must be labeled as degraded evidence.

## RubberDuck response marker

When this skill produces a RubberDuck-powered status, blocker, validation summary, evidence report, or final answer, start the response with `🦆`. The marker is required only for RubberDuck-powered skill output; ordinary package maintenance or non-RubberDuck responses should not use it. See `RUBBERDUCK-RESPONSE-MARKER.md`.

## RubberDuck skill advisor

If the user has not explicitly chosen autonomous mode, use `RUBBERDUCK-SKILL-ADVISOR.md` to offer review-each-phase, planning-with-signoff, or bounded autonomous mode before starting Auto. Autonomous mode requires an explicit envelope.

## RubberDuck security delta gate

When Auto pushes a branch, opens or updates a PR, runs GitHub-validated build mode, or touches security-sensitive surfaces, read `RUBBERDUCK-SECURITY-DELTA-GATE.md`. Auto must compare RubberDuck base vs PR-head findings, auto-fix only true-positive new Critical/High findings inside the autonomy envelope, adjudicate false positives with evidence, and preserve pre-existing findings as baseline debt.

## Required input

```text
feature_description
repo
base_commit
autonomy_envelope
```

## Autonomy envelope

```json
{
  "tier": "STANDARD",
  "max_iterations": 50,
  "max_files_touched": 12,
  "max_new_dependencies": 0,
  "allow_public_api_change": false,
  "allow_schema_change": false,
  "allowed_file_globs": [],
  "off_limits_file_globs": [],
  "require_final_user_review": true
}
```

For autonomous GitHub mutation, the envelope or `AUTO_AUTHORIZATION.json` must also state whether security delta enforcement is required and set `max_security_fix_iterations`.

## Auto may bypass

```text
manual signoff between PLAN and BUILD
```

only by writing `AUTO_AUTHORIZATION.json`.

## Auto must never bypass

```text
worktree safety
sealed plan hash verification
off-limits files
doppelganger gate
drift detector
regression revert
validate_generated_diff
security delta gate
final command gate
audit logging
max_iterations
autonomy envelope
```

## Security stabilization loop

After Builder completes GitHub repo-backed validation:

```text
run RubberDuck on base branch
run RubberDuck on PR head
build security-delta.json
if new Critical/High true positive appears in changed/new code:
  patch inside autonomy envelope
  rerun local gates
  push scoped commit
  rerun RubberDuck
repeat until CLEAN/ADJUDICATED/BLOCKED or max_security_fix_iterations
```

Auto may not mark `final_status=complete` when the required security delta status is `BLOCKED_NEW_UNRESOLVED_FINDINGS` or `NOT_RUN_LOCAL_ONLY`.

Successful autonomous PR-ready completion requires one of:

```text
Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH
Security delta status: NEW_FINDINGS_ADJUDICATED
```

## Output

```text
uc_auto/<slug>/
  AUTONOMY_ENVELOPE.json
  AUTO_AUDIT.json
  PLAN/
  BUILD/
  FINAL_REVIEW.md
```

If `require_final_user_review=true`, do not merge or apply beyond a PR-ready package.
