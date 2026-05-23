#!/usr/bin/env python3
"""Verify RubberDuck Change Impact Pro skill structure."""
from __future__ import annotations
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
required = [
    "SKILL.md",
    "RUBBERDUCK-WORKFLOW.md",
    "TARGET-RESOLUTION.md",
    "IMPACT-PROMPT-COMPILER.md",
    "IMPACT-WORKFLOW.md",
    "DUAL-SOURCE-ADJUDICATION.md",
    "SHADOW-PREFLIGHT.md",
    "CHANGE-TYPE-PLAYBOOKS.md",
    "COMMENT-CONTRACTS.md",
    "MOCK-BREAKAGE.md",
    "IMPACT-RISK-SCORING.md",
    "QUALITY-RUNTIME-SWEEP.md",
    "RUNTIME-OPTIMIZATION.md",
    "EVIDENCE-PACK.md",
    "EVIDENCE-GOVERNANCE.md",
    "CLAIM-FIREWALL.md",
    "TOOL-HEALTH-SENTINEL.md",
    "UNSUPPORTED-SURFACE-ROUTER.md",
    "VALIDATION-REPORTING.md",
    "REPORT-TEMPLATE.md",
    "PROTOCOL-COMPLETION.md",
    "CHANGELOG.md",
    "scripts/verify_skill_structure.py",
    "scripts/verify_report_consistency.py",
    "scripts/check_claim_ledger.py",
    "scripts/check_protocol_completion.py",
    "scripts/smoke_test_skill.py",
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    print("Missing required files:")
    for p in missing:
        print(f" - {p}")
    raise SystemExit(1)

skill = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")
checks = [
    'name: rubberduck-change-impact-pro',
    'semantic_mode="full"',
    'Dual-Source',
    'Runtime Optimization',
    'DEEP',
]
for needle in checks:
    if needle not in skill:
        print(f"Missing SKILL.md marker: {needle}")
        raise SystemExit(1)

banned_dirs = ["benchmarks", "private", "expected-findings"]
for d in banned_dirs:
    if (root / d).exists():
        print(f"Forbidden directory present: {d}")
        raise SystemExit(1)

print("OK: RubberDuck Change Impact Pro skill structure verified")
