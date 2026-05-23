# Audit Prompt Compiler

The compiler turns a Repo Intelligence Brief into a repo-specific audit prompt.

## Required behavior

The compiled prompt must include:

```text
repo class
threat model
attacker languages
privilege domains
adapters
selected specialist playbooks
mandatory universal baseline
mandatory census matrices
unsupported-surface routes
expected false-positive clusters
negative-claim requirements
Tier-2 targets
prior-run regression obligations
report gates
```

## Rule: emphasis, not tunnel vision

The compiled prompt may prioritize repo-specific risks, but it must not disable the universal baseline or census closure.

```text
Adaptive prompt = repo-specific emphasis + full census + universal baseline
```

## Template

```text
You are auditing <repo> at <commit>.

Repo Intelligence Brief:
- class:
- supported semantic surface:
- unsupported surfaces:
- entry points:
- attacker languages:
- privilege domains:
- adapters:
- high-risk trust transitions:
- top census clusters:
- untriaged privileged census rows:
- tool-health caveats:

Prioritize:
1. ...
2. ...
3. ...

Run specialist playbooks:
- ...

Run universal baseline sweeps:
- auth/authz
- unsafe deserialization
- subprocess/shell/argv option injection
- SSRF/URL fetch
- file/archive/path traversal and archive DoS
- ReDoS
- SQL/template injection
- credential storage
- tenant/batch invariants
- opaque-ID control planes
- durable sidecars
- unsupported surfaces

Triage deterministic census ledgers:
- file inventory
- sink census
- route/file matrix
- API-response/file matrix
- subprocess matrix
- secrets/logging matrix
- network-fetch matrix
- auth/session matrix
- deserialization/archive matrix
- crypto matrix

Expected false positives to verify carefully:
- ...

Negative claims require:
- search pattern
- scope
- match count
- unsupported surfaces
- caveat

Tier-2 validation targets:
- ...

Prior-run candidates:
- Every prior item must be promoted, merged, ruled out, weakened, open, or invalidated.

Final report must include:
- Repo Intelligence Brief
- compiled audit prompt
- exhaustive census summary
- route/file and API-response/file matrices
- R/H/M/P/F ledgers
- sink census ledgers
- negative-claim ledger
- unsupported-surface table
- root-cause variant table
- claim firewall result
- exhaustive completion check result
- consistency check result
```
