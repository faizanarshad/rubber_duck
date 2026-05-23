#!/usr/bin/env python3
from pathlib import Path
import argparse, re

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fusion_ledger")
    args = ap.parse_args()
    txt = Path(args.fusion_ledger).read_text(encoding="utf-8", errors="replace")
    errors = []
    if "HIGH" not in txt and "MEDIUM" not in txt and "LOW" not in txt and "REJECTED" not in txt:
        errors.append("fusion ledger lacks confidence labels")
    # LOW concepts must not be marked as final drift.
    for line in txt.splitlines():
        low = line.lower()
        if "low" in low and ("final drift" in low or "confirmed drift" in low):
            errors.append("LOW confidence fusion appears promoted to final drift")
    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 2
    print("OK: concept fusion check passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
