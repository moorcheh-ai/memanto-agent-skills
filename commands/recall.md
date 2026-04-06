# /memanto:recall

Search persistent memories using semantic similarity.

## Syntax

```
/memanto:recall query "<text>" [type <type>] [limit <n>] [min_confidence <0.0-1.0>]
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `query` | Natural language search | Required |
| `type` | Filter by memory type | All types |
| `limit` | Max results | 10 |
| `min_confidence` | Minimum trust score | 0.0 |

## Examples

```bash
# General search
memanto recall "database architecture"

# Search decisions only
memanto recall "frontend framework" --type decision

# High-confidence facts
memanto recall "authentication" --type fact --min-confidence 0.9

# Load session context
memanto recall "instructions decisions goals" --limit 20

# Find commitments
memanto recall "todo pending" --type commitment
```

## Session Start Pattern

Always run this at the beginning of each session:

```bash
memanto recall "instructions decisions goals" --limit 20
memanto answer "What are my pending commitments?"
```
