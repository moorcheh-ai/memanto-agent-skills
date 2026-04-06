"""
MEMANTO Answer Script

Generates a RAG-powered answer grounded in persistent agent memory.

Usage:
    uv run answer.py "What database did we choose and why?"
    uv run answer.py "What are my pending commitments?" --type commitment

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
    sys.path.insert(0, str(__file__).replace("answer.py", ""))
    from memanto_conn import load_api_key, load_session, get_headers, get_base_url

VALID_TYPES = [
    "fact", "decision", "preference", "instruction", "goal", "commitment",
    "artifact", "learning", "event", "relationship", "observation", "error", "context",
]


async def get_answer(question: str, memory_type: str | None, limit: int) -> None:
    api_key = load_api_key()
    session = load_session()
    agent_id = session["agent_id"]
    session_token = session["session_token"]
    base_url = get_base_url()

    payload = {"query": question, "limit": limit}
    if memory_type:
        payload["type"] = memory_type

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{base_url}/api/v2/agents/{agent_id}/answer",
            headers=get_headers(api_key, session_token),
            json=payload,
        )

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)

    result = response.json()

    print(f"\nQuestion: {question}\n")
    print(f"Answer:\n{result.get('answer', 'No answer generated.')}\n")

    sources = result.get("sources", [])
    if sources:
        print(f"Based on {len(sources)} memories:")
        for src in sources[:5]:
            print(f"  - [{src.get('type', '?')}] {src.get('title', src.get('content', '')[:60])}")


def main():
    parser = argparse.ArgumentParser(description="Get a RAG-powered answer from MEMANTO memory")
    parser.add_argument("question", help="Question to answer from memory")
    parser.add_argument("--type", choices=VALID_TYPES, dest="memory_type", default=None,
                        help="Filter context to memories of this type")
    parser.add_argument("--limit", type=int, default=5,
                        help="Max memories to use as context (default: 5)")
    args = parser.parse_args()

    asyncio.run(get_answer(
        question=args.question,
        memory_type=args.memory_type,
        limit=args.limit,
    ))


if __name__ == "__main__":
    main()
