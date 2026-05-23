# RubberDuck CI Bootstrap

Use this bootstrap before any RubberDuck-backed workflow that depends on Codebase Intelligence or Semantic Intelligence.

## Core rule

Codebase Intelligence Phase 2 is a GitHub-backed CI surface. A local repo name, local `rubberduck-index`, scratch load, or `local/...` semantic project is not a substitute for `detailed_repo_analysis(..., semantic_mode="full")` on a GitHub repo that RubberDuck can access.

If the target is local-only, temporary, inaccessible to the RubberDuck GitHub App, stuck on stale/pending CI state, or returns only kickoff/background-indexing responses, create or use an authorized GitHub mirror and run CI Phase 2 on that mirror.

Local indexing is allowed only after CI semantic full has completed, and only as a post-CI fallback for semantic loading gaps. Label that state `source-confirmed, graph-degraded` or `semantic-load-degraded`; never present it as completed Codebase Intelligence Phase 2.

## Mirror decision gate

Use an authorized GitHub mirror when any of these are true:

- the target is a local path, toy repo, generated QA repo, or unpushed worktree;
- `get_started` or `detailed_repo_analysis` shows missing GitHub App access;
- the upstream repository is private or inaccessible to RubberDuck;
- repeated CI calls remain queued, pending, stale, degraded, unavailable, or tied to the wrong commit;
- the user explicitly requests full CI coverage for a repo that only exists locally.

For private or sensitive code, stop before pushing unless the user has authorized a GitHub mirror destination and visibility.

## Safe mirror procedure

Mirror from a temporary copy, not from a production working tree:

```bash
mkdir -p /tmp/rubberduck-mirror
rsync -a --delete \
  --exclude .git \
  --exclude .rubberduck \
  --exclude node_modules \
  --exclude .venv \
  --exclude venv \
  --exclude __pycache__ \
  --exclude '.*Store' \
  <target>/ /tmp/rubberduck-mirror/
cd /tmp/rubberduck-mirror
git init
git checkout -b main
git add .
git commit -m "Mirror for RubberDuck CI analysis"
gh repo create <owner>/<mirror-repo> --private --source . --remote origin --push
```

Do not use destructive git operations or force-push unless the user explicitly authorized that exact repository rewrite.

Verify the mirror before analysis:

```bash
gh repo view <owner>/<mirror-repo>
git ls-remote origin HEAD
```

Record mirror owner/repo, branch, commit, visibility, GitHub App access status, and whether the source was a toy/temp repo.

## Required CI sequence

Use the GitHub repo key, not a local path, for CI:

```python
get_started(repo="<owner>/<mirror-or-authorized-repo>")

detailed_repo_analysis(
    repo="<owner>/<mirror-or-authorized-repo>",
    branch="<branch>",
    semantic_mode="full",
)
```

Repeat `detailed_repo_analysis(..., semantic_mode="full")` until the complete CI semantic full report is returned. A response that only says started, queued, indexing, pending, stale, degraded, unavailable, refused, or failed is not completion.

Then re-poll Semantic Intelligence and save the instance:

```python
get_started(repo="<owner>/<mirror-or-authorized-repo>")
```

Require `phase1` and `phase2` readiness before graph-dependent semantic calls. If `phase2` is `not_available`, stop or report the blocker instead of claiming full graph coverage.

Load code with the saved `instance_id`:

```python
load_code(
    repo="<owner>/<mirror-or-authorized-repo>",
    instance_id="<instance_id>",
    max_files=2000,
    file_pattern="*.py",
)
```

Repeat per supported language and verify that loaded analyses belong to the mirror repo and current commit.

## Post-CI local fallback boundary

Only after the full CI report exists may you use local source reads, local grep, scratch `load_code(file_path=...)`, or local indexing to fill semantic loading gaps. That fallback cannot replace CI Phase 2 and must be disclosed as degraded evidence.

Never say "RubberDuck full CI completed" unless the completed `detailed_repo_analysis(..., semantic_mode="full")` report exists for the authorized GitHub repo or mirror.
