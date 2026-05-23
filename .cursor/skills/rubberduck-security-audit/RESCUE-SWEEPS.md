# Mandatory Rescue Sweeps

Run all applicable sweeps even when RubberDuck is quiet. Each sweep creates M-ledger candidates.

These sweeps are executed over the deterministic census, not by ad hoc sampling. Run `scripts/build_sink_census.py` first, then use the sections below to triage every matching census row.

## 1. Shell / subprocess construction

Search:

```text
exec(
execSync(
spawn(
spawnSync(
subprocess
Popen
shell=True
os.system
sh -c
child_process
```

Check:

```text
shell-parsed vs argv-array
attacker-controlled command fragments
repo/config/env/CLI/model-output origins
runtime/build/install/deploy reachability
```

## 2. Argv option injection

`argv` arrays block shell metacharacter injection. They do not automatically block option injection.

Inspect calls to:

```text
git
ssh/scp
docker/buildx/podman
pip/uv/conda
tar/unzip
curl/wget
rsync
gpg
kubectl/helm
cloud CLIs
```

For each user-controlled argv element:

```text
can it begin with "-"?
is it before a "--" delimiter?
is it a URL/ref/path/branch/tag/image parsed as options?
does the tool support config/helper/proxy/upload-pack/ext-protocol/hook injection?
```

If no PoC is run and the value can be attacker-controlled and dash-leading, keep the item as an M-ledger open candidate. Do not mark it false positive solely because the subprocess uses an argv array.

## 3. Secret / token comparison

Search:

```text
Authorization
Bearer
SECRET
TOKEN
API_KEY
signature
timingSafeEqual
compare_digest
=== / !== / == / !=
```

Check:

```text
repeated attempts possible?
constant-time comparison?
length normalization?
missing secret fail-closed?
sibling route stronger?
```

## 4. Tenant / batch invariant

Search:

```text
jobs[0]
items[0]
requests[0]
ids[0]
tenantId
organizationId
userId
instanceId
connectionId
jobIds
```

Rule:

```text
Caller-side grouping is not a security boundary.
Privileged callees must reassert tenant/user/instance invariants.
```

## 5. Opaque-ID control plane

Search:

```text
task_id
job_id
run_id
request_id
result_id
status
get_result
retry
cancel
delete
claim
lock
uuid
```

Report table required:

```text
Endpoint | ID source | Entropy | Auth? | Ownership binding? | State-changing? | Leak paths | Status
```

Strong UUIDs reduce exploitability but do not replace authorization.

## 6. Durable sidecar audit

Trace:

```text
write path -> stored representation -> read path -> interpretation point -> privileged behavior
```

Classify:

```text
data only
context-adjacent
system-prompt-adjacent
control input
tool argument
scheduler input
plugin/config input
credential
```

## 7. AI prompt/tool boundary

For tool-capable agents:

```text
Who influences prompt?
Who influences tool results?
Who influences memory/schedules/summaries?
Which tools carry OAuth/cloud/remote-shell credentials?
Which paths run autonomously?
Is provenance marked or hidden?
```

## 8. ML / model-artifact loader

Search:

```text
torch.load
joblib.load
pickle.load
pickle.loads
cloudpickle.load
np.load
allow_pickle=True
from_pretrained
AutoModel
AutoTokenizer
transformers.pipeline
trust_remote_code
safetensors
model store
artifact store
registry
pull
setup_script
custom_objects
pipeline.pkl
protocol.pkl
```

For every hit:

```text
who controls artifact?
trusted-only, tenant-shared, registry-pulled, or user-uploaded?
signature/provenance?
does load execute Python/unpickle/import/run scripts?
dependency version constrained?
weights_only explicit?
trust_remote_code assigned/forced?
```

Negative claims require source proof:

```text
"trust_remote_code is not forced" requires search_code("trust_remote_code") and source reads of every hit.
"weights_only is absent/present" requires search_code("weights_only|torch.load") and dependency-version inspection.
```

## 9. URL-fetch / file-ingestion SSRF

Search:

```text
httpx.get
httpx.AsyncClient
requests.get
aiohttp.ClientSession
urllib.request
client.get(url)
make_safe_connect
ensure_file
UploadFile
FileSchema
multipart_fields
download
fetch
signed_url
presigned
urlopen
```

Report table required:

```text
Source input | Fetch site | Attacker controls URL? | Guard | Redirect/proxy/DNS/IP checks | Status
```

Do not conflate operator-controlled cloud endpoints with user-controlled file URL ingestion.

## 9.5 Route / file-serving traversal

This sweep is mandatory for web apps, CLIs with local dev servers, preview servers, static asset servers, middleware stacks, and browser-facing tools.

Search:

```text
defineEventHandler
createRouter
router.use
loader
action
getRouterParams
params
query
sendFile
serveStatic
fileServerMiddleware
readFile
createReadStream
Access-Control-Allow-Origin
```

Report table required:

```text
Route | Handler | Param source | Path construction | File operation | Containment guard | Exposure/CORS | Status
```

If a decoded route/query/body/header parameter reaches `join`, `resolve`, `readFile`, `writeFile`, `copy`, or static serving, require source proof of containment. A string-prefix `startsWith` guard is insufficient unless a path-separator or relative-path check proves containment.

Do not mark a route safe only because it is a dev route. Localhost plus permissive CORS, tunnel exposure, or browser-reachable development surfaces remain security-relevant.

## 9.6 API-response / file-write traversal

This sweep is mandatory for CLIs, sync tools, package managers, template generators, and deployment tools.

Search:

```text
asset.key
filename
fileName
path
remotePath
key
writeFile
copyFile
rename
ensureDir
download
sync
pull
```

Report table required:

```text
Source | Field | Local path construction | File operation | Guard | Status
```

API-provided paths, archive entry names, package metadata filenames, and remote asset keys are attacker-influenced unless source evidence proves they are constrained by a trusted service invariant or allowlist. Even trusted-service invariants should be recorded as defenses, not silently assumed.

## 10. Archive ingestion: traversal vs DoS

Split analysis:

```text
A. Traversal/symlink/hardlink escape
B. Resource exhaustion: size/count/ratio/nested archive/fd exhaustion
```

Report table required:

```text
Archive source | Extraction site | Traversal guarded? | Symlink/hardlink guarded? | Size/count/ratio bounded? | Status
```

If traversal is guarded but DoS is not, report:

```text
traversal ruled out; archive DoS/hardening remains
```

## 11. ReDoS / regex CPU exhaustion

Search:

```text
re.compile
regex.compile
RegExp(
new RegExp
match(
search(
replace(
user-defined regex
pattern
rules
filters
```

Check:

```text
attacker controls pattern or input?
pattern linting?
timeout?
input length cap?
backtracking-prone structure?
loop over many inputs?
```

## 12. Sibling / variant comparison

Compare:

```text
main vs non-main
entry service vs worker
request path vs response path
public route vs internal route
new SDK vs legacy SDK
dev vs prod
backend A vs backend B
secure sibling vs weak sibling
```
