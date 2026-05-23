#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", required=True)
    args = ap.parse_args()
    p = Path(args.summary)
    data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    errors = []
    for c in data.get("clusters", []):
        cid = c.get("id", "<unknown>")
        named = c.get("named_members", [])
        inline = c.get("inline_members", [])
        roles = c.get("roles", {})
        mergeability = c.get("mergeability")
        if not named and not inline:
            errors.append(f"{cid}: cluster has no members")
        missing_roles = [m for m in list(named) + list(inline) if m not in roles]
        if missing_roles:
            errors.append(f"{cid}: missing roles for {missing_roles}")
        if not mergeability:
            errors.append(f"{cid}: missing mergeability")
        dims = c.get("dimension_coverage", {})
        included = set(c.get("included_dimensions", []))
        for d in included:
            if str(dims.get(d, "")).upper() not in {"COMPUTED", "APPROXIMATED"}:
                errors.append(f"{cid}: included dimension {d} is not computed/approximated")
    if errors:
        print("FAIL: cluster consistency")
        for e in errors:
            print(" -", e)
        return 2
    print("OK: cluster consistency checks passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
