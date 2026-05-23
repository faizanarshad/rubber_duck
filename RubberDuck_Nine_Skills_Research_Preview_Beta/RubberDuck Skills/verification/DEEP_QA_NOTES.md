# Verification Notes

This research-preview package includes two single-command verifiers.

## Package-tree verification

Run from the extracted package root:

```bash
python3 verification/run_all_checks.py . --write verification/package_verification_results.json
```

This checks all nine skills across Codex, Claude Code, and Cursor in one process, plus Cursor rules, top-level docs, platform equivalence, CI bootstrap wiring, and local artifact markers.

## Installed-target verification

After copying skills into a target skills directory, run:

```bash
python3 verification/verify_installed_skills.py ~/.codex/skills
python3 verification/verify_installed_skills.py ~/.claude/skills
python3 verification/verify_installed_skills.py .cursor/skills
```

Use the path that matches your platform. This verifies the copied destination, not just the package tree.

## Runtime note

If the surrounding Python environment emits unrelated startup warnings, trust the verifier exit code and JSON result.
