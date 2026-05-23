#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
failures = []
for rel in ['SKILL.md', 'AUTONOMY-WORKFLOW.md', 'AUTONOMY-ENVELOPE.md', 'PLAN-BUILD-ORCHESTRATION.md', 'SAFETY-BOUNDARIES.md', 'STOP-CONDITIONS.md', 'HUMAN-ESCALATION.md', 'AUDIT-TRAIL.md', 'REPORT-TEMPLATE.md', 'RUBBERDUCK-SECURITY-DELTA-GATE.md', 'CHANGELOG.md', 'scripts/verify_skill_structure.py', 'scripts/smoke_test_skill.py', 'scripts/validate_autonomy_envelope.py', 'scripts/validate_auto_audit.py']:
    p = root / rel
    if not p.exists():
        failures.append(f"missing {rel}")
    elif p.is_file() and p.stat().st_size == 0:
        failures.append(f"empty {rel}")

skill = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
for token in ['AUTONOMY_ENVELOPE.json', 'AUTO_AUTHORIZATION.json', 'Feature Planner Pro', 'Feature Builder Pro', 'must never bypass', 'max_iterations', 'Security Delta Gate', 'CLEAN_NO_NEW_CRITICAL_HIGH']:
    if token not in skill:
        failures.append(f"missing token {token}")

if failures:
    print("FAIL")
    for f in failures:
        print(" -", f)
    sys.exit(2)

print("OK: Autonomous Feature Mode smoke test passed")
