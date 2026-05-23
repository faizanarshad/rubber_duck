# Verification Summary

## Scope

This research-preview beta packages nine RubberDuck skills across Codex, Claude Code, and Cursor:

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

## Verification Coverage

The package verifier checks:

- top-level docs and install instructions;
- all platform skill folders;
- skill folder equivalence across Codex, Claude Code, and Cursor;
- Cursor rule frontmatter and skill references;
- `RUBBERDUCK-CI-BOOTSTRAP.md` presence and wiring across every installed skill;
- local artifact and hygiene markers;
- per-skill structure and smoke tests;
- routing precedence;
- Plan / Build / Autonomous synthetic validator fixtures.

## Expected Results

From the extracted package root:

```bash
python3 verification/run_all_checks.py . --write verification/package_verification_results.json
```

Expected:

```text
checks_run: 56
failures: 0
safety_hits: 0
```

Additional standalone checks:

```bash
python3 verification/check_skill_routing.py .
python3 verification/run_power_skill_synthetic_tests.py .
python3 -m compileall -q verification codex claude-code cursor
```

Expected:

```text
routing tests: 9 passed
synthetic validator tests: 24 passed
python parse errors: 0
```

## Installed-Target Verification

After copying skills:

```bash
python3 verification/verify_installed_skills.py ~/.codex/skills
python3 verification/verify_installed_skills.py ~/.claude/skills
python3 verification/verify_installed_skills.py .cursor/skills --cursor-rules-root .cursor/rules
```

Expected:

```text
Codex: 18 checks, 0 failures
Claude Code: 18 checks, 0 failures
Cursor: 18 checks, 0 failures
```
