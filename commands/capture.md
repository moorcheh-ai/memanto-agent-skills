---
description: Review this session and store what is worth remembering
allowed-tools: Bash(memanto:*)
disable-model-invocation: true
---

Review this conversation and commit the durable parts to MEMANTO. Optional focus: `$ARGUMENTS`

**1 — Extract candidates.** Go back over the session and pull out what will still matter in a
week:

- Decisions made, **with the reasoning** — `decision`
- Standing rules or conventions the user stated — `instruction`
- Preferences they expressed — `preference`
- Things you or the user committed to doing — `commitment`
- Corrections the user made to you — `learning`, provenance `corrected`
- Bugs hit and how they were resolved — `error`
- Non-obvious things you learned about this codebase — `learning`

Skip anything transient: file contents, command output, intermediate reasoning, and anything
already recorded in the repo or git history.

**2 — Check for duplicates.** Recall each candidate's topic before storing. If it already exists,
`memanto edit <id>` it rather than adding a near-duplicate.

**3 — Show the user the list first.** Content, type, and confidence for each. Let them cut items
before anything is written. Drop anything you would score below 0.6.

**4 — Store what survives**, one call per memory, each self-contained:

```bash
memanto remember "<content>" --type <type> --confidence <n> \
  --provenance <provenance> --source claude_code --tags "<2-5 tags>"
```

For several at once, write a JSON array and use `memanto remember --batch <file>.json`.

**5 — Sync** so the project picks it up:

```bash
memanto memory sync --project-dir .
```

---

To extract from an **external** transcript instead of this session, MEMANTO can do the
extraction itself — the file must be a JSON array of `{role, content}` objects:

```bash
memanto remember --from-conversation transcript.json --dry-run   # preview first
memanto remember --from-conversation transcript.json
```
