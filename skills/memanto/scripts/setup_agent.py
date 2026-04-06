"""
MEMANTO Agent Setup Script

Creates a new MEMANTO agent and activates a session.

Usage:
    uv run setup_agent.py --agent-id my-agent
    uv run setup_agent.py --agent-id my-agent --pattern tool --duration-hours 8

Requirements:
    uv pip install memanto
    export MOORCHEH_API_KEY="your-api-key"
"""

# /// script
# requires-python = ">=3.10"
# dependencies = ["memanto"]
# ///

import argparse
import subprocess
import sys


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    print(result.stdout.strip())


def main():
    parser = argparse.ArgumentParser(description="Set up a MEMANTO agent")
    parser.add_argument("--agent-id", required=True, help="Agent identifier (e.g. my-project)")
    parser.add_argument(
        "--pattern",
        choices=["tool", "chat", "research"],
        default="tool",
        help="Agent pattern (default: tool)",
    )
    parser.add_argument(
        "--duration-hours",
        type=int,
        default=6,
        help="Session duration in hours (default: 6)",
    )
    args = parser.parse_args()

    print(f"\n=== Setting up MEMANTO agent: {args.agent_id} ===\n")

    # Create agent
    print(f"Creating agent '{args.agent_id}'...")
    run(["memanto", "agent", "create", args.agent_id, "--pattern", args.pattern])

    # Activate session
    print(f"\nActivating session (duration: {args.duration_hours}h)...")
    run([
        "memanto", "agent", "activate", args.agent_id,
        "--duration-hours", str(args.duration_hours),
    ])

    # Show session info
    print("\nSession info:")
    run(["memanto", "session", "info"])

    # Sync MEMORY.md
    print("\nSyncing MEMORY.md...")
    run(["memanto", "memory", "sync", "--project-dir", "."])

    print(f"\nAgent '{args.agent_id}' is ready. Start working!\n")


if __name__ == "__main__":
    main()
