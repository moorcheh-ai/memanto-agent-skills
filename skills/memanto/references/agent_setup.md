# Agent Setup — Create and Activate an Agent

An **agent** in MEMANTO is a named identity with its own isolated memory namespace. Create one per project or per AI agent instance.

## Create an Agent

```bash
memanto agent create my-agent
```

With a pattern hint (influences initial bootstrap):
```bash
memanto agent create my-agent --pattern tool       # Tool-use agent
memanto agent create my-agent --pattern chat       # Conversational agent
memanto agent create my-agent --pattern research   # Research agent
```

**What this does:**
- Creates a Moorcheh namespace `memanto_agent_my-agent`
- Saves agent metadata to `~/.memanto/agents/my-agent.json`

## Activate a Session

```bash
memanto agent activate my-agent
```

With custom duration:
```bash
memanto agent activate my-agent --hours 12
```

**What this does:**
- Issues a JWT session token (default 6-hour lifetime)
- Stores token in `~/.memanto/sessions/my-agent.json`
- All subsequent `memanto` commands use this session automatically

## Check Active Session

```bash
memanto session info
```

Output includes: agent ID, token preview, status, expiry, and time remaining.

## List Agents

```bash
memanto agent list
```

## Deactivate / End Session

```bash
memanto agent deactivate
```

## Delete an Agent

```bash
memanto agent delete my-agent
```

The CLI runs a **two-step delete**:

1. **Confirm deletion** — interactive prompt (skip with `--force`)
2. **Keep cloud memories?** — prompts whether to preserve or purge the Moorcheh namespace
   - Default is **keep** (`Y`) — local metadata removed, cloud memories preserved
   - Choose `n` — also deletes `memanto_agent_{agent_id}` namespace and all stored memories from Moorcheh (non-recoverable)

```bash
# Skip confirmation prompt
memanto agent delete my-agent --force
```

**What always happens:**
- Calls `DELETE /api/v2/agents/{agent_id}`
- Removes `~/.memanto/agents/{agent_id}.json`
- Clears active session if this agent was currently active

**What happens only if you choose to purge cloud memories:**
- Deletes the Moorcheh namespace `memanto_agent_{agent_id}`
- All stored memories are permanently removed

**Note:** Cloud memories at [console.moorcheh.ai/namespaces](https://console.moorcheh.ai/namespaces) survive local deletion by default. A re-created agent with the same ID can access them again.

Or via the Python script:

```bash
uv run skills/memanto/scripts/delete_agent.py --agent-id my-agent

# Skip prompts
uv run skills/memanto/scripts/delete_agent.py --agent-id my-agent --force --keep-cloud
uv run skills/memanto/scripts/delete_agent.py --agent-id my-agent --force --delete-cloud
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `No active session` | Session expired or never activated | Run `memanto agent activate <id>` |
| `Agent not found` | Agent ID doesn't exist locally | Run `memanto agent list` to see available agents |
| `Session expired` | Token lifetime exceeded | Run `memanto agent activate <id>` again |
| `API key missing` | `MOORCHEH_API_KEY` not set | Run `memanto` to configure interactively |

## Python SDK (REST API)

```python
import httpx
import asyncio

async def setup_agent():
    base_url = "http://localhost:8000"

    async with httpx.AsyncClient() as client:
        # Create agent
        resp = await client.post(
            f"{base_url}/api/v2/agents",
            json={"name": "my-agent"}
        )
        agent = resp.json()
        print(f"Agent namespace: {agent.get('namespace')}")

        # Activate session
        resp = await client.post(f"{base_url}/api/v2/agents/my-agent/activate")
        session = resp.json()
        print(f"Session token: {session.get('session_token')}")
        print(f"Expires: {session.get('expires_at')}")

if __name__ == "__main__":
    asyncio.run(setup_agent())
```
