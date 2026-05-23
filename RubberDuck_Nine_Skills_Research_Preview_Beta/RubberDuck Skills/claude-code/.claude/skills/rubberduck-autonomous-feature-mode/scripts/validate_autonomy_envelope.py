#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

REQUIRED = ["repo","base_commit","feature_description","tier","max_iterations","max_files_touched","max_new_dependencies","allowed_file_globs","off_limits_file_globs","require_final_user_review"]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("envelope")
    args=ap.parse_args()
    data=json.loads(Path(args.envelope).read_text())
    errors=[f"missing {k}" for k in REQUIRED if k not in data]
    if data.get("tier") not in ["QUICK","STANDARD","DEEP"]:
        errors.append("tier must be QUICK/STANDARD/DEEP")
    for k in ["max_iterations","max_files_touched","max_new_dependencies"]:
        if k in data and (not isinstance(data[k], int) or data[k] < 0):
            errors.append(f"{k} must be nonnegative integer")
    if isinstance(data.get("max_iterations"), int) and data["max_iterations"] <= 0:
        errors.append("max_iterations must be positive")
    if errors:
        print("FAIL")
        for e in errors: print(" -", e)
        sys.exit(2)
    print("OK: autonomy envelope validates")
if __name__=="__main__":
    main()
