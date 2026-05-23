# Impact Prompt Compiler

Generate a repo/target-specific execution prompt after target resolution.

## Inputs

```text
Repo Intelligence Brief
Target Resolution
Change Type
Tool Health
Initial RubberDuck signals
Prior reports/context if available
```

## Compiled prompt must include

```text
target and proposed change
change type playbook
expected risky dimensions
mandatory tools
evidence requirements
dual-source adjudication requirement
output contract
anti-claims
runtime optimization requirement
```

## Example shape

```text
You are analyzing impact of changing <target> in <file>.

This target appears to be:
- public/internal/test-only: <classification>
- call profile: <callers/callees summary>
- state profile: <module/shared variables>
- test/mocking profile: <mock patterns>
- change type: <rename/signature/behavior/...>

Prioritize:
- direct callers
- call shapes
- shared state
- comments/contracts
- mocks
- public exports
- tests
- runtime-equivalent optimization opportunities

Do not claim LOW risk until search_code, call_chain, and source reads agree.
```
