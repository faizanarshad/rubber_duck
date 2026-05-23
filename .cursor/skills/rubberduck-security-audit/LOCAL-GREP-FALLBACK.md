# Local Grep and Source Fallback After CI Semantic Full

This fallback is allowed only after `detailed_repo_analysis(..., semantic_mode="full")` has completed. If CI semantic full has not completed, abort the audit session and report the blocker instead of using this fallback. When post-CI semantic loading is incomplete, do not pretend graph coverage exists.

## Trigger conditions

Use this fallback only after completed CI semantic full, and only when:

```text
load_code fails
repo storage is evicted
analysis IDs are stale/wrong
CPG returns impossible zero metrics
language unsupported by RubberDuck
tool output is truncated but saved to file
coverage of critical surface is below target
```

## Recovery ladder

Try in order:

```text
1. get_started(repo) and verify commit/instance_id
2. discover/list loaded analyses with scoped or saved-output parsing
3. load by file_path or subpath
4. load by extension
5. load via local/alternate repo alias if supported
6. load via raw code= parameter for small high-risk files
7. chunk large files with source reads
8. local grep full repo
9. local source reads for targeted functions
10. mark post-CI graph-degraded/source-confirmed coverage
```

## Canonical full-repo grep pack

Run when semantic coverage is partial or broad scan is suspiciously clean:

```text
eval/exec/compile/importlib/getattr/globals
subprocess/Popen/shell=True/os.system
SQL f-string / string concatenation / raw execute
JWT verify=False / signature disabled
pickle/cloudpickle/joblib/torch/np allow_pickle
trust_remote_code / from_pretrained / pipeline
archive extraction / tarfile / zipfile / shutil.unpack
URL fetch / httpx / requests / aiohttp / urllib
regex compile/search/match/fullmatch from untrusted config
YAML unsafe load
Jinja/template rendering
credential file writes
chmod/file mode
plugin loader / dynamic import
sidecar writes then reads
```

Every hit becomes an M-ledger row until source-validated as finding, FP, info, or open.

## Post-CI source claim label

After CI semantic full completion, local source fallback can still produce Tier-1 source evidence, but final claims must be labeled:

```text
source-confirmed, graph-degraded
```

Do not say graph-confirmed.
