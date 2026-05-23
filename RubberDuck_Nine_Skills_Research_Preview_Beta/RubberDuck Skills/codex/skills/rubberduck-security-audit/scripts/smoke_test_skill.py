#!/usr/bin/env python3
"""Smoke test RubberDuck Security Audit skill files without spawning nested Python."""
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
    "EXHAUSTIVE-CENSUS.md",
    "scripts/build_sink_census.py",
    "scripts/check_exhaustive_completion.py",
    "scripts/verify_report_consistency.py",
    "scripts/check_claim_ledger.py",
    "scripts/check_protocol_completion.py",
    "scripts/smoke_test_skill.py",
    "scripts/verify_skill_structure.py",
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    print("Missing required files:")
    for p in missing:
        print(f" - {p}")
    raise SystemExit(1)

combined = []
for path in root.rglob("*.md"):
    combined.append(path.read_text(encoding="utf-8", errors="replace"))
text = "\n".join(combined).lower()

requirements = {
    "security skill name": "rubberduck-security-audit",
    "semantic full": 'semantic_mode="full"',
    "repo intelligence": "repo intelligence",
    "capability graph": "capability graph",
    "claim firewall": "claim firewall",
    "evidence governance": "evidence",
    "exhaustive census": "exhaustive",
    "rescue sweeps": "rescue",
    "root-cause de-duplication": "root-cause",
    "report consistency": "consistency",
    "platform-neutral installed skill path": "<installed_skill_dir>",
    "pr delta security review": "pr_delta_security_review",
    "security delta status": "security delta status",
}
missing_markers = [label for label, needle in requirements.items() if needle not in text]
if missing_markers:
    print("Security smoke test missing required markers:")
    for label in missing_markers:
        print(f" - {label}")
    raise SystemExit(2)

print("OK: Security Audit smoke test passed")
