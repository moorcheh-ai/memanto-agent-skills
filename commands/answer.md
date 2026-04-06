# /memanto:answer

Generate a RAG-powered answer grounded in persistent agent memory.

## Syntax

```
/memanto:answer question "<question>" [type <type>]
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `question` | The question to answer | Required |
| `type` | Filter context to this memory type | All types |

## Examples

```bash
# General question
memanto answer "What database did we choose and why?"

# Ask about commitments
memanto answer "What are my pending commitments?"

# Ask about decisions
memanto answer "What frontend framework did we decide on?"

# Ask about preferences
memanto answer "What coding conventions does the user prefer?"

# Ask about errors encountered
memanto answer "What bugs have we had with the auth system?"
```

## MANDATORY Rule

Before saying "I don't know" or "I don't have context on that", ALWAYS run:

```bash
memanto recall "topic of the question"
memanto answer "What did we decide about X?"
```

These must be run first. Never claim ignorance without checking memory.
