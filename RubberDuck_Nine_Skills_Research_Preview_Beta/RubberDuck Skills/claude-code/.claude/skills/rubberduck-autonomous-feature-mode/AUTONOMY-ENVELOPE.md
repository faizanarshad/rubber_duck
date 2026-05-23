# Autonomy Envelope

Required fields:

```text
repo
base_commit
feature_description
tier
max_iterations
max_files_touched
max_new_dependencies
allowed_file_globs
off_limits_file_globs
require_final_user_review
```

The envelope is the authority boundary. If an action exceeds it, halt.
