# /memanto:sync

Sync agent memories to `MEMORY.md` in the project root.

## Syntax

```
/memanto:sync [project_dir <path>]
```

## Examples

```bash
# Sync to current directory
memanto memory sync --project-dir .

# Sync to specific project
memanto memory sync --project-dir /path/to/project
```

## What This Does

Exports all agent memories to `MEMORY.md` as a structured markdown file. The agent should read this file at the start of every session to load full context.

## When to Run

- At the start of each session (auto-runs if connected via `memanto connect`)
- After adding many new memories
- Before committing the project (to share context with teammates)
- Before switching agents or projects

## MEMORY.md Structure

```markdown
# Agent Memory — my-agent
> Last synced: 2025-03-15 14:30 UTC

## Instructions
- Always use type hints in Python (confidence: 1.0)

## Decisions
- Chose PostgreSQL for metadata storage (confidence: 0.95)

## Commitments
- Add rate limiting before v0.2 release (confidence: 1.0)
...
```
