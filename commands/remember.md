# /memanto:remember

Store a persistent memory for the active agent.

## Syntax

```
/memanto:remember content "<text>" type <type> [confidence <0.0-1.0>] [provenance <type>] [tags "<tag1,tag2>"]
```

## Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `content` | The memory text | Yes |
| `type` | Memory type | Yes |
| `confidence` | Trust score 0.0–1.0 | Recommended |
| `provenance` | Source classification | Recommended |
| `source` | Agent/tool name | Recommended |
| `tags` | Comma-separated tags | Recommended |

## Memory Types

`fact` · `decision` · `preference` · `instruction` · `goal` · `commitment` · `artifact` · `learning` · `event` · `relationship` · `observation` · `error` · `context`

## Examples

```bash
# Store a decision
memanto remember "Chose PostgreSQL over SQLite for production. Reason: need JSONB and FTS." \
  --type decision --confidence 0.95 --provenance explicit_statement --source claude_code \
  --tags "database,postgresql,architecture"

# Store a user preference
memanto remember "User prefers tabs over spaces in all languages." \
  --type preference --confidence 1.0 --provenance explicit_statement --source claude_code \
  --tags "formatting,style,tabs"

# Store a commitment
memanto remember "Will implement rate limiting before v0.2 release." \
  --type commitment --confidence 1.0 --provenance explicit_statement --source claude_code \
  --tags "rate-limiting,todo,v0.2"
```

## Rules

- Confidence < 0.6 → don't store (too uncertain)
- Always include `--type`, `--confidence`, `--provenance`, `--source`
- Always include 2–5 `--tags`
- Search first with `memanto recall` to avoid duplicates
