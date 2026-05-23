#!/usr/bin/env python3
"""Check protocol completion file/report markers."""
from __future__ import annotations
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
protocol = root / "evidence" / "protocol-completion.md"
if not protocol.exists():
    print("Missing evidence/protocol-completion.md")
    raise SystemExit(1)
txt = protocol.read_text(encoding="utf-8", errors="replace")
if "[ ]" in txt:
    print("Incomplete protocol items remain")
    raise SystemExit(1)
print("OK: protocol completion check passed")
