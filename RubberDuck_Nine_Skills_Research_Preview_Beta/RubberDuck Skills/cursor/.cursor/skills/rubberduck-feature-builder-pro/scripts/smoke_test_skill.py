#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
failures = []
for rel in ['SKILL.md', 'BUILD-WORKFLOW.md', 'WORKTREE-SAFETY.md', 'SIGNOFF-AND-AUTHORIZATION.md', 'SPEC-HEARTBEAT.md', 'PREVALIDATE-CHANGE.md', 'INCREMENTAL-REINDEX.md', 'REGRESSION-REVERT.md', 'DOPPELGANGER-GATE.md', 'DRIFT-DETECTOR.md', 'WARN-ADJUDICATION.md', 'VALIDATION-CADENCE.md', 'AUDIT-TRAIL.md', 'PR-READY-DIFF.md', 'EVIDENCE-GOVERNANCE.md', 'TOOL-HEALTH-SENTINEL.md', 'REPORT-TEMPLATE.md', 'GITHUB-PUBLISH-REINDEX-GATE.md', 'GITHUB-VALIDATION-SELF-CHECK.md', 'RUBBERDUCK-SECURITY-DELTA-GATE.md', 'CHANGELOG.md', 'scripts/verify_skill_structure.py', 'scripts/smoke_test_skill.py', 'scripts/validate_build_inputs.py', 'scripts/validate_signoff.py', 'scripts/validate_heartbeat.py', 'scripts/validate_audit_log.py', 'scripts/validate_final_build_package.py']:
    p = root / rel
    if not p.exists():
        failures.append(f"missing {rel}")
    elif p.is_file() and p.stat().st_size == 0:
        failures.append(f"empty {rel}")

skill = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
for token in ['HEARTBEAT.json', 'SIGNOFF.json', 'AUTO_AUTHORIZATION.json', 'PR_READY.diff', 'GREEN', 'YELLOW_UNACKED', 'validate_generated_diff', 'Worktree Safety', 'GitHub Publish/Re-index Gate', 'Security Delta Gate', 'FULL_REPO_BACKED_RUBBERDUCK_VALIDATED', 'LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING', 'CLEAN_NO_NEW_CRITICAL_HIGH']:
    if token not in skill:
        failures.append(f"missing token {token}")

if failures:
    print("FAIL")
    for f in failures:
        print(" -", f)
    sys.exit(2)

print("OK: Feature Builder Pro smoke test passed")
