# Session Management

MEMANTO uses JWT-based sessions to identify which agent is active. Sessions have a configurable lifetime (default: 6 hours).

## Session Lifecycle

```
agent create → agent activate → [work] → session extend → [work] → agent deactivate
```

## Commands

### Check Session Status

```bash
memanto session info
```

Output:
```
Agent:      my-agent
Session ID: sess_abc123
Namespace:  memanto_agent_my-agent
Started:    2025-03-15 09:00:00
Expires:    2025-03-15 15:00:00
Remaining:  4h 32m
Status:     active
```

### Extend Session

```bash
memanto session extend
memanto session extend --hours 4
```

### View All Agents

```bash
memanto agent list
```

### Switch Active Agent

```bash
memanto agent activate other-agent
```

Only one agent can be active at a time per terminal session.

## Session Start Checklist

Always run this at the beginning of a work session:

```bash
# 1. Activate (or re-activate if expired)
memanto agent activate my-agent

# 2. Sync MEMORY.md to project root
memanto memory sync --project-dir .

# 3. Load context
memanto recall "instructions decisions goals" --limit 20
memanto answer "What are my pending commitments?"
```

## Session File

The active session token is stored at `~/.memanto/sessions/{agent_id}.json`:

```json
{
  "session_id": "sess_abc123",
  "session_token": "eyJ...",
  "agent_id": "my-agent",
  "namespace": "memanto_agent_my-agent",
  "started_at": "2025-03-15T09:00:00Z",
  "expires_at": "2025-03-15T15:00:00Z",
  "status": "active"
}
```

## Token in API Calls

When calling the MEMANTO API directly, include the session token as a header:

```
X-Session-Token: eyJ...
Authorization: Bearer YOUR_MOORCHEH_API_KEY
```

## Auto-Hook (Claude Code)

When connected via `memanto connect claude-code`, a SessionStart hook runs automatically:

```bash
memanto memory sync --project-dir .
```

This populates `MEMORY.md` every time Claude Code starts, ensuring full context from the first message.

## Session Duration

| Use Case | Recommended Duration |
|----------|---------------------|
| Short task | 2–4 hours |
| Full workday | 8–10 hours |
| Long background process | 24 hours |
| CI/CD pipeline | 1–2 hours |

```bash
memanto agent activate my-agent --duration-hours 24
```
