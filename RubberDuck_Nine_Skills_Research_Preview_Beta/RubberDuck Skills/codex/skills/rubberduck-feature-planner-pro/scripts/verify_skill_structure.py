#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
required = ['SKILL.md', 'RUBBERDUCK-WORKFLOW.md', 'PLAN-WORKFLOW.md', 'FIT-PACK-GOVERNANCE.md', 'PATTERN-DISCOVERY.md', 'TESTS-FIRST-DESIGN.md', 'INTEGRATION-POINT-SELECTION.md', 'NEGATIVE-SCOPE.md', 'SEALED-PLAN-SCHEMA.md', 'SIGNOFF-HANDOFF.md', 'EVIDENCE-GOVERNANCE.md', 'CLAIM-FIREWALL.md', 'TOOL-HEALTH-SENTINEL.md', 'REPORT-TEMPLATE.md', 'CHANGELOG.md', 'scripts/verify_skill_structure.py', 'scripts/smoke_test_skill.py', 'scripts/validate_sealed_plan.py', 'scripts/validate_test_diff_contract.py', 'scripts/check_protocol_completion.py']
tokens = ['sealed_plan.json', 'SIGNOFF_TEMPLATE.json', 'Fit Pack', 'tests-first', 'semantic_mode="full"', 'Do not write production', 'plan_sha256']

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

print("OK: RubberDuck Feature Planner Pro skill structure verified")
