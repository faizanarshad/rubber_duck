#!/usr/bin/env python3
from pathlib import Path
import argparse, re

REQUIRED = [
    "Scope and target resolution",
    "Import and module context",
    "Path catalogue",
    "Path-match table",
    "Side-effect manifest",
    "Exception envelope",
    "Witness inputs",
    "Generated tests",
    "Verdict taxonomy applied",
    "Falsification recipes",
    "Tool health",
    "Evidence pack",
]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    p = root / "evidence" / "protocol-completion.md"
    if not p.exists():
        print("missing evidence/protocol-completion.md")
        return 2
    txt = p.read_text(encoding="utf-8", errors="replace")
    errors = []
    for item in REQUIRED:
        if item not in txt:
            errors.append(f"protocol row missing: {item}")
    bad = re.findall(r"\|\s*(no|missing|blocked)\s*\|", txt, flags=re.I)
    if bad:
        errors.append("protocol completion contains unhandled missing/blocked rows")
    if errors:
        print("FAIL: protocol completion check")
        for e in errors:
            print(" -", e)
        return 2
    print("OK: protocol completion check passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
