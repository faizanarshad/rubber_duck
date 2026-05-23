#!/usr/bin/env python3
from pathlib import Path
import argparse

REQUIRED = [
    "mode declared",
    "RubberDuck setup",
    "layer inventory",
    "concept extraction",
    "concept fusion",
    "drift matrix",
    "runtime failure prediction",
    "round-trip proof",
    "remediation diffs",
    "negative claims",
    "falsification recipes",
    "evidence pack",
]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("protocol_completion")
    args = ap.parse_args()
    txt = Path(args.protocol_completion).read_text(encoding="utf-8", errors="replace").lower()
    missing = [r for r in REQUIRED if r.lower() not in txt]
    if missing:
        print("FAIL: protocol completion missing:")
        for m in missing:
            print(" -", m)
        return 2
    print("OK: protocol completion check passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
