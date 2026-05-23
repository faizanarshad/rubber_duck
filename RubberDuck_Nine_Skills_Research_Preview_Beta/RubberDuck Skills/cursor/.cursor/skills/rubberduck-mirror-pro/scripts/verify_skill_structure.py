#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
required = [
    "SKILL.md",
    "RUBBERDUCK-WORKFLOW.md",
    "MIRROR-WORKFLOW.md",
    "INPUT-CONTRACTS.md",
    "IMPORT-CONTEXT.md",
    "PATH-ENUMERATION.md",
    "SIDE-EFFECT-MANIFEST.md",
    "EXCEPTION-ENVELOPE.md",
    "WITNESS-GENERATION.md",
    "TEST-SUITE-GENERATION.md",
    "VERDICT-TAXONOMY.md",
    "EVIDENCE-GOVERNANCE.md",
    "CLAIM-FIREWALL.md",
    "TOOL-HEALTH-SENTINEL.md",
    "REPORT-TEMPLATE.md",
    "scripts/verify_report_consistency.py",
    "scripts/check_mirror_verdict.py",
    "scripts/check_path_match_table.py",
    "scripts/check_protocol_completion.py",
    "scripts/smoke_test_skill.py",
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    print("Missing required files:")
    for p in missing:
        print(" -", p)
    sys.exit(1)

txt = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
tokens = [
    "semantic_mode=\"full\"",
    "PROVEN_EQUIVALENT_UNDER_CONTRACT",
    "NOT_EQUIVALENT",
    "preserved_contract",
    "side effects",
    "exception",
    "witness",
    "Do not interrupt halfway",
]
for token in tokens:
    if token not in txt:
        print(f"SKILL.md missing required token: {token}")
        sys.exit(2)

for forbidden in ["expected_" + "findings", "private expected", "__" + "MACOSX", ".DS" + "_Store"]:
    if (root / forbidden).exists():
        print(f"Forbidden package artifact present: {forbidden}")
        sys.exit(3)

print("OK: RubberDuck Mirror Pro skill structure present")
