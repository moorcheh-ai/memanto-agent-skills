# Memory Sync — Export Memories to MEMORY.md

The `memanto memory sync` command exports the agent's full memory to `MEMORY.md` in the project root. This gives agents an always-current snapshot of everything they know without requiring a live API call during context loading.

## Basic Usage

```bash
memanto memory sync --project-dir .
```

## Full Syntax

```bash
memanto memory sync \
  --project-dir /path/to/project \
  --agent my-agent \
  --limit 25
```

## Parameters

| Flag | Description | Default |
|------|-------------|---------|
| `--project-dir` | Directory where MEMORY.md will be written | Current directory |
| `--agent` | Target agent identifier | Active agent |
| `--limit` | Maximum memories per type | 25 |

## What Gets Written

`MEMORY.md` contains a structured snapshot of all memories, grouped by type:

```markdown
# Agent Memory — my-agent
> Last synced: 2025-03-15 14:30:00 UTC

## Instructions
- Always use type hints in Python. No bare except clauses. (confidence: 1.0)

## Decisions
- Chose PostgreSQL 15 for metadata storage. (confidence: 0.95)
- Chose React for frontend. Team has more React experience. (confidence: 0.95)

## Commitments
- Add rate limiting to /api/v1/search before v0.2 release. (confidence: 1.0)

## Goals
- Ship MEMANTO v0.2 with multi-agent support by end of April 2025. (confidence: 0.95)

## Facts
- API runs on Python 3.11 with FastAPI 0.104. Deployed on AWS ECS. (confidence: 0.95)
...
```

## When to Sync

| Trigger | Command |
|---------|---------|
| Session start | `memanto memory sync --project-dir .` |
| After major work | `memanto memory sync --project-dir .` |
| Before committing | `memanto memory sync --project-dir .` |
| After adding many memories | `memanto memory sync --project-dir .` |

## Auto-Sync via Hook (Claude Code)

When connected via `memanto connect claude-code`, a hook runs sync automatically on every session start. No manual action needed.

## MANDATORY: Read MEMORY.md First

After syncing, the agent MUST read `MEMORY.md` before doing any work:

```
Read MEMORY.md in the project root before taking any action.
It contains all instructions, preferences, decisions, and commitments from previous sessions.
You MUST follow any instructions found there.
```

## Git Integration

Consider adding `MEMORY.md` to version control so it's shared with the team. This gives all team members (and agents) visibility into past decisions and context.

Add to `.gitignore` if you want it local only:
```gitignore
MEMORY.md
```

Or commit it as team shared context:
```bash
git add MEMORY.md
git commit -m "chore: update agent memory snapshot"
```
