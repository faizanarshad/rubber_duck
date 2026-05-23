# Unsupported Surface Router

Identify relevant surfaces outside RubberDuck semantic coverage:

```text
shell scripts
YAML workflows
Dockerfile
PowerShell
Terraform/IaC
Markdown instructions
JSON/TOML/INI config
generated/binary files
external repositories/actions
```

For impact analysis, route them by relevance:

```text
change touches build/deploy -> review shell/YAML/Dockerfile
change touches config -> review JSON/YAML/TOML/INI
change touches public API docs -> review docs/markdown
change touches generated artifacts -> mark unsupported or regenerate
```

Output table:

| Surface | Relevance | Review path | Status |
|---|---|---|---|
