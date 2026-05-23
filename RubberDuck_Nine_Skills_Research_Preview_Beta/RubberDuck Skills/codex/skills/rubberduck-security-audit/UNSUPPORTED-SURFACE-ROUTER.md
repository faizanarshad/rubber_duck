# Unsupported Surface Router

Do not imply a full repo is covered when semantic tools only cover some languages.

## Required table

```text
Surface | Count | Privilege | Review path | Status
```

## Routing

```text
Shell scripts -> shell/argv/CI scanner
GitHub Actions / CI YAML -> workflow permission and untrusted input review
Dockerfile / Containerfile -> build-time secrets, root/user, curl pipes, package install
PowerShell -> command/credential review
Terraform / Helm / Kubernetes -> IaC/cloud permission review
Markdown agent instructions -> prompt-adjacent sidecar audit
JSON/TOML/YAML configs -> config-to-action and secret/default review
Lockfiles -> supply-chain/dependency audit
```

## Claim rule

Do not say:

```text
100% coverage
```

unless every file type has a route and status.

Say instead:

```text
Semantic coverage complete for Python/TypeScript.
Shell/YAML/Dockerfile were routed to specialized review.
External action repositories are out of scope unless separately audited.
```
