#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
required = ['SKILL.md', 'AUTONOMY-WORKFLOW.md', 'AUTONOMY-ENVELOPE.md', 'PLAN-BUILD-ORCHESTRATION.md', 'SAFETY-BOUNDARIES.md', 'STOP-CONDITIONS.md', 'HUMAN-ESCALATION.md', 'AUDIT-TRAIL.md', 'REPORT-TEMPLATE.md', 'RUBBERDUCK-SECURITY-DELTA-GATE.md', 'CHANGELOG.md', 'scripts/verify_skill_structure.py', 'scripts/smoke_test_skill.py', 'scripts/validate_autonomy_envelope.py', 'scripts/validate_auto_audit.py']
tokens = ['AUTONOMY_ENVELOPE.json', 'AUTO_AUTHORIZATION.json', 'Feature Planner Pro', 'Feature Builder Pro', 'must never bypass', 'max_iterations', 'Security Delta Gate', 'CLEAN_NO_NEW_CRITICAL_HIGH']

missing = [p for p in required if not (root / p).exists()]
if missing:
    print("Missing required files:")
    for p in missing:
        print(f" - {p}")
    sys.exit(1)

skill = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
for token in tokens:
    if token not in skill:
        print(f"SKILL.md missing required token: {token}")
        sys.exit(2)

print("OK: RubberDuck Autonomous Feature Mode skill structure verified")
