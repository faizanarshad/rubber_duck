#!/usr/bin/env python3
"""Check claim ledger for unsupported or unlabeled claims."""
from __future__ import annotations
from pathlib import Path
import sys, re

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
ledger = root / "evidence" / "claim-ledger.md"
if not ledger.exists():
    print("Missing evidence/claim-ledger.md")
    raise SystemExit(1)

txt = ledger.read_text(encoding="utf-8", errors="replace")
lower = txt.lower()

if "unsupported" in lower and not any(marker in lower for marker in ["caveat", "out of scope", "blocked"]):
    print("Unsupported claims found without caveat/out-of-scope/blocked marker")
    raise SystemExit(1)

# Heuristic: major claims table should include evidence labels.
if "|" in txt:
    for required in ["claim", "evidence"]:
        if required not in lower:
            print(f"Claim ledger table appears to be missing column/field: {required}")
            raise SystemExit(1)

# Negative claims must not be mixed into positive claim ledger without labeling.
if re.search(r"\bno\s+\w+", lower) and "negative" not in lower and "absence" not in lower:
    print("Potential negative claim in claim-ledger.md without negative/absence labeling")
    raise SystemExit(1)

print("OK: claim ledger check passed")
