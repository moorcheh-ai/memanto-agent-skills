# Migrating Memory Into MEMANTO

Import existing agent memory from another provider. Every migration targets the active agent
unless `--agent` says otherwise, and every one supports `--dry-run`.

**Always dry-run first.** The preview shows how source records map onto MEMANTO's typed schema,
which is where surprises live — flat provider records have to be classified into the 13 types,
and the mapping is worth eyeballing before it is committed.

## Mem0

```bash
memanto migrate mem0 --dry-run
memanto migrate mem0
memanto migrate mem0 --file ./mem0_export.json     # skip the live export
memanto migrate mem0 --agent my-agent --report
```

Needs a Mem0 API key via `--api-key` or `MEM0_API_KEY`; it is saved to `~/.memanto/.env`.
`--report` writes a token/latency/storage savings comparison on a real run.

## Letta

```bash
memanto migrate letta --dry-run
memanto migrate letta --file ./letta_export.json
```

Imports Letta archival passages. Key via `--api-key` or `LETTA_API_KEY`.

## Supermemory

```bash
memanto migrate supermemory --dry-run
memanto migrate supermemory --file ./supermemory_export.json
```

Key via `--api-key` or `SUPERMEMORY_API_KEY`.

## Langfuse

```bash
memanto migrate langfuse --dry-run
```

Syncs Langfuse observability signal into the agent — traces and evaluation results become
`learning` and `error` memories rather than a bulk import of conversation history.

## OKF bundles

[Open Knowledge Format](https://docs.memanto.ai/integrations/okf) is the portable interchange format, so this is
the path for moving between MEMANTO agents or backends without going through a vendor.

```bash
memanto migrate okf ./okf-bundle --dry-run
memanto migrate okf ./okf-bundle --agent my-agent
memanto migrate okf ./notes.md                     # a single markdown file also works
```

Fields that do not map onto MEMANTO's schema are preserved in a `[Supporting data]` footer, and
OKF's free-form `type` is auto-classified into the 13 MEMANTO types.

Export the other direction with:

```bash
memanto memory export --okf --split auto
memanto memory sync --project-dir . --okf
```

## After any migration

Imported memories carry `imported` provenance, which is exactly what you want — it marks them as
lower-trust than something the user stated directly, and conflict detection weights them
accordingly.

Verify and clean up:

```bash
memanto recall --recent --limit 20        # spot-check what landed
memanto detect-conflicts                  # imports often contradict existing memories
memanto conflicts --list
memanto memory sync --project-dir .
```

Bulk imports are the most common source of conflicts, because the provider's history overlaps
with what the agent already learned. Run detection before trusting recall again.
