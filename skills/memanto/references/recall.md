# Recall — Search Persistent Memories

The `memanto recall` command performs semantic search across all stored memories for the active agent.

## Basic Usage

```bash
memanto recall "query"
```

## Full Syntax

```bash
memanto recall "query" \
  --limit 10 \
  --type fact \
  --min-confidence 0.8 \
  --as-of "2d ago" \
  --changed-since "1h ago"
```

## Parameters

| Flag | Description | Default |
|------|-------------|---------|
| `query` | Natural language search query | Required |
| `--limit` | Max results to return | 10 |
| `--type` | Filter by memory type | All types |
| `--min-confidence` | Minimum trust score | 0.0 |
| `--as-of` | Show memories as of a point in time | Now |
| `--changed-since` | Only memories changed since a time | None |

## Examples

```bash
# General search
memanto recall "database architecture"

# Search for decisions only
memanto recall "frontend framework" --type decision

# High-confidence facts
memanto recall "API authentication" --type fact --min-confidence 0.9

# Recent changes
memanto recall "deployment" --changed-since "24h ago"

# Historical state (what did we know 2 days ago?)
memanto recall "auth setup" --as-of "2d ago"

# Find all commitments
memanto recall "todo will implement" --type commitment

# Search for errors and lessons
memanto recall "bug fix" --type error

# Multiple concepts (broad search)
memanto recall "instructions decisions goals" --limit 20
```

## Time Format

The `--as-of` and `--changed-since` flags accept natural language:
- `"1h ago"` — 1 hour ago
- `"2d ago"` — 2 days ago
- `"1w ago"` — 1 week ago
- `"2025-03-15"` — specific date

## Session Start Pattern

Always run this at the start of a session to load context:

```bash
memanto recall "instructions decisions goals" --limit 20
memanto recall "commitments todo" --type commitment
```

## Python SDK

```python
from memanto.app.services.memory_read_service import MemoryReadService

async def search_memories(namespace: str, session_token: str):
    svc = MemoryReadService()

    results = await svc.search_memories(
        namespace=namespace,
        query="database architecture decisions",
        memory_type="decision",
        min_confidence=0.8,
        limit=10,
        session_token=session_token,
    )

    for memory in results:
        print(f"[{memory.confidence:.2f}] {memory.title}: {memory.content[:100]}")
```
