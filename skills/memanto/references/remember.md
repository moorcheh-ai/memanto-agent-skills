# Remember — Store Persistent Memories

The `memanto remember` command stores a memory in the agent's persistent namespace.

## Basic Usage

```bash
memanto remember "content" --type TYPE --confidence 0.9 --provenance PROVENANCE --source AGENT_NAME
```

All flags are required for best results. Never let them default.

## Full Syntax

```bash
memanto remember "content" \
  --type fact \
  --confidence 0.95 \
  --provenance explicit_statement \
  --source claude_code \
  --tags "tag1,tag2,tag3" \
  --title "Optional short title"
```

## Parameters

| Flag | Description | Required |
|------|-------------|----------|
| `content` | The memory text (positional) | Yes |
| `--type` | Memory type (see table below) | Yes |
| `--confidence` | Trust score 0.0–1.0 | Yes |
| `--provenance` | Source of the memory | Yes |
| `--source` | Agent/tool creating this memory | Yes |
| `--tags` | Comma-separated tags for retrieval | Recommended |
| `--title` | Short title (auto-generated if omitted) | No |

## Memory Types

| Type | Confidence | When to Use |
|------|------------|-------------|
| `fact` | 0.9–1.0 | Verified information about the project or codebase |
| `decision` | 0.9–1.0 | Architecture choices, approach selections |
| `instruction` | 0.9–1.0 | Standing rules ("always use type hints") |
| `commitment` | 1.0 | Promises, TODOs, obligations |
| `preference` | 0.8–1.0 | User or team preferences |
| `goal` | 0.8–1.0 | Objectives, milestones, targets |
| `artifact` | 0.9–1.0 | Tool outputs, file locations, reports |
| `learning` | 0.7–0.9 | Knowledge from experience or debugging |
| `event` | 0.8–0.95 | Important conversations or milestones |
| `relationship` | 0.85–0.95 | Team context, collaboration patterns |
| `observation` | 0.6–0.85 | Patterns noticed, behaviors |
| `error` | 0.95–1.0 | Failures, bugs, lessons learned |
| `context` | 0.9–1.0 | Session summaries, status snapshots |

## Provenance Types

| Value | When to Use |
|-------|-------------|
| `explicit_statement` | User directly stated this |
| `inferred` | Derived from context or behavior |
| `observed` | Witnessed in action |
| `corrected` | Updated after a contradiction |
| `validated` | Confirmed/verified by evidence |

## Tagging Best Practices

- Use 2–5 tags per memory
- Lowercase with hyphens: `bug-fix` not `BugFix`
- Be specific: `oauth-expiry` not `auth`
- Include references: `commit-abc123`, `pr-42`, `issue-15`

```bash
# Good tags
--tags "authentication,oauth,session-tokens"
--tags "performance,batch-ops,commit-3f39351"
--tags "correction,testing,user-preference"

# Bad tags
--tags "important"      # too generic
--tags "stuff"          # not descriptive
```

## Examples

```bash
# Store a fact
memanto remember "API uses PostgreSQL 15 for metadata storage. Migrations managed with Alembic." \
  --type fact \
  --confidence 0.95 \
  --provenance explicit_statement \
  --source claude_code \
  --tags "database,postgresql,alembic"

# Store a decision
memanto remember "Chose React over Vue because the team has more React experience. Decision made 2025-03-15." \
  --type decision \
  --confidence 0.95 \
  --provenance explicit_statement \
  --source claude_code \
  --tags "frontend,react,architecture"

# Store a user preference
memanto remember "User prefers tabs over spaces for indentation in all languages." \
  --type preference \
  --confidence 1.0 \
  --provenance explicit_statement \
  --source claude_code \
  --tags "formatting,indentation,style"

# Store a commitment
memanto remember "Will implement rate limiting on the /api/v1/search endpoint before next release." \
  --type commitment \
  --confidence 1.0 \
  --provenance explicit_statement \
  --source claude_code \
  --tags "rate-limiting,api,todo"

# Store a lesson learned from an error
memanto remember "Namespace names must use underscores, not hyphens. Using hyphens causes ConflictError on creation." \
  --type error \
  --confidence 1.0 \
  --provenance observed \
  --source claude_code \
  --tags "namespace,bug-fix,moorcheh"

# Store a learning
memanto remember "Batch storing 100 memories at once is ~100x faster than storing individually. Use batch_store_memories() for bulk ops." \
  --type learning \
  --confidence 0.9 \
  --provenance observed \
  --source claude_code \
  --tags "performance,batch,optimization"
```

## Pitfalls to Avoid

1. **Memory hoarding** — Ask "Will this matter next week?" before storing
2. **Vague content** — Bad: "better performance" → Good: "API response < 200ms after caching"
3. **No context** — Bad: "fixed bug" → Good: "Fixed OAuth token expiry bug in auth.py:145. Commit abc123."
4. **Duplicates** — Always run `memanto recall` first to check if similar memory exists
5. **Missing tags** — Always include tags; they're the primary retrieval mechanism
6. **Wrong confidence** — Don't use 0.9 for a single observation; use 0.65–0.75

## Python SDK (REST API)

```python
import httpx
import asyncio

async def store_memory(agent_id: str, session_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:8000/api/v2/agents/{agent_id}/remember",
            json={
                "type": "decision",
                "content": "Chose PostgreSQL over SQLite for production workloads.",
                "confidence": 0.95,
                "provenance": "explicit_statement",
                "source": "my_agent",
                "tags": ["database", "postgresql", "architecture"]
            },
            headers={
                "X-Session-Token": session_token,
            }
        )
        result = response.json()
        print(f"Stored Memory ID: {result.get('memory_id')}")
```
