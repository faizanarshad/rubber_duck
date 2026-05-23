#!/usr/bin/env python3
"""Lightweight claim ledger checker.

Flags unsupported claims in a markdown claim ledger.

Expected rows should include evidence classes such as:
Tier-2 confirmed, source-confirmed, graph-confirmed, search-confirmed, manual review, unsupported, out of scope.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ALLOWED = [
    "tier-2 confirmed",
    "source-confirmed",
    "graph-confirmed",
    "search-confirmed",
    "manual review",
    "out of scope",
]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("claim_ledger")
    args = ap.parse_args()
    text = Path(args.claim_ledger).read_text(encoding="utf-8", errors="replace")
    bad = []
    for i, line in enumerate(text.splitlines(), 1):
        if "|" not in line or line.strip().startswith("|---"):
            continue
        low = line.lower()
        if "unsupported" in low and not any(term in low for term in ["blocked", "removed", "caveat"]):
            bad.append((i, line))
    if bad:
        print("Unsupported claims require block/remove/caveat status:")
        for i, line in bad:
            print(f"{i}: {line}")
        return 2
    print("OK: no unsupported un-gated claims found.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
