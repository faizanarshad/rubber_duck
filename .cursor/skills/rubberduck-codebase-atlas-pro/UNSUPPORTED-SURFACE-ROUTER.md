# Unsupported Surface Router

Do not imply full coverage when files exist outside RubberDuck's semantic surface.

Mirror unsupported-surface evidence in `evidence/unsupported-surfaces.md` for DEEP mode and reference it from falsification recipes and the evidence manifest.

## Required table

```markdown
| Surface | Count/examples | Privilege | Coverage status | Review path | Included in claims? |
|---|---:|---|---|---|---|
```

## Surfaces to check

```text
shell scripts
GitHub/GitLab CI YAML
Dockerfile / container build files
PowerShell
Terraform / Helm / Kubernetes YAML
Markdown agent instructions
JSON/TOML/YAML config
binary/generated/vendor files
external repos/actions
```

## Claim caveat

Every final report must say:

```text
Claims are limited to the analyzed RubberDuck semantic/codebase surface unless unsupported surfaces are explicitly reviewed.
```

## Review routing

Examples:

```text
shell -> shell/argv/script review
YAML workflow -> CI/CD permissions/secrets review
Dockerfile -> build/runtime/container review
Markdown agent rules -> prompt-adjacent sidecar review
Terraform/K8s -> cloud/IaC review
```
