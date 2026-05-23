#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
failures = []
for rel in ['SKILL.md', 'RUBBERDUCK-WORKFLOW.md', 'PLAN-WORKFLOW.md', 'FIT-PACK-GOVERNANCE.md', 'PATTERN-DISCOVERY.md', 'TESTS-FIRST-DESIGN.md', 'INTEGRATION-POINT-SELECTION.md', 'NEGATIVE-SCOPE.md', 'SEALED-PLAN-SCHEMA.md', 'SIGNOFF-HANDOFF.md', 'EVIDENCE-GOVERNANCE.md', 'CLAIM-FIREWALL.md', 'TOOL-HEALTH-SENTINEL.md', 'REPORT-TEMPLATE.md', 'CHANGELOG.md', 'scripts/verify_skill_structure.py', 'scripts/smoke_test_skill.py', 'scripts/validate_sealed_plan.py', 'scripts/validate_test_diff_contract.py', 'scripts/check_protocol_completion.py']:
    p = root / rel
    if not p.exists():
        failures.append(f"missing {rel}")
    elif p.is_file() and p.stat().st_size == 0:
        failures.append(f"empty {rel}")

skill = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
for token in ['sealed_plan.json', 'SIGNOFF_TEMPLATE.json', 'Fit Pack', 'tests-first', 'semantic_mode="full"', 'Do not write production', 'plan_sha256']:
    if token not in skill:
        failures.append(f"missing token {token}")

if failures:
    print("FAIL")
    for f in failures:
        print(" -", f)
    sys.exit(2)

print("OK: Feature Planner Pro smoke test passed")
