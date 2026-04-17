"""
MEMANTO File Upload Script

Uploads a document file into the active agent's memory namespace.
Uploaded content is immediately searchable via `memanto recall`.

Supported formats: .pdf  .docx  .xlsx  .json  .txt  .csv  .md
Maximum file size: 5 GB

Usage:
    uv run upload_file.py path/to/document.pdf
    uv run upload_file.py path/to/notes.md

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
from pathlib import Path

import httpx

try:
    from memanto_conn import load_api_key, load_session, get_headers, get_base_url
except ImportError:
    sys.path.insert(0, str(__file__).replace("upload_file.py", ""))
    from memanto_conn import load_api_key, load_session, get_headers, get_base_url

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".json", ".txt", ".csv", ".md"}


async def upload_file(file_path: Path) -> None:
    api_key = load_api_key()
    session = load_session()
    agent_id = session["agent_id"]
    session_token = session["session_token"]
    base_url = get_base_url()

    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        print(
            f"Error: Unsupported file type '{file_path.suffix}'.\n"
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}",
            file=sys.stderr,
        )
        sys.exit(1)

    file_size = file_path.stat().st_size
    print(f"Uploading '{file_path.name}' ({file_size:,} bytes) to agent '{agent_id}'...")

    headers = get_headers(api_key, session_token)
    del headers["Content-Type"]  # Let httpx set multipart boundary

    async with httpx.AsyncClient(timeout=300) as client:
        with open(file_path, "rb") as f:
            response = await client.post(
                f"{base_url}/api/v2/agents/{agent_id}/upload-file",
                headers=headers,
                files={"file": (file_path.name, f, _mime_type(file_path.suffix))},
            )

    if response.status_code not in (200, 201):
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)

    result = response.json()
    status = result.get("status", "unknown")
    message = result.get("message", "")

    if status == "uploaded":
        print(f"Upload successful.")
        print(f"  File:      {result.get('file_name', file_path.name)}")
        print(f"  Size:      {result.get('file_size', file_size):,} bytes")
        print(f"  Agent:     {result.get('agent_id', agent_id)}")
        print(f"  Namespace: {result.get('namespace', 'unknown')}")
        print(f"\nContent is now searchable via: memanto recall \"<query>\"")
    else:
        print(f"Upload status: {status}")
        if message:
            print(f"Message: {message}")


def _mime_type(suffix: str) -> str:
    return {
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".json": "application/json",
        ".txt": "text/plain",
        ".csv": "text/csv",
        ".md": "text/markdown",
    }.get(suffix.lower(), "application/octet-stream")


def main():
    parser = argparse.ArgumentParser(description="Upload a document file to MEMANTO memory")
    parser.add_argument("file", help="Path to the file to upload")
    args = parser.parse_args()

    asyncio.run(upload_file(Path(args.file)))


if __name__ == "__main__":
    main()
