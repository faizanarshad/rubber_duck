#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
required = [
    "SKILL.md",
    "RUBBERDUCK-WORKFLOW.md",
    "SCHEMA-DRIFT-WORKFLOW.md",
    "LAYER-INVENTORY.md",
    "CONCEPT-FUSION.md",
    "DRIFT-MATRIX.md",
    "RUNTIME-FAILURE-PREDICTION.md",
    "ROUND-TRIP-PROOF.md",
    "REMEDIATION-DIFFS.md",
    "EVIDENCE-GOVERNANCE.md",
    "CLAIM-FIREWALL.md",
    "TOOL-HEALTH-SENTINEL.md",
    "REPORT-TEMPLATE.md",
    "scripts/verify_skill_structure.py",
    "scripts/verify_report_consistency.py",
    "scripts/check_layer_inventory.py",
    "scripts/check_concept_fusion.py",
    "scripts/check_drift_matrix.py",
    "scripts/check_protocol_completion.py",
    "scripts/smoke_test_skill.py",
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    print("Missing required files:")
    for p in missing:
        print(" -", p)
    sys.exit(1)
skill = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
tokens = [
    "rubberduck-schema-code-api-drift-pro",
    "semantic_mode=\"full\"",
    "ANCHORED_CONCEPT",
    "SCOPE_DRIFT",
    "UNCONSTRAINED",
    "Drift dimensions",
    "No drift row may be reported unless at least two layers are cited",
]
for token in tokens:
    if token not in skill:
        print(f"SKILL.md missing token: {token}")
        sys.exit(2)
print("OK: RubberDuck Schema-Code-API Drift Pro skill structure present")
