#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

ALLOWED = {
    "PROVEN_EQUIVALENT_UNDER_CONTRACT",
    "NOT_EQUIVALENT",
    "CONDITIONALLY_EQUIVALENT",
    "EQUIVALENT_WITH_STRUCTURAL_DRIFT",
    "UNDECIDABLE",
    "HEURISTIC_ONLY",
}

def load_summary(root: Path) -> dict:
    p = root / "evidence" / "mirror-summary.json"
    if not p.exists():
        raise SystemExit("missing evidence/mirror-summary.json")
    return json.loads(p.read_text(encoding="utf-8", errors="replace"))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    s = load_summary(root)
    errors = []

    verdict = s.get("verdict", "")
    if verdict not in ALLOWED:
        errors.append(f"invalid verdict: {verdict}")
    if not s.get("preserved_contract"):
        errors.append("missing preserved_contract")

    divergence_count = int(s.get("divergence_count", 0) or 0)
    undecidable_count = int(s.get("undecidable_count", 0) or 0)
    generated_tests = int(s.get("generated_tests", 0) or 0)

    if verdict == "PROVEN_EQUIVALENT_UNDER_CONTRACT":
        if divergence_count != 0:
            errors.append("PROVEN_EQUIVALENT_UNDER_CONTRACT cannot have divergences")
        if undecidable_count != 0:
            errors.append("PROVEN_EQUIVALENT_UNDER_CONTRACT cannot have undecidable blockers")
        if not s.get("side_effects_compared", False) and not s.get("side_effects_out_of_scope", False):
            errors.append("equivalence verdict requires side-effect comparison or explicit out-of-scope")
        if not s.get("exceptions_compared", False) and not s.get("exceptions_out_of_scope", False):
            errors.append("equivalence verdict requires exception comparison or explicit out-of-scope")

    if verdict == "NOT_EQUIVALENT":
        if divergence_count < 1:
            errors.append("NOT_EQUIVALENT requires at least one divergence")
        witness = root / "evidence" / "witness-inputs.md"
        if not witness.exists() or ("Status: unavailable" in witness.read_text(encoding="utf-8", errors="replace") and "Reason:" not in witness.read_text(encoding="utf-8", errors="replace")):
            errors.append("NOT_EQUIVALENT requires witness inputs or a documented blocker")
        if generated_tests < 1 and not (root / "evidence" / "generated-tests.md").exists():
            errors.append("NOT_EQUIVALENT requires generated tests or a documented reason")

    if verdict == "HEURISTIC_ONLY" and "proven" in str(s.get("confidence", "")).lower():
        errors.append("HEURISTIC_ONLY cannot claim proven confidence")

    if errors:
        print("FAIL: mirror verdict check")
        for e in errors:
            print(" -", e)
        return 2
    print("OK: mirror verdict check passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
