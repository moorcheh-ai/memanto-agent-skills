# /memanto:session

Manage MEMANTO agent sessions — create, activate, extend, or inspect.

## Syntax

```
/memanto:session agent_id <id> [action activate|info|extend] [duration_hours <n>]
```

## Examples

```bash
# Activate a session
memanto agent activate my-agent

# Check session status
memanto session info

# Extend current session
memanto session extend --hours 4

# List all agents
memanto agent list

# Create a new agent
memanto agent create my-agent --pattern tool
```

## Session Lifecycle

1. `memanto agent create <id>` — Create agent identity (one time)
2. `memanto agent activate <id>` — Start a session (each work session)
3. `memanto session info` — Check status and time remaining
4. `memanto session extend` — Extend before expiry
5. `memanto agent deactivate <id>` — End session

## Error: No Active Session

If you see "No active session", run:
```bash
memanto agent activate <agent-id>
```
