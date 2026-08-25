# Cookbook: Conflict Resolution

Keep agent memory internally consistent. Over a long project, memory contradicts itself — a
decision is reversed, a preference changes, a fact is corrected. Both versions sit in the
namespace, recall surfaces them together, and RAG answers start hedging or picking the stale
one. This cookbook wires detection and resolution into a routine.

## Prerequisites

[Persistent Agent Memory](persistent_agent_memory.md) set up, with an active agent.

## The problem

```bash
memanto recall "database" --limit 5
```

```
[1] (decision) [0.95] Chose PostgreSQL for metadata storage
[2] (decision) [0.90] Migrated metadata storage to DynamoDB for scale
```

Both are true statements about different points in time, and neither says so. `memanto answer
"what database do we use?"` now has to guess.

## Step 1 — Detect

```bash
memanto detect-conflicts
memanto detect-conflicts --date 2026-08-20 --agent my-project
```

An LLM pass over the day's session memories writes a JSON report to `~/.memanto/conflicts/`.
Defaults to today and the active agent.

## Step 2 — Review

```bash
memanto conflicts --list
```

Lists what was found without entering the resolver. Good for a quick check, and the only mode
that is safe to run from an agent tool call.

## Step 3 — Resolve

```bash
memanto conflicts
```

Walks each unresolved conflict interactively. **Needs a real terminal** — from Claude Code, run
it yourself with `! memanto conflicts`.

Non-interactively, when you already know the winner:

```bash
memanto memory expire <losing-id> --reason "conflicts-with-<winning-id>"
```

## Picking a winner

| Signal | Prefer |
|---|---|
| Recency | The newer memory, for decisions and status |
| Provenance | `explicit_statement` / `corrected` over `inferred` / `observed` |
| Confidence | The higher score, when recency and provenance tie |
| Specificity | The more specific memory |

Recency does not automatically win. A standing `instruction` from the user outranks a later
`observation` that contradicts it — that observation is evidence the rule was *broken*, not that
it was withdrawn.

## Step 4 — Automate detection

```bash
memanto schedule enable
memanto schedule status
```

The nightly job runs daily summary, conflict detection, and the expiry sweep together. Detection
is automated; **resolution stays manual by design**, because choosing a winner is a judgment
call that silently guessing would get wrong.

## Preventing conflicts

Cheaper than resolving them:

1. **Recall before remember.** Update with `memanto edit <id>` rather than storing a second
   version.
2. **Expire on change.** When something stops being true, expire it in the same breath as
   storing the replacement:
   ```bash
   memanto memory expire <old-id> --reason "superseded"
   memanto remember "Migrated metadata storage to DynamoDB. PostgreSQL retired 2026-08-20." \
     --type decision --confidence 0.95 --provenance explicit_statement \
     --source claude_code --tags "database,dynamodb,migration"
   ```
3. **Mark corrections.** Use `--provenance corrected` so detection can weight it properly.
4. **Detect after bulk imports.** Migrations and file uploads are the biggest conflict source —
   see [migration.md](migration.md).

## Verify

```bash
memanto conflicts --list          # should be empty
memanto answer "What database do we use and why?"
memanto memory sync --project-dir .
```

The answer should now name one database and explain the switch, rather than presenting both.
