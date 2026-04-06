# Cookbook: Memory-Powered RAG

Build a question-answering system grounded in agent memory. Use MEMANTO's semantic search + RAG pipeline to answer questions from everything the agent has learned.

## Overview

MEMANTO's `answer` command implements a full RAG pipeline:
1. Semantic search over stored memories (retrieval)
2. Rank by relevance and confidence
3. Synthesize a grounded natural-language answer (generation)

## Basic Usage

```bash
# Ask anything from memory
memanto answer "What database did we choose and why?"
memanto answer "What are my pending commitments?"
memanto answer "What bugs have we encountered with authentication?"
memanto answer "What does the user prefer for code style?"
```

## REST API

```python
import httpx

async def ask_from_memory(agent_id: str, session_token: str, question: str) -> dict:
    """Ask a question grounded in agent memory."""
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"http://localhost:8000/api/v2/agents/{agent_id}/answer",
            headers={
                "Authorization": f"Bearer {MOORCHEH_API_KEY}",
                "X-Session-Token": session_token,
            },
            json={
                "query": question,
                "limit": 5,      # Max memories to use as context
            }
        )

    result = response.json()
    return {
        "answer": result["answer"],
        "sources": result["sources"],    # Memories used as context
        "source_count": len(result["sources"]),
    }

# Usage
result = await ask_from_memory(
    agent_id="my-project",
    session_token=session_token,
    question="What database are we using and what version?",
)
print(result["answer"])
print(f"Based on {result['source_count']} memories")
```

## Building a Chat Interface

```python
import asyncio
import httpx
from memanto_conn import load_api_key, load_session, get_headers, get_base_url

async def memory_chat():
    """Simple chat loop grounded in agent memory."""
    api_key = load_api_key()
    session = load_session()
    agent_id = session["agent_id"]
    session_token = session["session_token"]
    base_url = get_base_url()
    headers = get_headers(api_key, session_token)

    print(f"Memory-powered Q&A for agent: {agent_id}")
    print("Type 'quit' to exit\n")

    async with httpx.AsyncClient(timeout=60) as client:
        while True:
            question = input("Question: ").strip()
            if question.lower() in ("quit", "exit", "q"):
                break
            if not question:
                continue

            response = await client.post(
                f"{base_url}/api/v2/agents/{agent_id}/answer",
                headers=headers,
                json={"query": question, "limit": 5},
            )

            if response.status_code == 200:
                result = response.json()
                print(f"\nAnswer: {result['answer']}")
                sources = result.get("sources", [])
                if sources:
                    print(f"(Based on {len(sources)} memories)\n")
            else:
                print(f"Error: {response.status_code} — {response.text}\n")

asyncio.run(memory_chat())
```

## Multi-Type RAG Strategy

For comprehensive answers, combine `answer` with `recall`:

```python
async def comprehensive_answer(question: str) -> str:
    """Get a comprehensive answer using both recall and RAG."""
    # Step 1: Recall raw memories
    memories = await client.get(
        f"{base_url}/api/v2/agents/{agent_id}/recall",
        params={"q": question, "limit": 10},
        headers=headers,
    )

    # Step 2: Get RAG answer
    answer = await client.post(
        f"{base_url}/api/v2/agents/{agent_id}/answer",
        json={"query": question, "limit": 5},
        headers=headers,
    )

    result = answer.json()
    return result["answer"]
```

## Citation Tracking

The `answer` endpoint returns `sources` — the list of memories used as context. Use these to cite where answers come from:

```python
result = response.json()
answer = result["answer"]
sources = result["sources"]

print(answer)
print("\nBased on:")
for src in sources:
    print(f"  [{src['type']}] {src.get('title', src['content'][:60])} (confidence: {src['confidence']:.2f})")
```

## Limitations

- RAG answers are only as good as what's been stored
- The model synthesizes — it may occasionally hallucinate; check sources
- For precise factual lookups, use `recall` instead of `answer`
- Context window: up to 5 memories by default (increase with `--limit`)
