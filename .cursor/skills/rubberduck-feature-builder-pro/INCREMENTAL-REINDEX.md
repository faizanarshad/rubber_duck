# Incremental Re-index

After every changed file, prefer repo-relative path loading:

```python
load_code(repo="<owner/repo or authorized mirror>", file_path="<changed-file>", force=true)
```

Use the same authorized GitHub repo or mirror established by `RUBBERDUCK-CI-BOOTSTRAP.md`. If unavailable after CI semantic full has completed, fallback to basename pattern and record collision risk.
