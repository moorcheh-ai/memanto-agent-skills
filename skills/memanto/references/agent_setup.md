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
# This removes the agent's local metadata but does NOT delete memories from Moorcheh
memanto agent delete my-agent
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
