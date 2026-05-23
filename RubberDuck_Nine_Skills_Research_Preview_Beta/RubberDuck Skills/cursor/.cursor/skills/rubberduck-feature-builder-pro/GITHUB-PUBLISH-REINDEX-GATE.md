# GitHub Publish/Re-index Gate

Use this gate after the local final command gate and before final completion.

## Trigger

Trigger the gate when any condition is true:

- The user asks for RubberDuck Codebase Intelligence, Phase 2, indexing, re-indexing, semantic validation, or "use RubberDuck to validate."
- `load_code`, semantic indexing, or codebase-intelligence validation cannot read newly created local files.
- `validate_generated_diff` passed only on a subset of changed files because new files are unindexed.
- The feature creates substantial new modules that need repo-backed analysis.
- The plan, `SIGNOFF.json`, `AUTO_AUTHORIZATION.json`, or Skill Advisor selection says the run should be RubberDuck-validated end-to-end.

## Modes

```text
LOCAL_BUILD_ONLY
GITHUB_VALIDATED_BUILD
AUTO_GITHUB_VALIDATED_BUILD
```

`LOCAL_BUILD_ONLY` may emit `PR_READY.diff` after local gates pass, but must not claim full RubberDuck Codebase Intelligence validation. Final output must include:

```text
Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING
Local build complete; repo-backed RubberDuck validation is pending.
```

`GITHUB_VALIDATED_BUILD` requires explicit user approval before external mutation. Ask approval for:

```text
create a codex/... branch
stage only intended files
commit
push
open PR if appropriate
run/re-poll RubberDuck Codebase Intelligence and Semantic Intelligence
```

`AUTO_GITHUB_VALIDATED_BUILD` is allowed only when `AUTO_AUTHORIZATION.json` or an explicit user message authorizes external GitHub mutation. It runs the same branch/commit/push/index flow without step-by-step prompts.

## Git hygiene

Before any commit or push:

```text
run git status --short
identify unrelated dirty files and exclude them
stage only intended feature files
run a secret scan over staged changes
never stage .env, .env.local, local databases, caches, screenshots with secrets, browser artifacts, cookies, or API keys
never use git reset --hard or destructive checkout
prefer a new branch named codex/<feature-slug>
if already on main, create a feature branch before committing
inspect and preserve unexpected changes in files Builder must edit
```

## Repo-backed RubberDuck validation

After pushing:

```text
run or re-run detailed_repo_analysis(repo=..., branch=..., semantic_mode="full")
re-poll until the full report completes or a concrete blocker is reached
run semantic get_started(repo=...) when available
save index_status.instance_id
pass instance_id to load_code
use max_files=2000 or enough file-pattern loads to cover changed files
validate newly created files, not only pre-existing tracked files
record validation IDs and blockers
```

## Required evidence

When this gate runs, write:

```text
uc07/<slug>/evidence/github-publish.md
uc07/<slug>/evidence/repo-backed-rubberduck-validation.md
uc07/<slug>/evidence/indexed-files-coverage.md
```

`github-publish.md` includes branch, commit hash, pushed remote, PR URL if any, staged file list, and secret-scan result.

`repo-backed-rubberduck-validation.md` includes RubberDuck tool calls, repo/branch/commit, indexing status, validation result, validation IDs, and known limitations.

`indexed-files-coverage.md` includes changed files, new files, loaded files or patterns, coverage result, and gaps.

Use `Validation status: FULL_REPO_BACKED_RUBBERDUCK_VALIDATED` only if this evidence proves repo-backed validation ran against the pushed commit or branch and includes new files.
