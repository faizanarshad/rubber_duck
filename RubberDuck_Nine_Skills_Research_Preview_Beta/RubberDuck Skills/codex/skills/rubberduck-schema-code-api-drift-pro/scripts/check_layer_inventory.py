#!/usr/bin/env python3
from pathlib import Path
import argparse, re

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inventory")
    args = ap.parse_args()
    txt = Path(args.inventory).read_text(encoding="utf-8", errors="replace")
    required_terms = ["DB_SCHEMA", "CODE_TYPE", "API_CONTRACT"]
    missing = [t for t in required_terms if t not in txt]
    if missing:
        print("FAIL: layer inventory missing core terms:", ", ".join(missing))
        return 2
    if "Status" not in txt and "status" not in txt:
        print("FAIL: layer inventory must include status/caveats")
        return 2
    print("OK: layer inventory check passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
