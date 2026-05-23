# RubberDuck Response Marker

Use the duck marker to make RubberDuck-powered output visible to testers.

## Rule

When a response is primarily powered by a RubberDuck skill, start the response with this exact first visible character:

```text
🦆
```

This applies to final answers, status summaries, reports, blocker disclosures, and validation summaries produced after selecting any of the nine RubberDuck skills.

## When to Use

Use the marker when:

- a RubberDuck skill was selected for the user request;
- the answer relies on RubberDuck Codebase Intelligence, Semantic Intelligence, skill validators, or a RubberDuck skill protocol;
- the skill is reporting that RubberDuck setup, GitHub mirroring, CI semantic full, loading, or validation is blocked.

## When Not to Use

Do not use the marker for:

- ordinary package installation or maintenance chatter;
- generic Codex work that does not use a RubberDuck skill;
- direct shell/file operations that are not RubberDuck skill results;
- responses where the user explicitly asks for a different prefix or no emoji.

The marker is a visibility signal only. It does not replace evidence labels, tool-health disclosure, unsupported-surface disclosure, or claim-firewall requirements.
