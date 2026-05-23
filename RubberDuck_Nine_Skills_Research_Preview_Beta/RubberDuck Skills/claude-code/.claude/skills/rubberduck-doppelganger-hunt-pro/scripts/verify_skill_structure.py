#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
required = [
    "SKILL.md",
    "RUBBERDUCK-WORKFLOW.md",
    "DOPPELGANGER-WORKFLOW.md",
    "CANDIDATE-GENERATORS.md",
    "GRAPH-FINGERPRINTS.md",
    "INLINE-DOPPELGANGERS.md",
    "COMMENT-CONTRACT-MINING.md",
    "CLUSTER-ROLE-CLASSIFICATION.md",
    "DIVERGENCE-MATRIX.md",
    "MERGEABILITY-AND-UNIFICATION.md",
    "CHANGE-IMPACT-PREFLIGHT.md",
    "EVIDENCE-GOVERNANCE.md",
    "CLAIM-FIREWALL.md",
    "TOOL-HEALTH-SENTINEL.md",
    "REPORT-TEMPLATE.md",
    "scripts/verify_report_consistency.py",
    "scripts/check_cluster_consistency.py",
    "scripts/check_protocol_completion.py",
    "scripts/verify_skill_structure.py",
    "scripts/smoke_test_skill.py",
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    print("Missing required files:")
    for p in missing:
        print(" -", p)
    sys.exit(1)
txt = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
tokens = ["semantic_mode=\"full\"", "SEEDED", "CONCEPT", "UNCONSTRAINED", "candidate-generator", "graph-dimension", "comment-contract", "change-impact preflight"]
for t in tokens:
    if t not in txt:
        print(f"SKILL.md missing required token: {t}")
        sys.exit(2)
print("OK: RubberDuck Doppelganger Hunt Pro skill structure present")
