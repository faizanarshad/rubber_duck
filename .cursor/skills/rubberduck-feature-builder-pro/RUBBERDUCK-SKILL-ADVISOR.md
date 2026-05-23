# RubberDuck Skill Advisor

Use this advisor when the user's task could involve more than one RubberDuck skill, when the user is unsure which skill to apply, or when a repository has not yet been profiled.

Canonical activation phrase:

```text
I need help from the RubberDuck Advisor.
```

The primary skill entrypoint for this phrase is `rubberduck-codebase-atlas-pro`. When the phrase is used, produce an advisor recommendation and approval question first; do not launch a long workflow, mutate code, push to GitHub, or open a PR until the user approves.

## Goal

Help the user choose an ordered RubberDuck workflow before running a long multi-skill protocol.

The advisor does not replace the nine skills. It produces a short recommendation, asks for approval when the next step would run multiple skills or mutate code, and then hands off to the selected skill sequence.

## Intake

Infer what you can from the request. Ask at most one clarifying question only when the target repo, task objective, or approval mode is missing and cannot be inferred.

Capture:

```text
target repo/path/branch/commit
user objective
whether code changes are allowed
whether the repo is already GitHub-accessible to RubberDuck
desired control level: review each phase, approve before build, or autonomous
build execution scope when code mutation is requested
whether a Security Delta Gate is required before PR-ready status
time budget: quick, standard, deep
```

Apply `RUBBERDUCK-CI-BOOTSTRAP.md` before making graph-backed recommendations. If the repo is local-only or inaccessible, recommend the GitHub mirror/push path before CI semantic full.

## Default Recommendation Flow

For an unfamiliar repository, start with:

```text
1. rubberduck-codebase-atlas-pro
```

Use Codebase Atlas to learn the repository, unsupported surfaces, entry points, and architecture. Then recommend the next skills based on the user's objective and the repo intelligence.

## Skill Selection Matrix

```text
Understand the repository
  -> rubberduck-codebase-atlas-pro

Security audit, vulnerability hunt, scanner finding validation
  -> rubberduck-codebase-atlas-pro if repo is unfamiliar
  -> rubberduck-security-audit

PR security delta, final autonomous build sweep, or "make this PR clean"
  -> rubberduck-security-audit in PR_DELTA_SECURITY_REVIEW mode
  -> rubberduck-feature-builder-pro or rubberduck-autonomous-feature-mode fix loop only for true-positive new Critical/High findings in changed/new code

Change a function/file/API safely
  -> rubberduck-codebase-atlas-pro if repo is unfamiliar
  -> rubberduck-change-impact-pro
  -> rubberduck-doppelganger-hunt-pro if duplicate/shadow implementations may exist
  -> rubberduck-feature-planner-pro if a new implementation plan is needed

Find duplicate behavior or reusable existing implementation
  -> rubberduck-codebase-atlas-pro if repo is unfamiliar
  -> rubberduck-doppelganger-hunt-pro
  -> rubberduck-mirror-pro for replacement safety

Check whether one implementation can replace another
  -> rubberduck-mirror-pro
  -> rubberduck-change-impact-pro if replacement affects callers

Schema, model, API, validation, migration, or client contract drift
  -> rubberduck-codebase-atlas-pro if repo is unfamiliar
  -> rubberduck-schema-code-api-drift-pro
  -> rubberduck-change-impact-pro for proposed remediation

Plan a feature without writing production code
  -> rubberduck-codebase-atlas-pro if repo is unfamiliar
  -> rubberduck-feature-planner-pro

Build from a sealed plan with user control
  -> rubberduck-feature-builder-pro
  -> ask for local-only, step-by-step GitHub validation, or bounded autonomous GitHub validation unless already clear

Plan and build under bounded autonomy
  -> rubberduck-autonomous-feature-mode
```

## Recommendation Output

Before running a multi-skill workflow, produce a concise recommendation:

```text
🦆 RubberDuck Skill Recommendation

Goal: <user objective>
Repo state: <GitHub-accessible | needs mirror | blocked | unknown>
Recommended order:
1. <skill> - <why>
2. <skill> - <why>
3. <skill> - <why>

Control options:
A. Review each phase before continuing.
B. Run planning, then pause for signoff before build.
C. Autonomous mode inside an explicit envelope, report back when complete or blocked.

Build execution scope, if code will be changed:
1. Local build only - files changed locally, tests run, PR_READY.diff emitted; no GitHub push or repo-backed RubberDuck indexing.
2. GitHub-validated build, step-by-step - ask before branch, commit, push, PR, and indexing.
3. GitHub-validated build, autonomous bounded - create branch, commit scoped changes, push, run RubberDuck validation, and report blockers; never include secrets or unrelated files; stop if destructive git action would be needed.

Security delta:
S. Run the Security Delta Gate before PR-ready status - compare base vs PR head, auto-fix true-positive new Critical/High findings in changed/new code, adjudicate false positives, and report pre-existing findings separately.

Please approve A, B, or C.
If this is a build, also approve 1, 2, or 3, and say whether to run S.
```

Use the `🦆` marker because this recommendation is RubberDuck-powered guidance.

## Approval Rules

Do not start a long multi-skill workflow, create a GitHub mirror, or mutate repository files until the user approves the recommended path or has already clearly authorized it.

If the user chooses:

```text
A. Review each phase
```

Run the first skill, report results, and ask before the next skill.

If the user chooses:

```text
B. Planning then signoff
```

Run Codebase Atlas if needed, then Feature Planner. Stop after `sealed_plan.json`, `test_diff.patch`, and `SIGNOFF_TEMPLATE.json`.

If the user chooses:

```text
C. Autonomous mode
```

Require an explicit autonomy envelope, then run `rubberduck-autonomous-feature-mode`. The envelope must include file boundaries, max iterations, dependency policy, schema/API policy, and final review requirements.

If the user chooses build execution scope:

```text
1. Local build only
```

Run `rubberduck-feature-builder-pro` in `LOCAL_BUILD_ONLY`. It may emit `PR_READY.diff` after local gates pass, but final output must not claim full RubberDuck Codebase Intelligence validation and must say repo-backed RubberDuck validation is pending when local-only changes cannot be indexed.

```text
2. GitHub-validated build, step-by-step
```

Run `rubberduck-feature-builder-pro` in `GITHUB_VALIDATED_BUILD`. Ask before creating a `codex/...` branch, staging scoped files, committing, pushing, opening a PR if appropriate, and running/re-polling RubberDuck Codebase Intelligence and Semantic Intelligence.

```text
3. GitHub-validated build, autonomous bounded
```

Run `rubberduck-feature-builder-pro` in `AUTO_GITHUB_VALIDATED_BUILD` only with `AUTO_AUTHORIZATION.json` or explicit external GitHub mutation approval. Create a branch, commit scoped changes, push, run RubberDuck validation, and report blockers. Never include secrets or unrelated files, and stop if destructive git action would be needed.

If the user chooses Security Delta Gate:

```text
S. Security Delta Gate
```

Use `RUBBERDUCK-SECURITY-DELTA-GATE.md`. Run base-vs-PR RubberDuck security comparison before PR-ready status. The default target is no new untriaged Critical/High findings, not a completely clean repository. Fix true-positive new Critical/High findings in changed or newly created code; document pre-existing findings separately.

## When Not To Ask

If the user clearly names one skill and asks to run it, run that skill directly.

If the task is a simple package install, package verification, or documentation update, do not invoke the advisor.

If a hard gate blocks progress, report the blocker instead of asking preference questions.
