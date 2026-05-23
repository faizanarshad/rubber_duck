# RubberDuck Nine Skills — Research Preview Beta

This research-preview beta contains nine RubberDuck skills packaged for Codex, Claude Code, and Cursor:

```text
rubberduck-codebase-atlas-pro
rubberduck-security-audit
rubberduck-change-impact-pro
rubberduck-doppelganger-hunt-pro
rubberduck-mirror-pro
rubberduck-schema-code-api-drift-pro
rubberduck-feature-planner-pro
rubberduck-feature-builder-pro
rubberduck-autonomous-feature-mode
```

Skill note:
- The package intentionally includes only one security skill; Doppelganger Hunt and Mirror Pro are semantic/refactor-equivalence skills, not security audit skills.
- The selected security baseline is the exhaustive evidence-governed `rubberduck-security-audit` skill.
- Multi-skill tasks use `RUBBERDUCK-SKILL-ADVISOR.md` to recommend an ordered RubberDuck workflow and ask the user to choose review-each-phase, planning-with-signoff, or bounded autonomous mode. For builds, it also distinguishes local-only, step-by-step GitHub-validated, and autonomous bounded GitHub-validated execution.
- GitHub-validated builds can use `RUBBERDUCK-SECURITY-DELTA-GATE.md` before PR-ready status. The default standard is no new untriaged Critical/High findings in changed or newly created code; pre-existing findings are reported separately rather than auto-fixed blindly.
- All RubberDuck-backed skills share `RUBBERDUCK-CI-BOOTSTRAP.md`: local-only or inaccessible targets must be mirrored to an authorized GitHub repository, then analyzed with `detailed_repo_analysis(..., semantic_mode="full")` until CI semantic full completes. Local indexing is only a post-CI fallback for semantic loading gaps, not a substitute for Codebase Intelligence Phase 2.
- All RubberDuck-powered skill responses follow `RUBBERDUCK-RESPONSE-MARKER.md`: start RubberDuck skill results with `🦆` so testers can distinguish RubberDuck-powered output from ordinary model responses.

Platforms included:

```text
codex/skills/
claude-code/.claude/skills/
cursor/.cursor/skills/
cursor/.cursor/rules/
```

The core skill folders are byte-equivalent across Codex, Claude Code, and Cursor for each skill. Cursor rules are thin adapters that instruct Cursor to read the copied skill folder.

## Research Preview Status

This is a beta package for early testers and evaluators. It is intended to evaluate:

- RubberDuck-backed codebase understanding, security audit, change impact, duplicate-intent discovery, equivalence checks, and schema/code/API drift review.
- Tests-first planning, sealed build execution, and bounded autonomous plan/build orchestration.
- Cross-platform skill installation for Codex, Claude Code, and Cursor.

Run the verifier before installing and after copying into a target environment.

## One-command verification

From the extracted package root:

```bash
cd "RubberDuck Skills"
python3 verification/run_all_checks.py . --write verification/package_verification_results.json
```

This verifies all nine skills across all three platforms in one Python process:

```text
3 platforms × 9 skills × structure/smoke = 54 skill checks
plus routing and synthetic validator suites = 56 verifier checks
```

It also checks Cursor rules, top-level install/use docs, platform equivalence, and private/local artifact markers. After copying into a user or repo skills directory, use `verification/verify_installed_skills.py <skills-root>` to verify the installed target.

## Install docs

```text
SETUP_PROMPT.md
START_REPO_SESSION_PROMPT.md
INSTALL_CODEX.md
INSTALL_CLAUDE_CODE.md
INSTALL_CURSOR.md
USE_PROMPTS.md
```

For first-time installation, paste `SETUP_PROMPT.md` into the target agent with the zip path. It forces the extract -> package verify -> install -> installed-target verify sequence.

After installation and tool restart/reload, start a repo session by pasting `START_REPO_SESSION_PROMPT.md`. It brings the Skill Advisor online, asks for the target repo/task, and routes the work through the correct RubberDuck skill sequence and control mode.

Canonical advisor activation phrase:

```text
I need help from the RubberDuck Advisor.
```

In the clean shareable zip, only `SETUP_PROMPT.md`, `START_REPO_SESSION_PROMPT.md`, and the `RubberDuck Skills/` folder are visible at the top level. Detailed docs and platform folders live inside `RubberDuck Skills/`.


## Schema-Code-API Drift Pro

Use `rubberduck-schema-code-api-drift-pro` to triangulate DB schema, code types/models, validators, runtime handlers, API contracts, and client types for drift and predicted runtime failures.


## Feature Planner Pro

Use `rubberduck-feature-planner-pro` to turn a feature request into an immutable tests-first sealed plan. It writes `sealed_plan.json`, `test_diff.patch`, `SIGNOFF_TEMPLATE.json`, and evidence files, then halts for signoff. It does not write production code.

## Feature Builder Pro

Use `rubberduck-feature-builder-pro` to consume a sealed plan plus `SIGNOFF.json` or `AUTO_AUTHORIZATION.json`, apply tests first, run the Spec Heartbeat loop, validate generated diffs, and emit `PR_READY.diff` only when the structural gates pass.

For GitHub-validated or autonomous builds, Builder can also run the Security Delta Gate and must include a security delta status before PR-ready promotion.

## Autonomous Feature Mode

Use `rubberduck-autonomous-feature-mode` to orchestrate Feature Planner Pro and Feature Builder Pro inside an explicit autonomy envelope. It can bypass manual plan signoff only inside the envelope, and it never bypasses safety gates, drift/doppelganger gates, final validation, audit logging, or max-iteration limits.


## Install/runtime verification

This package includes a one-command package verifier plus an installed-target verifier.

```bash
python3 verification/run_all_checks.py . --write verification/package_verification_results.json
python3 verification/verify_installed_skills.py <installed-skills-root>
```

For Cursor, also verify the copied rules:

```bash
python3 verification/verify_installed_skills.py "$TARGET_REPO/.cursor/skills" \
  --cursor-rules-root "$TARGET_REPO/.cursor/rules" \
  --write verification/installed_cursor_results.json
```

`verification/run_all_checks.py` also runs `verification/run_power_skill_synthetic_tests.py`, which exercises Plan / Build / Autonomous validators with positive and negative fixtures.

## RubberDuck CI bootstrap

Before using any RubberDuck-backed skill, read `RUBBERDUCK-CI-BOOTSTRAP.md`. The verifier checks that this bootstrap is present in every platform copy.

The required path is:

```text
local-only/inaccessible target
  -> authorized GitHub mirror/push
  -> detailed_repo_analysis(..., semantic_mode="full") on owner/repo
  -> completed CI semantic full report
  -> get_started phase1/phase2 readiness
  -> load_code(..., instance_id=..., max_files=2000)
```

Do not treat `local/...`, scratch loading, or `rubberduck-index` as CI Phase 2. Those are allowed only after CI semantic full completes, and only for disclosed semantic loading gaps.

## RubberDuck skill advisor

When the user is unsure which RubberDuck skill to use, or a task likely needs multiple skills, use `RUBBERDUCK-SKILL-ADVISOR.md`.

The advisor recommends an ordered workflow, then asks the user to approve one control mode:

```text
A. Review each phase before continuing.
B. Run planning, then pause for signoff before build.
C. Autonomous mode inside an explicit envelope.

For builds, also choose:
1. Local build only.
2. GitHub-validated build, step-by-step.
3. GitHub-validated build, autonomous bounded.
S. Run the Security Delta Gate before PR-ready status.
```

## RubberDuck response marker

When a response is primarily powered by a RubberDuck skill, start it with:

```text
🦆
```

See `RUBBERDUCK-RESPONSE-MARKER.md` for the exact rule and exceptions.
