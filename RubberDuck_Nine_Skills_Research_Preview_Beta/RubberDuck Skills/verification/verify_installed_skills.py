#!/usr/bin/env python3
"""Verify an installed skills directory after copying the bundle.

Usage:
  python3 verification/verify_installed_skills.py ~/.codex/skills
  python3 verification/verify_installed_skills.py ~/.claude/skills
  python3 verification/verify_installed_skills.py .cursor/skills

This checks only the installed target root, not the all-platform package tree.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import runpy
import sys
from pathlib import Path

SKILLS = [
    "rubberduck-codebase-atlas-pro",
    "rubberduck-security-audit",
    "rubberduck-change-impact-pro",
    "rubberduck-doppelganger-hunt-pro",
    "rubberduck-mirror-pro",
    "rubberduck-schema-code-api-drift-pro",
    "rubberduck-feature-planner-pro",
    "rubberduck-feature-builder-pro",
    "rubberduck-autonomous-feature-mode",
]

def run_script(script: Path, argv: list[str]) -> dict:
    old_argv = sys.argv[:]
    old_path = sys.path[:]
    out = io.StringIO()
    err = io.StringIO()
    code = 0
    try:
        sys.argv = [str(script)] + argv
        sys.path.insert(0, str(script.parent))
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                runpy.run_path(str(script), run_name="__main__")
            except SystemExit as e:
                if isinstance(e.code, int):
                    code = e.code
                elif e.code is None:
                    code = 0
                else:
                    code = 1
                    print(str(e.code), file=err)
    except Exception as e:
        code = 99
        print(repr(e), file=err)
    finally:
        sys.argv = old_argv
        sys.path[:] = old_path
    return {"exit_code": code, "stdout": out.getvalue(), "stderr": err.getvalue()}


def has_wrong_duck_name(text: str) -> bool:
    lowered = text.lower()
    compact = "robot" + "duck"
    spaced = "robot" + " " + "duck"
    return compact in lowered or spaced in lowered


def check_bootstrap(skill_dir: Path) -> list[str]:
    failures: list[str] = []
    bootstrap = skill_dir / "RUBBERDUCK-CI-BOOTSTRAP.md"
    marker = skill_dir / "RUBBERDUCK-RESPONSE-MARKER.md"
    advisor = skill_dir / "RUBBERDUCK-SKILL-ADVISOR.md"
    start_prompt = skill_dir / "START_REPO_SESSION_PROMPT.md"
    security_delta = skill_dir / "RUBBERDUCK-SECURITY-DELTA-GATE.md"
    skill_md = skill_dir / "SKILL.md"
    if not bootstrap.exists():
        failures.append(f"missing bootstrap: {skill_dir.name}/RUBBERDUCK-CI-BOOTSTRAP.md")
        return failures
    text = bootstrap.read_text(encoding="utf-8", errors="replace")
    for required_marker in [
        "GitHub mirror",
        "RubberDuck GitHub App",
        "detailed_repo_analysis",
        'semantic_mode="full"',
        "Codebase Intelligence Phase 2",
        "not a substitute",
        "post-CI fallback",
    ]:
        if required_marker not in text:
            failures.append(f"bootstrap missing marker {required_marker!r}: {skill_dir.name}")
    if skill_md.exists():
        skill_text = skill_md.read_text(encoding="utf-8", errors="replace")
        skill_lower = skill_text.lower()
        if "RUBBERDUCK-CI-BOOTSTRAP.md" not in skill_text:
            failures.append(f"SKILL.md missing bootstrap reference: {skill_dir.name}")
        if "RUBBERDUCK-RESPONSE-MARKER.md" not in skill_text:
            failures.append(f"SKILL.md missing response marker reference: {skill_dir.name}")
        if "RUBBERDUCK-SKILL-ADVISOR.md" not in skill_text:
            failures.append(f"SKILL.md missing skill advisor reference: {skill_dir.name}")
        if "🦆" not in skill_text:
            failures.append(f"SKILL.md missing duck response marker: {skill_dir.name}")
        if has_wrong_duck_name(skill_lower):
            failures.append(f"SKILL.md contains wrong duck-name wording: {skill_dir.name}")
        if "local/repo" in skill_text:
            failures.append(f"SKILL.md uses local/repo as primary repo placeholder: {skill_dir.name}")
    if not marker.exists():
        failures.append(f"missing response marker: {skill_dir.name}/RUBBERDUCK-RESPONSE-MARKER.md")
    else:
        marker_text = marker.read_text(encoding="utf-8", errors="replace")
        marker_lower = marker_text.lower()
        if "🦆" not in marker_text:
            failures.append(f"response marker file missing duck marker: {skill_dir.name}")
        if has_wrong_duck_name(marker_lower):
            failures.append(f"response marker file contains wrong duck-name wording: {skill_dir.name}")
    if not advisor.exists():
        failures.append(f"missing skill advisor: {skill_dir.name}/RUBBERDUCK-SKILL-ADVISOR.md")
    else:
        advisor_text = advisor.read_text(encoding="utf-8", errors="replace")
        for required in ["RubberDuck Skill Recommendation", "Please approve A, B, or C", "autonomous"]:
            if required not in advisor_text:
                failures.append(f"skill advisor missing marker {required!r}: {skill_dir.name}")
    if not start_prompt.exists():
        failures.append(f"missing start repo session prompt: {skill_dir.name}/START_REPO_SESSION_PROMPT.md")
    else:
        setup_text = start_prompt.read_text(encoding="utf-8", errors="replace")
        for required in [
            "Use the RubberDuck Skill Advisor",
            "RUBBERDUCK-SKILL-ADVISOR.md",
            "GitHub-validated build",
            "Security Delta Gate",
        ]:
            if required not in setup_text:
                failures.append(f"start repo session prompt missing marker {required!r}: {skill_dir.name}")
    if skill_dir.name == "rubberduck-feature-builder-pro":
        combined = ""
        for rel in [
            "SKILL.md",
            "GITHUB-PUBLISH-REINDEX-GATE.md",
            "GITHUB-VALIDATION-SELF-CHECK.md",
            "RUBBERDUCK-SECURITY-DELTA-GATE.md",
            "scripts/validate_final_build_package.py",
        ]:
            p = skill_dir / rel
            if not p.exists():
                failures.append(f"builder missing GitHub validation file: {rel}")
                continue
            combined += "\n" + p.read_text(encoding="utf-8", errors="replace")
        for required in [
            "GitHub Publish/Re-index Gate",
            "LOCAL_BUILD_ONLY",
            "GITHUB_VALIDATED_BUILD",
            "AUTO_GITHUB_VALIDATED_BUILD",
            "Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED",
            "Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING",
            "Validation status: BLOCKED_BEFORE_REPO_BACKED_VALIDATION",
            "github-publish.md",
            "repo-backed-rubberduck-validation.md",
            "indexed-files-coverage.md",
            "BUILD.md must contain exactly one validation status label",
            "BUILD.md must contain exactly one security delta status label",
            "Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH",
            "security-delta.json",
        ]:
            if required not in combined:
                failures.append(f"builder GitHub validation marker missing {required!r}")
    if skill_dir.name in {"rubberduck-feature-builder-pro", "rubberduck-autonomous-feature-mode", "rubberduck-security-audit"}:
        if not security_delta.exists():
            failures.append(f"missing security delta gate: {skill_dir.name}/RUBBERDUCK-SECURITY-DELTA-GATE.md")
        else:
            delta_text = security_delta.read_text(encoding="utf-8", errors="replace")
            for required in [
                "Security delta status: CLEAN_NO_NEW_CRITICAL_HIGH",
                "Security delta status: BLOCKED_NEW_UNRESOLVED_FINDINGS",
                "pre_existing_findings",
                "security-delta.json",
            ]:
                if required not in delta_text:
                    failures.append(f"security delta gate missing marker {required!r}: {skill_dir.name}")
        if skill_md.exists() and "RUBBERDUCK-SECURITY-DELTA-GATE.md" not in skill_md.read_text(encoding="utf-8", errors="replace"):
            failures.append(f"SKILL.md missing security delta reference: {skill_dir.name}")
    return failures

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skills_root", help="Installed skills root, e.g. ~/.codex/skills")
    ap.add_argument("--write", default="", help="Optional JSON output path")
    ap.add_argument("--cursor-rules-root", default="", help="Optional Cursor rules root, e.g. .cursor/rules")
    args = ap.parse_args()

    root = Path(args.skills_root).expanduser().resolve()
    result = {
        "skills_root": str(root),
        "checks": {},
        "failures": [],
        "skills": SKILLS,
    }

    if not root.exists():
        result["failures"].append(f"skills root does not exist: {root}")

    for skill in SKILLS:
        skill_dir = root / skill
        if not skill_dir.exists():
            result["failures"].append(f"missing installed skill: {skill}")
            continue
        for failure in check_bootstrap(skill_dir):
            result["failures"].append(failure)
        for script_name in ["verify_skill_structure.py", "smoke_test_skill.py"]:
            script = skill_dir / "scripts" / script_name
            key = f"{skill}:{script_name}"
            if not script.exists():
                result["failures"].append(f"missing script: {key}")
                result["checks"][key] = {"exit_code": 1, "stdout": "", "stderr": "missing script"}
                continue
            res = run_script(script, [str(skill_dir)])
            result["checks"][key] = res
            if res["exit_code"] != 0:
                result["failures"].append(f"check failed: {key}")

    if args.cursor_rules_root:
        rules_root = Path(args.cursor_rules_root).expanduser().resolve()
        result["cursor_rules_root"] = str(rules_root)
        result["cursor_rules"] = {}
        if not rules_root.exists():
            result["failures"].append(f"cursor rules root does not exist: {rules_root}")
        for skill in SKILLS:
            rule = rules_root / f"{skill}.mdc"
            key = f"cursor-rule:{skill}"
            exists = rule.exists()
            result["cursor_rules"][key] = exists
            if not exists:
                result["failures"].append(f"missing cursor rule: {rule}")
            else:
                rule_text = rule.read_text(encoding="utf-8", errors="replace")
                if skill not in rule_text:
                    result["failures"].append(f"cursor rule does not reference skill slug: {rule}")
                if "RUBBERDUCK-CI-BOOTSTRAP.md" not in rule_text:
                    result["failures"].append(f"cursor rule missing bootstrap reference: {rule}")
                if "post-CI fallback" not in rule_text:
                    result["failures"].append(f"cursor rule missing post-CI fallback boundary: {rule}")
                if "RUBBERDUCK-RESPONSE-MARKER.md" not in rule_text:
                    result["failures"].append(f"cursor rule missing response marker reference: {rule}")
                if "RUBBERDUCK-SKILL-ADVISOR.md" not in rule_text:
                    result["failures"].append(f"cursor rule missing skill advisor reference: {rule}")
                if "🦆" not in rule_text:
                    result["failures"].append(f"cursor rule missing duck response marker: {rule}")
                if has_wrong_duck_name(rule_text):
                    result["failures"].append(f"cursor rule contains wrong duck-name wording: {rule}")

    if args.write:
        out = Path(args.write)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

    print(json.dumps({
        "skills_root": str(root),
        "checks_run": len(result["checks"]),
        "failures": len(result["failures"]),
        "skills": SKILLS,
    }, indent=2))
    if result["failures"]:
        print("FAILURES:")
        for failure in result["failures"]:
            print(f" - {failure}")
        return 2
    print("OK: installed skill target checks passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
