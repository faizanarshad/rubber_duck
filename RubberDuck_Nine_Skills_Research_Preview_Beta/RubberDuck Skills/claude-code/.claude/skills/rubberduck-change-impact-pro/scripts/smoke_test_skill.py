#!/usr/bin/env python3
"""Smoke test RubberDuck Change Impact Pro skill files."""
from __future__ import annotations
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
markers = {
    "SKILL.md": ["rubberduck-change-impact-pro", "DEEP", "Dual-Source", "Runtime Optimization"],
    "DUAL-SOURCE-ADJUDICATION.md": ["adopted truth", "call_chain", "search_code"],
    "SHADOW-PREFLIGHT.md": ["Doppelganger", "Do not halt"],
    "COMMENT-CONTRACTS.md": ["Comment Contract"],
    "MOCK-BREAKAGE.md": ["breaks loudly", "breaks silently"],
    "RUNTIME-OPTIMIZATION.md": ["same observable result", "±5%"],
    "EVIDENCE-PACK.md": ["impact-summary.json", "dual-source-adjudication.md"],
}
for rel, needles in markers.items():
    p = root / rel
    if not p.exists():
        print(f"Missing {rel}")
        raise SystemExit(1)
    txt = p.read_text(encoding="utf-8", errors="replace")
    for needle in needles:
        if needle not in txt:
            print(f"{rel} missing marker: {needle}")
            raise SystemExit(1)
print("OK: Change Impact Pro smoke test passed")
