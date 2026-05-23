# Install for Cursor

Copy the Cursor package into the target repository.

## 1. Verify the extracted package first

Run from the extracted package root:

```bash
cd RubberDuck_Nine_Skills_Research_Preview_Beta
python3 verification/run_all_checks.py . --write verification/package_verification_results.json
```

Keep `RUBBERDUCK-CI-BOOTSTRAP.md` with the package and installed skills. For RubberDuck-backed runs, local-only or inaccessible targets must be mirrored to an authorized GitHub repo and analyzed with `detailed_repo_analysis(..., semantic_mode="full")` until CI semantic full completes. Local indexing is only a post-CI fallback for semantic loading gaps.

## 2. Choose the target repository

Set `TARGET_REPO` to the repo where Cursor should use these skills:

```bash
export TARGET_REPO=/absolute/path/to/your/repo
```

## 3. Install Cursor skills and rules into that repo

```bash
mkdir -p "$TARGET_REPO/.cursor"
rsync -a ./cursor/.cursor/ "$TARGET_REPO/.cursor/"
```

If `rsync` is unavailable:

```bash
mkdir -p "$TARGET_REPO/.cursor"
cp -a ./cursor/.cursor/. "$TARGET_REPO/.cursor/"
```

Optional but recommended: add the block from `cursor/AGENTS.md_SNIPPET.md` to the target repo's `AGENTS.md`.

## 4. Verify the installed target

Run from the extracted package root:

```bash
python3 verification/verify_installed_skills.py "$TARGET_REPO/.cursor/skills"   --cursor-rules-root "$TARGET_REPO/.cursor/rules"   --write verification/installed_cursor_results.json
```

## Cursor rules

```text
.cursor/rules/rubberduck-codebase-atlas-pro.mdc
.cursor/rules/rubberduck-security-audit.mdc
.cursor/rules/rubberduck-change-impact-pro.mdc
.cursor/rules/rubberduck-doppelganger-hunt-pro.mdc
.cursor/rules/rubberduck-mirror-pro.mdc
.cursor/rules/rubberduck-schema-code-api-drift-pro.mdc
.cursor/rules/rubberduck-feature-planner-pro.mdc
.cursor/rules/rubberduck-feature-builder-pro.mdc
.cursor/rules/rubberduck-autonomous-feature-mode.mdc
```

The rules are thin adapters. The source of truth remains:

```text
.cursor/skills/rubberduck-codebase-atlas-pro/SKILL.md
.cursor/skills/rubberduck-security-audit/SKILL.md
.cursor/skills/rubberduck-change-impact-pro/SKILL.md
.cursor/skills/rubberduck-doppelganger-hunt-pro/SKILL.md
.cursor/skills/rubberduck-mirror-pro/SKILL.md
.cursor/skills/rubberduck-schema-code-api-drift-pro/SKILL.md
.cursor/skills/rubberduck-feature-planner-pro/SKILL.md
.cursor/skills/rubberduck-feature-builder-pro/SKILL.md
.cursor/skills/rubberduck-autonomous-feature-mode/SKILL.md
```

## Optional per-skill debugging only

If the all-check verifier reports a failure:

```bash
python3 "$TARGET_REPO/.cursor/skills/<skill-slug>/scripts/verify_skill_structure.py"   "$TARGET_REPO/.cursor/skills/<skill-slug>"
python3 "$TARGET_REPO/.cursor/skills/<skill-slug>/scripts/smoke_test_skill.py"   "$TARGET_REPO/.cursor/skills/<skill-slug>"
```

Installed skills:

```text
rubberduck-codebase-atlas-pro
rubberduck-security-audit
rubberduck-change-impact-pro
rubberduck-doppelganger-hunt-pro
rubberduck-mirror-pro
rubberduck-schema-code-api-drift-pro
rubberduck-feature-planner-pro
rubberduck-feature-builder-pro
rubberduck-autonomous-feature-mode
```
