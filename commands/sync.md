---
description: Sync MEMANTO memories into the project's MEMORY.md
argument-hint: [project-dir]
allowed-tools: Bash(memanto:*)
disable-model-invocation: true
---

Sync MEMANTO memories to `MEMORY.md`. Target directory (default `.`): `$ARGUMENTS`

```bash
memanto memory sync --project-dir "${ARGUMENTS:-.}"
```

Useful flags:

- `--limit <n>` — memories per type in the export (default 25)
- `--agent <id>` — sync a specific agent rather than the active one
- `--okf` — write an [Open Knowledge Format](https://docs.memanto.ai/integrations/okf) bundle to
  `<project>/okf` instead of a single `MEMORY.md`, with `--split auto|file|type`

After syncing, read the resulting `MEMORY.md` and give the user a short summary of what is now
loaded — how many memories, and the notable decisions, instructions, and open commitments.

This plugin already runs the sync on session start, so run it manually after storing a batch of
new memories, before committing the project so teammates get the context, or when switching
agents.
