# Claim Firewall

Before final output, inspect each important claim.

Block or caveat claims that exceed evidence.

## Atlas framing

Every report must state:

```text
This is a Codebase Atlas, not a vulnerability report.
Security-sensitive flows may be mentioned as architecture boundaries, but findings are not security-validated unless explicitly labeled.
```

Include an Atlas coverage statement:

```text
semantic surface covered
codebase-intelligence surface covered
unsupported surfaces
runtime/deployment not proven unless tool evidence says so
```

Do not present architecture boundary notes as security findings. If a security-sensitive flow is mentioned, label it architecture-only unless a separate security validation was explicitly performed.

## Allowed claim types

```text
source-confirmed
symbols-confirmed
call-chain-confirmed
data-flow-confirmed
search-confirmed
codebase-metric-confirmed
metadata-confirmed
manual inference with caveat
unsupported / out of scope
```

## Blocked patterns

Do not say:

```text
"the main flow is..."
"all major classes are..."
"no X exists..."
"complete coverage..."
"this function is unused..."
"this is the architecture..."
```

unless supported by relevant evidence and scope.

## Claim ledger checker

A final report should contain or reference a claim/evidence table. If absent, explicitly state why.

## Falsifiability gate

Every major claim must either include or link to a falsification recipe:

```text
To refute this claim/flow, rerun:
- <exact tool call>
- <search pattern>
- <source file / function>
Expected contradiction:
- <what output would invalidate the claim>
```

If the recipe cannot be written, downgrade the claim to manual inference, unsupported, or out of scope.

## Evidence-pack contradiction gate

Before finalizing a bundle, block contradictions:

```text
REPORT.md says evidence files are absent while evidence/ exists
REPORT.md says atlas-summary.json is absent while evidence/atlas-summary.json exists
REPORT.md implies raw transcripts exist while only normalized/report-derived evidence exists
§1 implies full symbol inventory while symbols-overview evidence is curated or derived only
```
