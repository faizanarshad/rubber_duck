#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
verify = root / "scripts" / "verify_skill_structure.py"
if not verify.exists():
    print("Missing verify_skill_structure.py")
    raise SystemExit(1)

# Inline the structure verifier's essential check to avoid spawning a nested Python process.
required = [
    "SKILL.md",
    "RUBBERDUCK-WORKFLOW.md",
    "REPO-INTELLIGENCE-BRIEF.md",
    "ATLAS-PROMPT-COMPILER.md",
    "SEMANTIC-MAP-WORKFLOW.md",
    "SYMBOLS-AND-ENTRYPOINTS.md",
    "CALL-CHAIN-AND-DATA-FLOW.md",
    "ARCHITECTURAL-SURPRISES.md",
    "GRAPH-ATLAS-SECTIONS.md",
    "FEATURE-ATLAS-MODE.md",
    "EVIDENCE-PACK.md",
    "ATLAS-SUMMARY-SCHEMA.md",
    "UNSUPPORTED-SURFACE-ROUTER.md",
    "EVIDENCE-GOVERNANCE.md",
    "CLAIM-FIREWALL.md",
    "TOOL-HEALTH-SENTINEL.md",
    "PROTOCOL-COMPLETION.md",
    "REPORT-TEMPLATE.md",
    "scripts/verify_skill_structure.py",
    "scripts/check_protocol_completion.py",
    "scripts/verify_report_consistency.py",
    "scripts/check_claim_ledger.py",
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
    "DEEP mode": "deep",
    "semantic_mode=\"full\"": 'semantic_mode="full"',
    "evidence pack": "evidence pack",
    "evidence manifest": "evidence-manifest.md",
    "atlas-summary.json": "atlas-summary.json",
    "architectural surprises": "architectural surprises",
    "bus-factor function": "bus-factor function",
    "falsification recipes": "falsification recipes",
    "feature atlas mode": "feature_atlas",
    "full/curated symbol distinction": "curated major-symbol",
    "cross-package coupling evidence table": "cross-package coupling evidence",
    "not-a-security-audit framing": "not a vulnerability report",
    "local path scrubber": "local machine paths",
    "unsupported surfaces": "unsupported surfaces",
    "claim firewall": "claim firewall",
    "tool health": "tool health",
    "no generic fallback": "generic source-read overview",
    "no private regression files": "non-public",
}
missing_markers = [label for label, needle in requirements.items() if needle not in text]
if missing_markers:
    print("Smoke test missing required markers:")
    for label in missing_markers:
        print(f" - {label}")
    raise SystemExit(2)

print("OK: smoke test passed")
