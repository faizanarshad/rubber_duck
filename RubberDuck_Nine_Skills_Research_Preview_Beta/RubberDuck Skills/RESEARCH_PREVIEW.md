# Research Preview Notes

Package name:

```text
RubberDuck_Nine_Skills_Research_Preview_Beta
```

Audience:

```text
early testers and evaluators
```

Purpose:

This package evaluates nine RubberDuck-backed skills across Codex, Claude Code, and Cursor. The skills are designed to make RubberDuck Codebase Intelligence and Semantic Intelligence the primary evidence layer for repository understanding, security review, change impact, duplicate-intent discovery, equivalence checks, schema/code/API drift review, feature planning, feature building, and bounded autonomous plan/build workflows.

## Evaluation Expectations

Use real repositories when testing the RubberDuck-backed workflows. For best coverage, the target should be a GitHub repository that RubberDuck can access.

If a target exists only locally or RubberDuck cannot access it, follow `RUBBERDUCK-CI-BOOTSTRAP.md`: mirror or push the target to an authorized GitHub repository, then run `detailed_repo_analysis(..., semantic_mode="full")` until CI semantic full completes. Local indexing is only a post-CI fallback for semantic loading gaps.

When evaluating responses, RubberDuck-powered skill results should begin with `🦆`. See `RUBBERDUCK-RESPONSE-MARKER.md`.

When installing the zip for the first time, use `SETUP_PROMPT.md`. It forces extraction, package verification, target installation, and installed-target verification before success is claimed.

When starting a fresh repo session after installation, use `START_REPO_SESSION_PROMPT.md`. It points the agent to the installed `RUBBERDUCK-SKILL-ADVISOR.md` and asks for the task, control mode, build scope, and Security Delta Gate preference.

When evaluating multi-skill tasks, use `RUBBERDUCK-SKILL-ADVISOR.md` first. It should recommend a skill order and ask the tester to approve review-each-phase, planning-with-signoff, or bounded autonomous mode before long-running execution. For build tasks, it should also ask whether execution is local-only, step-by-step GitHub-validated, or autonomous bounded GitHub-validated.

For GitHub-validated build tasks, evaluate `RUBBERDUCK-SECURITY-DELTA-GATE.md`: the agent should compare base vs PR-head RubberDuck findings, fix true-positive new Critical/High findings in changed/new code, adjudicate false positives, and report pre-existing findings separately.

## Before Installing

From the extracted package root:

```bash
python3 verification/run_all_checks.py . --write verification/package_verification_results.json
```

Expected result:

```text
failures: 0
safety_hits: 0
```

## After Installing

Run the installed-target verifier for the platform you copied into:

```bash
python3 verification/verify_installed_skills.py ~/.codex/skills
python3 verification/verify_installed_skills.py ~/.claude/skills
python3 verification/verify_installed_skills.py .cursor/skills --cursor-rules-root .cursor/rules
```

## Feedback Areas

Please evaluate:

- whether skill routing chooses the expected skill;
- whether the skill advisor recommends a useful order before multi-skill work;
- whether the GitHub mirror and CI semantic-full bootstrap is followed before graph-backed claims;
- whether unsupported or degraded evidence is disclosed clearly;
- whether validators reject unsafe or incomplete artifacts;
- whether final reports are evidence-backed and useful for review.
