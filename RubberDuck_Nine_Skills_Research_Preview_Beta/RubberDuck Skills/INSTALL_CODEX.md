# Install for Codex

Run commands from the extracted package root:

```bash
cd RubberDuck_Nine_Skills_Research_Preview_Beta
python3 verification/run_all_checks.py . --write verification/package_verification_results.json
```

Keep `RUBBERDUCK-CI-BOOTSTRAP.md` with the package and installed skills. For RubberDuck-backed runs, local-only or inaccessible targets must be mirrored to an authorized GitHub repo and analyzed with `detailed_repo_analysis(..., semantic_mode="full")` until CI semantic full completes. Local indexing is only a post-CI fallback for semantic loading gaps.

Install all Codex skills:

```bash
mkdir -p ~/.codex/skills
rsync -a ./codex/skills/ ~/.codex/skills/
```

If `rsync` is unavailable, use `cp -a ./codex/skills/. ~/.codex/skills/`.

Optional: add the Codex AGENTS block from `codex/AGENTS_SNIPPET.md` to:

```text
~/.codex/AGENTS.md
```

Recommended package verification from the extracted package root:

```bash
python3 verification/run_all_checks.py . --write verification/package_verification_results.json
```

Recommended installed-target verification after copying:

```bash
python3 verification/verify_installed_skills.py ~/.codex/skills --write verification/installed_codex_results.json
```

Optional per-skill debugging only, if the all-check verifier reports a failure:

```bash
python3 ~/.codex/skills/<skill-slug>/scripts/verify_skill_structure.py ~/.codex/skills/<skill-slug>
python3 ~/.codex/skills/<skill-slug>/scripts/smoke_test_skill.py ~/.codex/skills/<skill-slug>
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
