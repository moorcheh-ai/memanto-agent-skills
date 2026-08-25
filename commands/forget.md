---
description: Correct, expire, or delete a MEMANTO memory
argument-hint: <memory-id or description of what is wrong>
allowed-tools: Bash(memanto:*)
disable-model-invocation: true
---

Fix or retire a memory. Target: `$ARGUMENTS`

**1 — Find it.** If that is not already a memory id, locate it:

```bash
memanto recall "$ARGUMENTS" --limit 10
```

Show the user the candidates and confirm which one before touching anything.

**2 — Pick the right operation.** These are not interchangeable:

| Situation | Command |
|---|---|
| Content is wrong or incomplete, memory still applies | `memanto edit <id> --content "..." --confidence 0.95` |
| No longer true, but the history matters | `memanto memory expire <id> --reason "<why>"` |
| Stored by mistake, never should have existed | `memanto forget <id> --force` |
| Expired something you should not have | `memanto memory restore <id>` |

**Default to `memory expire`.** It is reversible, keeps the audit trail, and the memory still
surfaces in recall labelled `[EXPIRED]`. `forget` is permanent and non-recoverable — only use it
when the user explicitly wants the memory gone, and confirm before you run it.

**3 — When the user is correcting you**, expire the wrong memory *and* store the correction, so
the reason is preserved:

```bash
memanto memory expire <old-id> --reason "corrected-by-user"
memanto remember "<the corrected fact>" --type learning --confidence 1.0 \
  --provenance corrected --source claude_code --tags "correction,<topic>"
```

Report what you changed and which memory ids it affected.
