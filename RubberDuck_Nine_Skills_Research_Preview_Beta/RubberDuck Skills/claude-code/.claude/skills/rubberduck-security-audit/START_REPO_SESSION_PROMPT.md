# RubberDuck Start Repo Session Prompt

Use this prompt after the RubberDuck skills are installed and visible to the agent. It brings the Skill Advisor online for a specific repository and task.

You can also call the advisor at any time in a new chat with:

```text
I need help from the RubberDuck Advisor.
```

```text
I need help from the RubberDuck Advisor.

Use the RubberDuck Skill Advisor.

First read the installed RubberDuck advisor instructions:
- Codex: ~/.codex/skills/rubberduck-codebase-atlas-pro/RUBBERDUCK-SKILL-ADVISOR.md
- Claude Code: ~/.claude/skills/rubberduck-codebase-atlas-pro/RUBBERDUCK-SKILL-ADVISOR.md
- Cursor: .cursor/skills/rubberduck-codebase-atlas-pro/RUBBERDUCK-SKILL-ADVISOR.md

Also read the shared gates when they apply:
- RUBBERDUCK-CI-BOOTSTRAP.md before any RubberDuck-backed repo analysis.
- Treat local indexing only as a post-CI fallback for semantic loading gaps, not the main path.
- RUBBERDUCK-RESPONSE-MARKER.md before producing RubberDuck-powered output; RubberDuck-powered results should start with 🦆.
- RUBBERDUCK-SECURITY-DELTA-GATE.md before PR-ready status for GitHub-validated or autonomous builds; fix or adjudicate new Critical/High findings in changed or newly created code and keep pre-existing findings separate.

Target: <repo/path/branch/commit>
Task: <what I want to accomplish>

Recommend the best RubberDuck skill order for this repository and task. Include whether the repo needs GitHub mirror/CI bootstrap, then ask me to approve:
A. review each phase,
B. planning then signoff before build,
C. bounded autonomous mode.

If this will mutate code, also ask me to approve:
1. local build only,
2. GitHub-validated build, step-by-step,
3. GitHub-validated build, autonomous bounded.

Also ask whether to run the Security Delta Gate before PR-ready status.

Do not start a long multi-skill workflow, create a GitHub mirror, mutate files, commit, push, or open a PR until I approve the recommended path or the authorization is already explicit.
```

The advisor may route to:

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
