"""
MEMANTO Recall Script

Searches persistent memories for the active agent. Supports semantic recall plus
three temporal modes (as-of, changed-since, recent).

Usage:
    # Semantic search (default)
    uv run recall.py "database architecture"
    uv run recall.py "authentication" --type fact --min-confidence 0.8 --limit 5

    # Temporal modes (omit the query)
    uv run recall.py --as-of "2026-05-01T12:00:00Z"
    uv run recall.py --changed-since "2026-05-03"
    uv run recall.py --recent --limit 10
    uv run recall.py --recent --type fact

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
from typing import Any

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
    query: str | None,
    memory_type: str | None,
    min_confidence: float,
    limit: int,
    as_of: str | None,
    changed_since: str | None,
    recent: bool,
) -> None:
    api_key = load_api_key()
    session = load_session()
    agent_id = session["agent_id"]
    session_token = session["session_token"]
    base_url = get_base_url()

    # Resolve endpoint + body based on which mode was selected
    type_list = [memory_type] if memory_type else None
    if recent:
        path = "recall/recent"
        body: dict[str, Any] = {"limit": limit}
        if type_list:
            body["type"] = type_list
        mode_label = "Recent (newest first)"
    elif as_of:
        path = "recall/as-of"
        body = {"as_of": as_of, "limit": limit}
        if type_list:
            body["type"] = type_list
        mode_label = f"As of {as_of}"
    elif changed_since:
        path = "recall/changed-since"
        body = {"since": changed_since, "limit": limit}
        if type_list:
            body["type"] = type_list
        mode_label = f"Changed since {changed_since}"
    else:
        if not query:
            print("Error: a query is required unless --recent, --as-of, or --changed-since is set.", file=sys.stderr)
            sys.exit(2)
        path = "recall"
        body = {
            "query": query,
            "limit": limit,
            "min_confidence": min_confidence,
        }
        if type_list:
            body["type"] = type_list
        mode_label = f"Semantic search for '{query}'"

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{base_url}/api/v2/agents/{agent_id}/{path}",
            headers=get_headers(api_key, session_token),
            json=body,
        )

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)

    results = response.json()
    memories = results.get("memories", [])

    if not memories:
        print(f"No memories found ({mode_label}).")
        return

    print(f"Found {len(memories)} memories ({mode_label}):\n")
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
    parser.add_argument("query", nargs="?", default=None, help="Natural language search query (omit for temporal modes)")
    parser.add_argument("--type", choices=VALID_TYPES, dest="memory_type", default=None)
    parser.add_argument("--min-confidence", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--as-of", dest="as_of", default=None, help="Point-in-time query (ISO date/datetime)")
    parser.add_argument("--changed-since", dest="changed_since", default=None, help="Differential query (ISO date/datetime)")
    parser.add_argument("--recent", action="store_true", help="List most recently stored memories (newest first)")
    args = parser.parse_args()

    temporal_flags = [bool(args.as_of), bool(args.changed_since), args.recent]
    if sum(temporal_flags) > 1:
        print("Error: --as-of, --changed-since, and --recent are mutually exclusive.", file=sys.stderr)
        sys.exit(2)

    if args.query and any(temporal_flags):
        print("Error: do not pass a query alongside --as-of, --changed-since, or --recent.", file=sys.stderr)
        sys.exit(2)

    asyncio.run(search_memories(
        query=args.query,
        memory_type=args.memory_type,
        min_confidence=args.min_confidence,
        limit=args.limit,
        as_of=args.as_of,
        changed_since=args.changed_since,
        recent=args.recent,
    ))


if __name__ == "__main__":
    main()
