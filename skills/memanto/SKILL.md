---
name: memanto
description: Store and retrieve persistent agent memory with the MEMANTO CLI. Use whenever the user states a decision, preference, correction, or commitment worth keeping; whenever you are about to say you lack context on prior work; or when asked what was decided, preferred, or promised earlier. Covers remember, recall, answer, edit/forget, file upload, conflict resolution, expiry policy, and MEMORY.md sync.
allowed-tools: Bash(memanto:*)
license: MIT
---

# MEMANTO — Persistent Memory for AI Agents

MEMANTO is a memory companion agent built on Moorcheh's semantic database. It gives you
long-term memory that survives session restarts: 13 memory types, confidence scoring and
provenance tracking to resist memory poisoning, semantic and temporal recall, and grounded
RAG answers.

**All `memanto` commands are shell commands.** Run them through Bash. Never simulate, describe,
or "pretend to call" them — if you cannot run a shell, say so rather than inventing memory state.

## MANDATORY: check memory before claiming ignorance

Before you say "I don't know", "I don't have context on that", or "we haven't discussed that",
you MUST run one of:

```bash
memanto recall "<topic>" --limit 10
memanto answer "<the user's question>"
```

Claiming ignorance without checking is a failure. The whole point of this skill is that the
answer is probably already stored.

## Session start

```bash
memanto memory sync --project-dir .          # refresh MEMORY.md (the plugin's SessionStart hook does this for you)
memanto recall "instructions decisions goals" --limit 20
memanto answer "What are my pending commitments?"
```

## Choosing between `recall` and `answer`

These are **equal-priority tools**. Do not always default to `recall`.

| Your next step is… | Use |
|---|---|
| *Read these memories and act on them* | `recall` |
| *Deliver this as the answer* | `answer` |
| Building context before a complex multi-step task | `recall` |
| User asks "what did we decide / prefer / commit to?" | `answer` |
| Comparing several matching memories | `recall` |
| One grounded yes/no or summary | `answer` |

## Storing memories

```bash
memanto remember "Chose PostgreSQL over SQLite for production. Needs JSONB and full-text search." \
  --type decision --confidence 0.95 --provenance explicit_statement \
  --source claude_code --tags "database,postgresql,architecture"
```

Search first (`memanto recall`) to avoid duplicates. Always pass `--type`, `--confidence`,
`--provenance`, `--source`, and 2–5 `--tags`.

Batch and conversation extraction:

```bash
memanto remember --batch memories.json                     # array of memory objects
memanto remember --from-conversation transcript.json       # array of {role, content}
memanto remember --from-conversation transcript.json --dry-run   # preview, store nothing
```

### Memory types

| Type | When to Use | Confidence | Example |
|------|-------------|------------|---------|
| `fact` | Verified information, project status | 0.9–1.0 | "API uses PostgreSQL for metadata" |
| `decision` | Architecture choices, approach selections | 0.9–1.0 | "Chose React over Vue for frontend" |
| `instruction` | Standing rules, preferences, guidelines | 0.9–1.0 | "Always use type hints in Python" |
| `commitment` | Promises, TODOs, obligations | 1.0 | "Will deploy monitoring by Friday" |
| `preference` | User/team preferences | 0.8–1.0 | "User prefers dark mode" |
| `goal` | Objectives, targets, milestones | 0.8–1.0 | "Launch CLI by end of March" |
| `artifact` | Tool outputs, reports, file locations | 0.9–1.0 | "Report saved at ./reports/q1.md" |
| `learning` | Knowledge acquired from experience | 0.7–0.9 | "Batch operations 100x faster" |
| `event` | Important conversations, milestones | 0.8–0.95 | "Completed Phase 1 features" |
| `relationship` | Team context, collaboration patterns | 0.85–0.95 | "Alice is lead backend engineer" |
| `observation` | Patterns noticed, behaviors | 0.6–0.85 | "User prefers short responses" |
| `error` | Failures, bugs, lessons learned | 0.95–1.0 | "Namespace format bug — use underscores" |
| `context` | Session summaries, status updates | 0.9–1.0 | "Project 70% done, API complete" |

### Confidence levels

- `1.0` — Explicit user statement, verified fact, standing instruction
- `0.9–0.95` — Strong consensus, well-tested approach
- `0.8–0.85` — Observed pattern (3+ times)
- `0.7–0.75` — Emerging pattern (2 times), reasonable inference
- `0.6–0.65` — Single observation, uncertain
- `< 0.6` — **Do not store.** Too uncertain.

### Provenance

`explicit_statement` · `inferred` · `observed` · `corrected` · `validated` · `imported`

### Source

The tool or agent writing the memory — use `claude_code` here. Up to 64 characters of
letters, digits, `.`, `_`, or `-`; no spaces.

## Retrieving memories

```bash
memanto recall "database architecture" --limit 10
memanto recall "auth" --type decision --min-confidence 0.9 --tags "security"
memanto recall --recent --limit 10                  # newest first, no query
memanto recall --as-of "2026-01-15"                 # what was true then
memanto recall --changed-since "2026-08-01"         # what changed since
memanto recall "deploy" --active                    # exclude expired memories
```

By default recall returns both active and expired memories, each labelled. Narrow with
`--active` or `--expired`.

```bash
memanto answer "What database did we choose and why?"
```

## Correcting and retiring memories

```bash
memanto edit <memory-id> --content "..." --confidence 0.95   # update in place
memanto memory expire <memory-id> --reason superseded        # reversible; stays in recall as [EXPIRED]
memanto memory restore <memory-id>                           # undo an expire
memanto forget <memory-id> --force                           # permanent, non-recoverable
```

Prefer `memory expire` over `forget`. Expiry is reversible and preserves the audit trail.

## Other capabilities

Each has a reference file with full detail:

| Capability | Command | Reference |
|---|---|---|
| Agent & session lifecycle | `memanto agent create/activate/list/delete` | [agent_setup.md](references/agent_setup.md) |
| Session tokens and renewal | `memanto session info` | [session_management.md](references/session_management.md) |
| File ingestion | `memanto upload <file>` | [file_upload.md](references/file_upload.md) |
| MEMORY.md / OKF export | `memanto memory sync`, `memanto memory export` | [memory_sync.md](references/memory_sync.md) |
| Daily digests | `memanto daily-summary`, `memanto schedule enable` | [daily_summary.md](references/daily_summary.md) |
| Conflict resolution | `memanto detect-conflicts`, `memanto conflicts` | [conflicts.md](references/conflicts.md) |
| Expiry policy | `memanto policy show/apply-preset/apply/purge` | [expiry_policy.md](references/expiry_policy.md) |
| Provider migration | `memanto migrate mem0/letta/supermemory/okf` | [migration.md](references/migration.md) |
| Storage guidance | — | [best_practices.md](references/best_practices.md) |
| Type selection detail | — | [memory_types.md](references/memory_types.md) |

## Setup

Requires a free Moorcheh account ([console.moorcheh.ai](https://console.moorcheh.ai)).

```bash
pip install memanto
memanto                          # interactive setup — stores the API key in ~/.memanto/.env
memanto agent create my-project  # creates AND activates the agent
memanto status                   # verify
```

Or set `MOORCHEH_API_KEY` in the environment instead of running the wizard. See
[environment_requirements.md](references/environment_requirements.md).

## Pitfalls

1. **Memory hoarding** — ask "will this matter in a week?" before storing.
2. **Vague content** — "better performance" is useless; "API p99 under 200ms after connection pooling" is not.
3. **No context** — "fixed bug" is useless; "fixed OAuth token expiry bug, commit abc123" is not.
4. **Duplicates** — recall before you remember.
5. **Generic tags** — `important` and `thing` are not findable. Use `oauth`, `commit-abc123`.

## Common errors

| Error | Fix |
|---|---|
| `MEMANTO not configured` | Run `memanto` to set the API key, or export `MOORCHEH_API_KEY` |
| `No active agent` | Run `memanto agent activate <id>` (or `memanto agent list` to find one) |
| Session expired | Sessions auto-renew by default; if it fails, re-run `memanto agent activate <id>` |
