#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, sys

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("drift_matrix_csv")
    args = ap.parse_args()
    p = Path(args.drift_matrix_csv)
    rows = list(csv.DictReader(p.read_text(encoding="utf-8", errors="replace").splitlines()))
    required = {"concept_id", "canonical_concept", "layers_compared", "dimension", "status", "evidence", "confidence"}
    if not rows:
        print("FAIL: drift matrix has no rows")
        return 2
    missing_cols = required - set(rows[0].keys())
    if missing_cols:
        print("FAIL: missing columns:", ", ".join(sorted(missing_cols)))
        return 2
    errors = []
    for i, row in enumerate(rows, 2):
        layers = [x.strip() for x in row.get("layers_compared", "").split(";") if x.strip()]
        if row.get("status") == "DRIFT" and len(layers) < 2:
            errors.append(f"row {i}: DRIFT with fewer than two layers")
        if row.get("status") == "DRIFT" and not row.get("evidence"):
            errors.append(f"row {i}: DRIFT without evidence")
    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 2
    print("OK: drift matrix check passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
