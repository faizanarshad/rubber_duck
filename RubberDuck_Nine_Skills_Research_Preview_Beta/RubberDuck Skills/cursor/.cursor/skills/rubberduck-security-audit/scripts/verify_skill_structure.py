#!/usr/bin/env python3
"""RubberDuck Security Audit skill package structure checker.

This checker intentionally forbids bundled private regression corpora or repository-specific private expected-result files.
"""
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

required = [
    "SKILL.md",
    "RUBBERDUCK-WORKFLOW.md",
    "REPO-INTELLIGENCE-BRIEF.md",
    "AUDIT-PROMPT-COMPILER.md",
    "CAPABILITY-GRAPH.md",
    "SPECIALIST-PLAYBOOKS.md",
    "RESCUE-SWEEPS.md",
    "EXHAUSTIVE-CENSUS.md",
    "UNSUPPORTED-SURFACE-ROUTER.md",
    "COVERAGE-GOVERNANCE.md",
    "EVIDENCE-GOVERNANCE.md",
    "CLAIM-FIREWALL.md",
    "TOOL-HEALTH-SENTINEL.md",
    "PROTOCOL-COMPLETION.md",
    "DEFENSE-VERIFICATION.md",
    "LOCAL-GREP-FALLBACK.md",
    "VALIDATION-REPORTING.md",
    "FALSE-POSITIVES-DEDUP.md",
    "RUNTIME-VALIDATION-PLANNER.md",
    "PROOF-CARRYING-PATCH.md",
    "REPORT-TEMPLATE.md",
    "RUBBERDUCK-SECURITY-DELTA-GATE.md",
    "scripts/verify_report_consistency.py",
    "scripts/check_claim_ledger.py",
    "scripts/check_protocol_completion.py",
    "scripts/build_sink_census.py",
    "scripts/check_exhaustive_completion.py",
]

missing = [p for p in required if not (root / p).exists()]
if missing:
    print("Missing required files:")
    for p in missing:
        print(f" - {p}")
    sys.exit(1)

for forbidden in ["private regression corpora", "expected_findings", "private expected-results"]:
    if (root / forbidden).exists():
        print(f"Forbidden private regression directory present: {forbidden}")
        sys.exit(2)

print("OK: RubberDuck Security Audit skill structure present; no bundled private regression corpus required.")
