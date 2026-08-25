#!/usr/bin/env python3
"""MEMANTO status line for Claude Code.

Renders a one-line summary of the agent's memory state:

    👾 Memanto · my-project · 42 memories · +3 this session · synced 2m ago

Reads Claude Code's status line JSON on stdin and derives everything from real
MEMANTO artifacts — the active session file and the project's MEMORY.md — so it
needs no cooperating hooks and no background process.

Install it with `/memanto:statusline`, or by hand:

    "statusLine": {
      "type": "command",
      "command": "python /path/to/statusline.py",
      "refreshInterval": 5
    }

Must never raise and never write to stderr: a status line that crashes disrupts
the session it is decorating. Every failure path degrades to a shorter line or
to no output at all.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BRAND = "👾 Memanto"

# Session-baseline records older than this are pruned on write.
BASELINE_TTL = 7 * 24 * 3600
# MEMORY.md older than this is reported as stale rather than current.
STALE_AFTER = 24 * 3600
# Warn when the MEMANTO session has less than this left.
EXPIRY_WARN = 30 * 60

RESET = "\033[0m"
BOLD = "\033[1m"
VIOLET = "\033[38;2;167;139;250m"
DIM = "\033[38;5;245m"
WHITE = "\033[97m"
AMBER = "\033[38;2;251;191;36m"


def _memanto_home() -> Path:
    return Path(os.path.expanduser("~")) / ".memanto"


def _use_color() -> bool:
    # https://no-color.org/ — any non-empty value disables color.
    if os.environ.get("NO_COLOR"):
        return False
    return os.environ.get("TERM") != "dumb"


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _age(seconds: float) -> str:
    seconds = max(0, int(seconds))
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    return f"{hours}h" if hours < 24 else f"{hours // 24}d"


def _parse_iso(value: str):
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return None


def active_agent() -> str | None:
    """Agent id from ~/.memanto/sessions/active, if one is active."""
    try:
        name = (_memanto_home() / "sessions" / "active").read_text(encoding="utf-8").strip()
    except Exception:
        return None
    return name or None


def session_state(agent: str) -> tuple[str, float | None]:
    """Return (status, seconds_remaining) for the agent's session."""
    data = _read_json(_memanto_home() / "sessions" / f"{agent}.json")
    if not isinstance(data, dict):
        return "unknown", None

    remaining = None
    expires = _parse_iso(data.get("expires_at", ""))
    if expires is not None:
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        remaining = (expires - datetime.now(timezone.utc)).total_seconds()
        if remaining <= 0:
            return "expired", 0.0

    return str(data.get("status") or "unknown"), remaining


def is_configured() -> bool:
    if os.environ.get("MOORCHEH_API_KEY"):
        return True
    home = _memanto_home()
    for candidate in (home / ".env", home / "config.yaml"):
        if candidate.exists():
            return True
    return False


def memory_snapshot(project_dir: str | None) -> tuple[int | None, float | None]:
    """Return (total_memories, seconds_since_sync) from the project's MEMORY.md."""
    if not project_dir:
        return None, None
    path = Path(project_dir) / "MEMORY.md"
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
        synced = time.time() - path.stat().st_mtime
    except Exception:
        return None, None

    match = re.search(r"Total memories:\s*\*{0,2}\s*(\d+)", raw)
    if match:
        return int(match.group(1)), synced
    # Older exports omit the summary line; fall back to counting bullets.
    return (len(re.findall(r"^\s*[-*]\s+\S", raw, re.M)) or None), synced


def session_delta(session_id: str | None, total: int | None) -> int | None:
    """Memories added since this Claude Code session first rendered a line.

    The status line maintains its own baseline, so no hook has to write state.
    """
    if not session_id or total is None:
        return None

    root = _memanto_home() / ".claude-statusline"
    key = hashlib.sha256(session_id.encode("utf-8")).hexdigest()[:32]
    record = root / f"{key}.json"

    existing = _read_json(record)
    if isinstance(existing, dict) and isinstance(existing.get("baseline"), int):
        delta = total - existing["baseline"]
        return delta if delta > 0 else None

    try:
        root.mkdir(parents=True, exist_ok=True)
        tmp = root / f".{key}.{os.getpid()}.tmp"
        tmp.write_text(json.dumps({"baseline": total, "at": time.time()}), encoding="utf-8")
        os.replace(tmp, record)
        _prune(root)
    except Exception:
        pass
    return None


def _prune(root: Path) -> None:
    cutoff = time.time() - BASELINE_TTL
    try:
        for entry in root.glob("*.json"):
            if entry.stat().st_mtime < cutoff:
                entry.unlink(missing_ok=True)
    except Exception:
        pass


def render(payload: dict, color: bool = True) -> str:
    def paint(text: str, *codes: str) -> str:
        return f"{''.join(codes)}{text}{RESET}" if color else text

    brand = paint(BRAND, VIOLET, BOLD)
    sep = paint(" · ", DIM) if color else " · "

    if not is_configured():
        return brand + sep + paint("not configured", AMBER)

    agent = active_agent()
    if not agent:
        return brand + sep + paint("no active agent", AMBER)

    status, remaining = session_state(agent)
    if status == "expired":
        return brand + sep + paint(f"{agent} · session expired", AMBER)

    workspace = payload.get("workspace") or {}
    project_dir = workspace.get("project_dir") or workspace.get("current_dir") or payload.get("cwd")
    total, synced = memory_snapshot(project_dir)

    parts = [paint(agent, WHITE)]

    if total is not None:
        label = "memory" if total == 1 else "memories"
        parts.append(paint(f"{total} {label}", WHITE))
        delta = session_delta(payload.get("session_id"), total)
        if delta:
            parts.append(paint(f"+{delta} this session", VIOLET))
    else:
        parts.append(paint("no MEMORY.md", DIM))

    if synced is not None:
        parts.append(paint(f"{'stale' if synced > STALE_AFTER else 'synced'} {_age(synced)} ago", DIM))

    if remaining is not None and remaining < EXPIRY_WARN:
        parts.append(paint(f"expires in {_age(remaining)}", AMBER))

    return brand + sep + sep.join(parts)


def read_stdin(timeout: float = 0.5) -> dict:
    if sys.stdin is None or sys.stdin.isatty():
        return {}
    try:
        data = sys.stdin.read()
    except Exception:
        return {}
    try:
        parsed = json.loads(data.strip() or "{}")
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _write(line: str) -> None:
    """Write the line as UTF-8 regardless of the console's default encoding.

    Windows consoles default to a legacy code page (cp1252), which cannot encode
    the brand emoji — without this the whole status line would silently vanish.
    """
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stdout.write(line)
        return
    except Exception:
        pass
    try:
        buffer = getattr(sys.stdout, "buffer", None)
        if buffer is not None:
            buffer.write(line.encode("utf-8", "replace"))
            return
    except Exception:
        pass
    # Last resort: drop anything the console cannot represent.
    try:
        sys.stdout.write(line.encode("ascii", "ignore").decode("ascii"))
    except Exception:
        pass


def main() -> None:
    try:
        line = render(read_stdin(), color=_use_color())
        if line:
            _write(line)
    except Exception:
        # A status line must fail silently so it never disrupts Claude Code.
        pass


if __name__ == "__main__":
    main()
