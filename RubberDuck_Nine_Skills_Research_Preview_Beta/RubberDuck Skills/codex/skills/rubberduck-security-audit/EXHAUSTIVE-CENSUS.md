# Exhaustive Census Default

Security audits default to client-grade exhaustive coverage. This is not an optional mode.

The agent may prioritize validation order, but it may not skip census generation or finalize with untriaged privileged rows.

## Required Command

After CI semantic full completes and a local checkout is available, run:

```bash
python <installed_skill_dir>/scripts/build_sink_census.py \
  --root <repo_root> \
  --out <report_bundle_dir>
```

`<installed_skill_dir>` means the copied `rubberduck-security-audit` skill folder for the current platform.


This creates or updates the census ledgers under `<report_bundle_dir>/ledgers`.

## Required Ledgers

```text
ledgers/file-inventory.md
ledgers/sink-census.md
ledgers/route-file-census.md
ledgers/api-response-file-census.md
ledgers/subprocess-census.md
ledgers/secrets-logging-census.md
ledgers/network-fetch-census.md
ledgers/auth-session-census.md
ledgers/deserialization-archive-census.md
ledgers/crypto-census.md
```

If a repo has no rows for a matrix, keep the ledger with an explicit empty-state line. Do not delete the file.

## Disposition Values

Each census row starts as `untriaged`. Before final reporting, replace it with exactly one of:

```text
promoted
false-positive
hardening
expected-behavior
fixed
out-of-scope
blocked
```

Every row also needs an evidence pointer before final closeout. Evidence can be a RubberDuck graph call, a source snippet, a local command output, a prior-report link, or a documented blocker.

## Privileged Rows

Rows are privileged by default when they involve any of:

```text
route or middleware
file read/write/delete/copy/rename
path construction for file operations
subprocess/shell/tool invocation
network fetch/download/upload
secret/token/key/password/auth material
auth/session/identity/tenant state
deserialization/archive extraction
crypto/key/signature/randomness
config-to-action behavior
API-response-controlled local path or command input
```

Untriaged privileged rows block a complete report.

## Route/File Matrix

For each route, middleware, handler, loader, action, or router registration that can reach file IO:

```text
Route | Handler | Param source | Path construction | File operation | Containment guard | Exposure/CORS | Disposition | Evidence
```

Required validation:

```text
read route registration
read handler body
trace route/query/body/header param into path construction
identify read/write/delete/copy sink
prove containment guard exists or record it missing
check exposure: localhost, tunnel, CORS, authenticated, unauthenticated
```

Do not downgrade merely because a route is "dev only" if it is reachable from a browser, localhost, tunnel, or permissive CORS surface.

## API-Response/File Matrix

For each API or external data field that can become a local path:

```text
Source | Field | Local path construction | File operation | Guard | Disposition | Evidence
```

Examples:

```text
remote API asset key -> join(root, key) -> writeFile
package metadata filename -> join(cache, filename) -> writeFile
download archive entry name -> extract/write target
```

Do not mark false positive unless source evidence shows the field is constrained, normalized, allowlisted, or contained before the file operation.

## Subprocess Matrix

For each subprocess/tool invocation:

```text
File | Line | Command | Argument source | Shell? | Option injection possible? | Privilege | Disposition | Evidence
```

Argv arrays block shell metacharacter injection but do not automatically block option injection. Check dash-leading values, `--` delimiters, tool-specific config/helper/proxy hooks, and whether arguments are attacker-controlled.

## Secrets/Logging Matrix

For each secret/token/key/password source and log/storage/network sink:

```text
File | Line | Secret source | Sink | Masking/guard | Runtime context | Disposition | Evidence
```

Secret masking in CI is defense-in-depth, not permission to print the secret.

## Prior Findings

If prior findings are provided, parse them before final triage. Every prior finding gets a row in `ledgers/p-ledger.md` with one current status:

```text
still-present
fixed
not-in-current-scope
disproven
merged-into-new-finding
blocked
```

No prior High/Critical finding may disappear silently. If it is downgraded, write a dedicated downgrade note.

## Final Gate

Run:

```bash
python <installed_skill_dir>/scripts/check_exhaustive_completion.py \
  --root <report_bundle_dir>
```

This checker must pass before the report can be called complete. If it fails and the remaining rows cannot be completed in-session, mark the report incomplete and list the exact unresolved rows.
