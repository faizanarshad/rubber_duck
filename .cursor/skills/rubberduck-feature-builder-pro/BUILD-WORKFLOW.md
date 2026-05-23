# Build Workflow

Follow the phases in SKILL.md. Never skip B0/B1/B2/B3. Never emit PR_READY.diff unless completion gates pass.

After B14, run B14.5 GitHub Publish/Re-index Gate when repo-backed RubberDuck validation is required or when local-only files cannot be read by RubberDuck CI. Do not call the result fully RubberDuck-validated unless the pushed branch or commit was indexed and validated. If GitHub validation is declined or unavailable, finish as `Validation status: LOCAL_BUILD_COMPLETE_RUBBERDUCK_PENDING`.

After B14.5, run B14.6 Security Delta Gate when the build is GitHub-validated, autonomous, security-sensitive, or the user asks for PR security validation. Compare RubberDuck base vs PR head findings. Auto-fix only true-positive new Critical/High findings in changed or new code, adjudicate false positives with evidence, and keep pre-existing repo findings separate.

At each iteration:

```text
read HEARTBEAT.json
select smallest RED/YELLOW dimension
propose smallest change
cheap prevalidate
apply one-file patch
re-index changed file
refresh heartbeat
revert if regression
log AUDIT.json
```
