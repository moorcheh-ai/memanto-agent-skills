"""
MEMANTO connection helper.

Provides a shared client setup used by all other scripts.
Reads MOORCHEH_API_KEY from the environment (or ~/.memanto/.env).
"""

import os
import json
from pathlib import Path


def load_api_key() -> str:
    """Load MOORCHEH_API_KEY from environment or ~/.memanto/.env."""
    key = os.environ.get("MOORCHEH_API_KEY")
    if key:
        return key

    env_file = Path.home() / ".memanto" / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("MOORCHEH_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                if key:
                    return key

    raise EnvironmentError(
        "MOORCHEH_API_KEY not found.\n"
        "Set it with: export MOORCHEH_API_KEY=your-key\n"
        "Or run:      memanto config set api-key YOUR_KEY"
    )


def load_session(agent_id: str | None = None) -> dict:
    """Load the active session from ~/.memanto/sessions/."""
    sessions_dir = Path.home() / ".memanto" / "sessions"

    if agent_id:
        session_file = sessions_dir / f"{agent_id}.json"
    else:
        # Find most recently modified session file
        files = sorted(sessions_dir.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
        if not files:
            raise FileNotFoundError(
                "No active session found. Run: memanto agent activate <agent-id>"
            )
        session_file = files[0]

    if not session_file.exists():
        raise FileNotFoundError(
            f"Session not found for agent '{agent_id}'. "
            "Run: memanto agent activate <agent-id>"
        )

    session = json.loads(session_file.read_text())

    if session.get("status") != "active":
        raise RuntimeError(
            f"Session for '{agent_id}' is not active (status: {session.get('status')}). "
            "Run: memanto agent activate <agent-id>"
        )

    return session


def get_headers(api_key: str, session_token: str | None = None) -> dict:
    """Build request headers for MEMANTO API calls."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if session_token:
        headers["X-Session-Token"] = session_token
    return headers


def get_base_url() -> str:
    """Get the MEMANTO server base URL."""
    config_file = Path.home() / ".memanto" / "config.yaml"
    if config_file.exists():
        import yaml
        config = yaml.safe_load(config_file.read_text()) or {}
        url = config.get("server_url", "http://localhost:8000")
        return url.rstrip("/")
    return "http://localhost:8000"
