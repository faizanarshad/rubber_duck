# Exception Envelope

Compare thrown/rejected errors.

Fields:

```text
error type/class
message shape
sync throw vs async reject
when error occurs
cleanup before error
caller-visible behavior
```

Output:

```text
Path | BEFORE exception | AFTER exception | Equivalent? | Evidence
```

Do not ignore exception drift unless the preserved contract says exception details are out of scope.
