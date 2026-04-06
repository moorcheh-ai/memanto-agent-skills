"""
MEMANTO Remember Script

Stores a persistent memory for the active agent.

Usage:
    uv run remember.py "content" --type fact --confidence 0.9 --provenance explicit_statement --source my_agent --tags "tag1,tag2"

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
    sys.path.insert(0, str(__file__).replace("remember.py", ""))
    from memanto_conn import load_api_key, load_session, get_headers, get_base_url

VALID_TYPES = [
    "fact", "decision", "preference", "instruction", "goal", "commitment",
    "artifact", "learning", "event", "relationship", "observation", "error", "context",
]

VALID_PROVENANCE = [
    "explicit_statement", "inferred", "observed", "corrected", "validated",
]


async def store_memory(
    content: str,
    memory_type: str,
    confidence: float,
    provenance: str,
    source: str,
    tags: list[str],
    title: str | None = None,
) -> None:
    api_key = load_api_key()
    session = load_session()
    agent_id = session["agent_id"]
    session_token = session["session_token"]
    base_url = get_base_url()

    payload = {
        "content": content,
        "type": memory_type,
        "confidence": confidence,
        "provenance": provenance,
        "source": source,
        "tags": tags,
    }
    if title:
        payload["title"] = title

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{base_url}/api/v2/agents/{agent_id}/remember",
            headers=get_headers(api_key, session_token),
            json=payload,
        )

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)

    result = response.json()
    print(f"Memory stored: {result.get('id', 'unknown')}")
    print(f"  Type:       {memory_type}")
    print(f"  Confidence: {confidence}")
    print(f"  Tags:       {', '.join(tags)}")


def main():
    parser = argparse.ArgumentParser(description="Store a MEMANTO persistent memory")
    parser.add_argument("content", help="Memory content text")
    parser.add_argument("--type", required=True, choices=VALID_TYPES, dest="memory_type")
    parser.add_argument("--confidence", required=True, type=float)
    parser.add_argument("--provenance", required=True, choices=VALID_PROVENANCE)
    parser.add_argument("--source", required=True, help="Agent/tool name creating this memory")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--title", default=None)
    args = parser.parse_args()

    if not 0.0 <= args.confidence <= 1.0:
        print("Error: --confidence must be between 0.0 and 1.0", file=sys.stderr)
        sys.exit(1)

    if args.confidence < 0.6:
        print("Warning: confidence < 0.6 — consider not storing this memory (too uncertain)")
        sys.exit(0)

    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []

    asyncio.run(store_memory(
        content=args.content,
        memory_type=args.memory_type,
        confidence=args.confidence,
        provenance=args.provenance,
        source=args.source,
        tags=tags,
        title=args.title,
    ))


if __name__ == "__main__":
    main()
