# Answer — RAG-Powered Answers from Memory

The `memanto answer` command retrieves relevant memories and synthesizes a grounded natural-language answer to a question.

## Basic Usage

```bash
memanto answer "question"
```

## Full Syntax

```bash
memanto answer "question" --limit 5
```

## Parameters

| Flag | Description | Default |
|------|-------------|---------|
| `question` | The question to answer (positional) | Required |
| `--limit` | Max memories to use as context | 5 |

## Examples

```bash
# General question
memanto answer "What database are we using and why did we choose it?"

# Ask about past commitments
memanto answer "What are my pending commitments?"

# Ask about preferences
memanto answer "What coding style does the user prefer?"

# Ask about decisions
memanto answer "What frontend framework did we decide on?"

# Ask about errors
memanto answer "What bugs have we encountered with the auth system?"

# Ask about goals
memanto answer "What are the project goals for this quarter?"
```

## When to Use `answer` vs `recall`

| Use `recall` when... | Use `answer` when... |
|---------------------|----------------------|
| You want raw memory entries | You want a synthesized response |
| You're building on the data programmatically | You want a human-readable answer |
| You need metadata (confidence, tags, IDs) | You want a quick answer to paste into context |
| You're exploring what's stored | The user asked a specific question |

## MANDATORY Before Saying "I Don't Know"

Before telling a user you don't have context on something, ALWAYS run:

```bash
memanto recall "topic of the question"
memanto answer "What did we decide about X?"
```

Do NOT say "I don't have context on that" without running these first.

## Python SDK (REST API)

```python
import httpx

async def get_answer(agent_id: str, session_token: str, question: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:8000/api/v2/agents/{agent_id}/answer",
            json={"question": question},
            headers={
                "X-Session-Token": session_token,
            }
        )
        result = response.json()
        print(result["answer"])
        print(f"Sources: {len(result['sources'])} memories used")
```
