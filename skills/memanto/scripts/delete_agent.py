"""
MEMANTO Delete Agent Script

Deletes a MEMANTO agent. Mirrors the CLI behavior:
  1. Removes local agent metadata via DELETE /api/v2/agents/{agent_id}
  2. Optionally deletes the Moorcheh cloud namespace (all memories) via
     DELETE /api/v1/namespaces/agent/{agent_id}

Usage:
    uv run delete_agent.py --agent-id my-agent
    uv run delete_agent.py --agent-id my-agent --force           # skip confirmation
    uv run delete_agent.py --agent-id my-agent --delete-cloud    # also purge cloud memories
    uv run delete_agent.py --agent-id my-agent --keep-cloud      # always preserve cloud memories

Requirements:
    uv pip install memanto httpx
    export MOORCHEH_API_KEY="your-api-key"
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
    from memanto_conn import load_api_key, get_headers, get_base_url
except ImportError:
    sys.path.insert(0, str(__file__).replace("delete_agent.py", ""))
    from memanto_conn import load_api_key, get_headers, get_base_url


async def delete_agent(agent_id: str, delete_cloud: bool) -> None:
    api_key = load_api_key()
    base_url = get_base_url()
    headers = get_headers(api_key)

    async with httpx.AsyncClient(timeout=30) as client:
        # Step 1: delete local agent metadata
        response = await client.delete(
            f"{base_url}/api/v2/agents/{agent_id}",
            headers=headers,
        )

        if response.status_code == 404:
            print(f"Error: Agent '{agent_id}' not found.", file=sys.stderr)
            sys.exit(1)

        if response.status_code not in (200, 204):
            print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
            sys.exit(1)

        print(f"Agent '{agent_id}' deleted (local metadata removed).")

        # Step 2 (optional): delete Moorcheh cloud namespace
        if delete_cloud:
            ns_response = await client.delete(
                f"{base_url}/api/v1/namespaces/agent/{agent_id}",
                headers=headers,
            )

            if ns_response.status_code in (200, 204):
                print(f"Cloud memories for '{agent_id}' deleted.")
            else:
                print(
                    f"Warning: Agent deleted locally, but failed to delete cloud namespace "
                    f"({ns_response.status_code}): {ns_response.text}",
                    file=sys.stderr,
                )
        else:
            print(
                "Cloud memories preserved. "
                "View them at https://console.moorcheh.ai/namespaces"
            )


def main():
    parser = argparse.ArgumentParser(description="Delete a MEMANTO agent")
    parser.add_argument("--agent-id", required=True, help="Agent identifier to delete")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt",
    )

    cloud_group = parser.add_mutually_exclusive_group()
    cloud_group.add_argument(
        "--delete-cloud",
        action="store_true",
        help="Also delete all cloud memories (non-recoverable)",
    )
    cloud_group.add_argument(
        "--keep-cloud",
        action="store_true",
        help="Preserve cloud memories without prompting",
    )

    args = parser.parse_args()

    if not args.force:
        answer = input(
            f"Delete agent '{args.agent_id}'? This cannot be undone. [y/N] "
        ).strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted.")
            sys.exit(0)

    # Determine whether to delete cloud memories
    if args.delete_cloud:
        delete_cloud = True
    elif args.keep_cloud:
        delete_cloud = False
    else:
        # Interactive prompt — mirrors CLI default (keep=True)
        keep = input(
            "Keep cloud memories on Moorcheh? "
            "(https://console.moorcheh.ai/namespaces) [Y/n] "
        ).strip().lower()
        delete_cloud = keep in ("n", "no")

    asyncio.run(delete_agent(args.agent_id, delete_cloud=delete_cloud))


if __name__ == "__main__":
    main()
