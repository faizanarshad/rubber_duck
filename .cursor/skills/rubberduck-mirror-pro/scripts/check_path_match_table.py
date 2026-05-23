#!/usr/bin/env python3
from pathlib import Path
import argparse, json, re

BAD_STATUSES = ["DIVERGENT", "MISSING_IN_BEFORE", "MISSING_IN_AFTER", "UNDECIDABLE"]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    table = root / "evidence" / "path-match-table.md"
    summary = root / "evidence" / "mirror-summary.json"
    errors = []
    if not table.exists():
        errors.append("missing evidence/path-match-table.md")
    if not summary.exists():
        errors.append("missing evidence/mirror-summary.json")
    if errors:
        print("FAIL: path match table check")
        for e in errors:
            print(" -", e)
        return 2

    txt = table.read_text(encoding="utf-8", errors="replace")
    s = json.loads(summary.read_text(encoding="utf-8", errors="replace"))
    rows = [ln for ln in txt.splitlines() if ln.strip().startswith("|") and "---" not in ln]
    if len(rows) < 2:
        errors.append("path-match-table has no data rows")

    if s.get("verdict") == "PROVEN_EQUIVALENT_UNDER_CONTRACT":
        for bad in BAD_STATUSES:
            if bad in txt:
                errors.append(f"equivalence verdict cannot contain path status {bad}")

    if errors:
        print("FAIL: path match table check")
        for e in errors:
            print(" -", e)
        return 2
    print("OK: path match table check passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
