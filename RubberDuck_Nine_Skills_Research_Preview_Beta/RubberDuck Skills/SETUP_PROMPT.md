# RubberDuck First-Time Installation Prompt

Use this prompt when someone receives `RubberDuck_Nine_Skills_Research_Preview_Beta_Clean.zip` for the first time and wants an agent to install it correctly. Paste the whole prompt into Codex, Claude Code, or Cursor along with the zip path.

```text
You are installing the RubberDuck Nine Skills Research Preview Beta package from a zip file.

Source package:
<path/to/RubberDuck_Nine_Skills_Research_Preview_Beta_Clean.zip>

Your job:
Install the full RubberDuck nine-skill package for this environment, verify the package before and after installation, and do not claim success unless the checks pass.

Expected package root after extraction:
RubberDuck Skills/

Expected skills:
- rubberduck-codebase-atlas-pro
- rubberduck-security-audit
- rubberduck-change-impact-pro
- rubberduck-doppelganger-hunt-pro
- rubberduck-mirror-pro
- rubberduck-schema-code-api-drift-pro
- rubberduck-feature-planner-pro
- rubberduck-feature-builder-pro
- rubberduck-autonomous-feature-mode

Non-negotiable rules:
1. Do not install blindly.
2. Do not skip validation.
3. Do not silently ignore missing skills.
4. Do not mutate a user project except to install Cursor rules into the explicitly selected target repo.
5. Do not delete existing unrelated skills.
6. Preserve backups of replaced RubberDuck skill folders.
7. Do not claim the Skill Advisor is ready until installed-target verification passes.

Installation sequence:

1. Locate and extract the zip into a temporary work directory. The clean zip has two top-level prompts and one package folder:

   RubberDuck Skills/

   Use `RubberDuck Skills/` as the package root. If the archive was unpacked differently, use the directory that contains `verification/run_all_checks.py`, `codex/`, `claude-code/`, and `cursor/`.

2. From the extracted package root, run:

   python3 verification/run_all_checks.py . --write verification/package_verification_results.json

   If this fails, stop and report the failure. Do not install.

3. Install Codex skills if Codex is the target or if ~/.codex/skills exists. Back up replaced RubberDuck skill folders first:

   mkdir -p ~/.codex/skills ~/.codex/skills-backups
   BACKUP_DIR="$HOME/.codex/skills-backups/rubberduck-nine-skills-$(date -u +%Y%m%dT%H%M%SZ)"
   mkdir -p "$BACKUP_DIR"
   for skill in rubberduck-codebase-atlas-pro rubberduck-security-audit rubberduck-change-impact-pro rubberduck-doppelganger-hunt-pro rubberduck-mirror-pro rubberduck-schema-code-api-drift-pro rubberduck-feature-planner-pro rubberduck-feature-builder-pro rubberduck-autonomous-feature-mode; do
     [ -d "$HOME/.codex/skills/$skill" ] && mv "$HOME/.codex/skills/$skill" "$BACKUP_DIR/$skill"
     cp -R "codex/skills/$skill" "$HOME/.codex/skills/$skill"
   done
   python3 verification/verify_installed_skills.py ~/.codex/skills

4. Install Claude Code skills if Claude Code is the target or if ~/.claude/skills exists. Back up replaced RubberDuck skill folders first:

   mkdir -p ~/.claude/skills ~/.claude/skills-backups
   BACKUP_DIR="$HOME/.claude/skills-backups/rubberduck-nine-skills-$(date -u +%Y%m%dT%H%M%SZ)"
   mkdir -p "$BACKUP_DIR"
   for skill in rubberduck-codebase-atlas-pro rubberduck-security-audit rubberduck-change-impact-pro rubberduck-doppelganger-hunt-pro rubberduck-mirror-pro rubberduck-schema-code-api-drift-pro rubberduck-feature-planner-pro rubberduck-feature-builder-pro rubberduck-autonomous-feature-mode; do
     [ -d "$HOME/.claude/skills/$skill" ] && mv "$HOME/.claude/skills/$skill" "$BACKUP_DIR/$skill"
     cp -R "claude-code/.claude/skills/$skill" "$HOME/.claude/skills/$skill"
   done
   python3 verification/verify_installed_skills.py ~/.claude/skills

5. Install Cursor skills only into the selected target repo, not into the package root. Back up replaced RubberDuck skill folders and rules first:

   TARGET_REPO=<absolute/path/to/the/repo/that/should/get/Cursor/rules>
   mkdir -p "$TARGET_REPO/.cursor/skills" "$TARGET_REPO/.cursor/rules" "$TARGET_REPO/.cursor/skills-backups"
   BACKUP_DIR="$TARGET_REPO/.cursor/skills-backups/rubberduck-nine-skills-$(date -u +%Y%m%dT%H%M%SZ)"
   mkdir -p "$BACKUP_DIR/skills" "$BACKUP_DIR/rules"
   for skill in rubberduck-codebase-atlas-pro rubberduck-security-audit rubberduck-change-impact-pro rubberduck-doppelganger-hunt-pro rubberduck-mirror-pro rubberduck-schema-code-api-drift-pro rubberduck-feature-planner-pro rubberduck-feature-builder-pro rubberduck-autonomous-feature-mode; do
     [ -d "$TARGET_REPO/.cursor/skills/$skill" ] && mv "$TARGET_REPO/.cursor/skills/$skill" "$BACKUP_DIR/skills/$skill"
     [ -f "$TARGET_REPO/.cursor/rules/$skill.mdc" ] && mv "$TARGET_REPO/.cursor/rules/$skill.mdc" "$BACKUP_DIR/rules/$skill.mdc"
     cp -R "cursor/.cursor/skills/$skill" "$TARGET_REPO/.cursor/skills/$skill"
     cp "cursor/.cursor/rules/$skill.mdc" "$TARGET_REPO/.cursor/rules/$skill.mdc"
   done
   python3 verification/verify_installed_skills.py "$TARGET_REPO/.cursor/skills" --cursor-rules-root "$TARGET_REPO/.cursor/rules"

6. Confirm that all nine expected skills exist in the installed target.

7. Tell the user whether a restart/reload is needed for their tool to see the new skills.

8. After installation passes, tell the user to restart or reload their tool, then show this exact handoff:

   🦆 RubberDuck skills are installed and verified.

   Restart or reload your IDE/Codex/Claude Code/Cursor now so the new skills become visible.

   After restart, you can call the advisor from any chat with:

   I need help from the RubberDuck Advisor.

   To start immediately after restart, paste:

   I need help from the RubberDuck Advisor.
   Target: <repo/path/branch/commit>
   Task: <what you want to accomplish>

   The same starter prompt is stored in START_REPO_SESSION_PROMPT.md.

Final response must include:
- package path
- installed target(s)
- backup location(s), if any
- package verification result
- installed-target verification result
- missing tools or blockers, if any
- whether the Skill Advisor is ready
- the exact advisor activation phrase: I need help from the RubberDuck Advisor.

Do not run RubberDuck analysis during installation. Installation is complete only when package verification and installed-target verification pass.
```

After the tool restarts or reloads skills, start repository work with:

```text
I need help from the RubberDuck Advisor.
```
