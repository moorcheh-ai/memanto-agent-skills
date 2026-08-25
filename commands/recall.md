---
description: Search MEMANTO memories by meaning, type, or time
argument-hint: <query> [--type X] [--recent] [--as-of DATE]
allowed-tools: Bash(memanto:*)
disable-model-invocation: true
---

Search MEMANTO persistent memory for:

$ARGUMENTS

Pick the right mode:

```bash
# Semantic search — the default
memanto recall "$ARGUMENTS" --limit 10

# Narrow by type, confidence, or tags when the request implies it
memanto recall "<query>" --type decision --min-confidence 0.9 --tags "security"

# Temporal modes — these take NO query
memanto recall --recent --limit 10            # newest first
memanto recall --as-of "2026-01-15"           # what was true at that date
memanto recall --changed-since "2026-08-01"   # what changed since then
```

Recall returns active and expired memories together, each labelled. Add `--active` to exclude
expired ones, `--expired` to see only those.

If the user asked a **question** rather than for a list of memories, use `/memanto:answer`
instead — it synthesizes a single grounded response rather than returning chunks.

After running, summarize what you found and flag anything that contradicts something else in
the results. If nothing comes back, say so plainly and suggest a broader query — do not
silently conclude the topic was never discussed.
