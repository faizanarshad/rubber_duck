#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path

REQUIRED = [
    "Mode declared",
    "Candidate generators run",
    "Graph dimension coverage recorded",
    "Inline implementations searched",
    "Comment contracts searched",
    "Cluster roles assigned",
    "Mergeability classified",
    "Change-impact preflight complete",
    "Negative results enumerated",
    "Falsification recipes written",
]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    p = root / "evidence" / "protocol-completion.md"
    if not p.exists():
        print("FAIL: missing evidence/protocol-completion.md")
        return 2
    txt = p.read_text(encoding="utf-8", errors="replace")
    errors = [r for r in REQUIRED if r not in txt]
    if "Incomplete" in txt or "NOT DONE" in txt:
        errors.append("protocol-completion.md contains incomplete marker")
    if errors:
        print("FAIL: protocol completion")
        for e in errors:
            print(" -", e)
        return 2
    print("OK: protocol completion checks passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
