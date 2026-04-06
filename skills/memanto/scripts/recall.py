"""
MEMANTO Recall Script

Searches persistent memories for the active agent using semantic similarity.

Usage:
    uv run recall.py "database architecture"
    uv run recall.py "authentication" --type fact --min-confidence 0.8 --limit 5

Requirements:
    uv pip install memanto httpx
    export MOORCHEH_API_KEY="your-api-key"
    # Must have an active session: memanto agent activate <agent-id>
    # Must have MEMANTO server running: memanto serve
"""

# /// script
# requires-python = ">=3.10"
# dependencies = ["memanto", "httpx"]
# ///

import argparse
import asyncio
import sys

import httpx

try:
    from memanto_conn import load_api_key, load_session, get_headers, get_base_url
except ImportError:
    sys.path.insert(0, str(__file__).replace("recall.py", ""))
    from memanto_conn import load_api_key, load_session, get_headers, get_base_url

VALID_TYPES = [
    "fact", "decision", "preference", "instruction", "goal", "commitment",
    "artifact", "learning", "event", "relationship", "observation", "error", "context",
]


async def search_memories(
    query: str,
    memory_type: str | None,
    min_confidence: float,
    limit: int,
) -> None:
    api_key = load_api_key()
    session = load_session()
    agent_id = session["agent_id"]
    session_token = session["session_token"]
    base_url = get_base_url()

    params = {
        "q": query,
        "limit": limit,
        "min_confidence": min_confidence,
    }
    if memory_type:
        params["type"] = memory_type

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            f"{base_url}/api/v2/agents/{agent_id}/recall",
            headers=get_headers(api_key, session_token),
            params=params,
        )

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)

    results = response.json()
    memories = results.get("memories", [])

    if not memories:
        print("No memories found.")
        return

    print(f"Found {len(memories)} memories for '{query}':\n")
    for i, mem in enumerate(memories, 1):
        conf = mem.get("confidence", 0)
        mtype = mem.get("type", "unknown")
        title = mem.get("title", "")
        content = mem.get("content", "")
        tags = ", ".join(mem.get("tags", []))

        print(f"[{i}] ({mtype}) [{conf:.2f}] {title or content[:60]}")
        if title and content:
            print(f"     {content[:120]}")
        if tags:
            print(f"     Tags: {tags}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Search MEMANTO persistent memories")
    parser.add_argument("query", help="Natural language search query")
    parser.add_argument("--type", choices=VALID_TYPES, dest="memory_type", default=None)
    parser.add_argument("--min-confidence", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    asyncio.run(search_memories(
        query=args.query,
        memory_type=args.memory_type,
        min_confidence=args.min_confidence,
        limit=args.limit,
    ))


if __name__ == "__main__":
    main()
