# Cookbook: Migrating from Another Provider

Move existing agent memory into MEMANTO from Mem0, Letta, Supermemory, Langfuse, or an OKF
bundle — without losing the history you already accumulated.

## Prerequisites

[Persistent Agent Memory](persistent_agent_memory.md) set up, with a target agent created. The
migration writes into the **active** agent unless `--agent` says otherwise, so confirm which one
that is before you start:

```bash
memanto session info
```

## The shape of the problem

Most providers store flat records — a string, maybe a timestamp and a user id. MEMANTO stores
typed memories with confidence and provenance. Migration therefore **classifies**: every source
record is mapped onto one of the 13 types and given a confidence score.

That mapping is where surprises live, which is why every migration command supports `--dry-run`
and you should always use it first.

## Step 1 — Dry run

```bash
memanto migrate mem0 --dry-run
memanto migrate letta --dry-run
memanto migrate supermemory --dry-run
memanto migrate okf ./okf-bundle --dry-run
```

Credentials come from `--api-key` or the provider's env var (`MEM0_API_KEY`, `LETTA_API_KEY`,
`SUPERMEMORY_API_KEY`) and are saved to `~/.memanto/.env`. To work from an export you already
have rather than pulling live, pass `--file ./export.json`.

Read the preview and check: are decisions landing as `decision` rather than `fact`? Are
preferences being flattened into `observation`? If the mapping looks wrong, migrate a subset
first via an export file you have trimmed.

## Step 2 — Import

```bash
memanto migrate mem0
memanto migrate mem0 --agent my-project --report
```

`--report` also writes a token/latency/storage comparison against the source provider — useful
if you need to justify the switch. Not available for OKF imports.

## Step 3 — Verify

```bash
memanto recall --recent --limit 20
memanto status
```

Spot-check that content survived intact and types look sane. Everything imported carries
`imported` provenance, which is deliberate: it marks these memories as lower-trust than
something the user stated to you directly, and conflict detection weights them accordingly.

## Step 4 — Reconcile

**This is the step people skip.** A bulk import overlaps with what the agent already learned, so
imports are the single largest source of contradictory memory:

```bash
memanto detect-conflicts
memanto conflicts --list
```

Resolve before trusting recall again — see [Conflict Resolution](conflict_resolution.md).

## Step 5 — Sync

```bash
memanto memory sync --project-dir .
```

## Langfuse

Different in kind from the others. It syncs observability signal — traces and eval results —
rather than conversation history, landing as `learning` and `error` memories:

```bash
memanto migrate langfuse --dry-run
```

Use it to teach an agent from its own production failures, not to seed it with prior knowledge.

## OKF: the portable path

[Open Knowledge Format](https://docs.memanto.ai/integrations/okf) is the vendor-neutral interchange format, and
the right route for moving between MEMANTO agents or backends:

```bash
# Export from one agent
memanto memory export --okf --split type -o ./okf-bundle

# Import into another
memanto migrate okf ./okf-bundle --agent other-project --dry-run
memanto migrate okf ./okf-bundle --agent other-project
```

Fields with no MEMANTO equivalent are preserved in a `[Supporting data]` footer rather than
dropped, and OKF's free-form `type` is auto-classified. A single `.md` file works as well as a
bundle directory.

## Migrating incrementally

For a large namespace, do not move everything at once:

1. Export from the provider to a file.
2. Split it into batches.
3. Dry-run, import, and reconcile one batch at a time.

The reconcile step is what makes this worth the extra effort — conflicts are far easier to judge
in batches of fifty than in a single import of five thousand.
