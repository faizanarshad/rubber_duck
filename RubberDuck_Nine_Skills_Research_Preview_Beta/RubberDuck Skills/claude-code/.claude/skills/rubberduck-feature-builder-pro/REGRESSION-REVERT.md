# Regression Revert

If a previously GREEN dimension becomes YELLOW/RED/BLOCKED after a write:

```text
revert the write
log reason
retry max 2 times
halt on third regression
```
