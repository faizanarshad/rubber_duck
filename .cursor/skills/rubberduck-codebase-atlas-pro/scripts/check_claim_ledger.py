#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys

report = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("REPORT.md")
if report.is_dir():
    report = report / "REPORT.md"
if not report.exists():
    print(f"Missing report: {report}")
    sys.exit(1)

text = report.read_text(encoding="utf-8", errors="replace")
root = report.parent
claim_ledger = root / "evidence" / "claim-ledger.md"
if "Evidence Ledger" not in text and not claim_ledger.exists():
    print("Missing Evidence Ledger")
    sys.exit(1)

if claim_ledger.exists():
    text = text + "\n" + claim_ledger.read_text(encoding="utf-8", errors="replace")

labels = [
    "symbols-confirmed",
    "call-chain-confirmed",
    "data-flow-confirmed",
    "search-confirmed",
    "codebase-metric-confirmed",
    "source-confirmed",
    "manual inference",
    "unsupported",
    "out of scope",
]
if not any(label in text.lower() for label in labels):
    print("Evidence Ledger exists but no recognized evidence labels found")
    sys.exit(2)

if "raw tool output" not in text.lower() and "normalized evidence" not in text.lower() and "report-derived evidence" not in text.lower():
    print("Claim/evidence materials do not declare evidence level")
    sys.exit(3)

print("OK: claim ledger check passed")
