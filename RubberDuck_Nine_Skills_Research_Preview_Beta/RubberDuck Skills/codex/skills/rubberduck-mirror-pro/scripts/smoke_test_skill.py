#!/usr/bin/env python3
from pathlib import Path
import json, tempfile, runpy, sys, contextlib, io

def run(script: Path, args: list[str], cwd: Path) -> int:
    script = script.resolve()
    cwd = cwd.resolve()
    old_argv = sys.argv[:]
    old_path = sys.path[:]
    old_cwd = Path.cwd()
    try:
        sys.argv = [str(script)] + args
        sys.path.insert(0, str(script.parent))
        import os
        os.chdir(cwd)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                runpy.run_path(str(script), run_name="__main__")
                return 0
            except SystemExit as e:
                return e.code if isinstance(e.code, int) else 1
    finally:
        sys.argv = old_argv
        sys.path[:] = old_path
        import os
        os.chdir(old_cwd)

def make_bundle(root: Path, verdict="NOT_EQUIVALENT", divergence_count=1, undecidable_count=0, proven_bad=False):
    (root / "evidence").mkdir(parents=True)
    report_sections = [
        "§0 Envelope",
        "§1 Verdict",
        "§2 Headline",
        "§3 Input",
        "§4 Import",
        "§5 Path Catalogue",
        "§6 Path-Match Table",
        "§7 Divergences",
        "§8 Side-Effect",
        "§9 Exception",
        "§10 Witness",
        "§11 Generated",
        "§12 Undecidable",
        "§13 Structural",
        "§14 Falsification",
        "§15 Tool Health",
        "§16 Evidence Pack",
    ]
    report = "# Mirror Report\n\nPreserved contract: observable-behavior\n\n" + "\n\n".join("## " + s + "\ncontent" for s in report_sections)
    (root / "REPORT.md").write_text(report, encoding="utf-8")
    summary = {
        "mode": "sibling-equivalence",
        "preserved_contract": "observable-behavior",
        "verdict": verdict,
        "divergence_count": divergence_count,
        "undecidable_count": undecidable_count,
        "generated_tests": 1,
        "confidence": "high",
        "side_effects_compared": True,
        "exceptions_compared": True,
    }
    if proven_bad:
        summary["verdict"] = "PROVEN_EQUIVALENT_UNDER_CONTRACT"
        summary["divergence_count"] = 1
    (root / "evidence/mirror-summary.json").write_text(json.dumps(summary), encoding="utf-8")
    required = [
        "before-source.md","after-source.md","import-context.md","path-catalogue-before.md","path-catalogue-after.md",
        "side-effect-manifest.md","exception-envelope.md","witness-inputs.md","generated-tests.md","undecidable-blockers.md",
        "structural-drift.md","falsification-recipes.md","tool-health.md",
    ]
    for name in required:
        (root / "evidence" / name).write_text("# " + name + "\ncontent", encoding="utf-8")
    (root / "evidence/path-match-table.md").write_text(
        "| BEFORE path | AFTER path | Status | Divergence | Evidence |\n|---|---|---|---|---|\n| p1 | p1 | DIVERGENT | observable drift | source |\n",
        encoding="utf-8",
    )
    protocol_rows = [
        "Scope and target resolution","Import and module context","Path catalogue","Path-match table","Side-effect manifest",
        "Exception envelope","Witness inputs","Generated tests","Verdict taxonomy applied","Falsification recipes","Tool health","Evidence pack",
    ]
    (root / "evidence/protocol-completion.md").write_text("\n".join(f"| {r} | yes | evidence |" for r in protocol_rows), encoding="utf-8")

def main() -> int:
    skill_dir = (Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")).resolve()
    scripts = skill_dir / "scripts"
    with tempfile.TemporaryDirectory() as td:
        valid = Path(td) / "valid"
        valid.mkdir()
        make_bundle(valid)
        for script, args in [
            ("verify_report_consistency.py", ["--root", str(valid)]),
            ("check_mirror_verdict.py", ["--root", str(valid)]),
            ("check_path_match_table.py", ["--root", str(valid)]),
            ("check_protocol_completion.py", ["--root", str(valid)]),
        ]:
            code = run(scripts / script, args, skill_dir)
            if code != 0:
                print(f"valid fixture failed {script}: {code}")
                return 2

        invalid = Path(td) / "invalid"
        invalid.mkdir()
        make_bundle(invalid, proven_bad=True)
        code = run(scripts / "check_mirror_verdict.py", ["--root", str(invalid)], skill_dir)
        if code == 0:
            print("invalid proven-equivalent-with-divergence fixture passed unexpectedly")
            return 2

    print("OK: Mirror Pro smoke test passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
