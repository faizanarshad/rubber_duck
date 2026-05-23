# Worktree Safety

Before writing:

```bash
git rev-parse --show-toplevel
git rev-parse HEAD
git status --short
git branch --show-current
```

Halt if not a git repo. Halt if HEAD differs from sealed_plan.base_commit unless explicit override exists. Halt on dirty tree unless allowed by SIGNOFF or AUTO_AUTHORIZATION.

Before commit or push, inspect dirty files and stage only the intended feature files. Preserve unrelated user changes. Never stage `.env`, `.env.local`, local databases, caches, browser artifacts, cookies, API keys, or screenshots that may contain secrets. Never use `git reset --hard` or destructive checkout.
