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
memanto agent activate my-agent --duration-hours 12
```

**What this does:**
- Issues a JWT session token (default 6-hour lifetime)
- Stores token in `~/.memanto/sessions/my-agent.json`
- All subsequent `memanto` commands use this session automatically

## Check Active Session

```bash
memanto session info
```

Output includes: agent ID, session ID, namespace, time remaining.

## Extend a Session

```bash
memanto session extend
memanto session extend --hours 4
```

## List Agents

```bash
memanto agent list
```

## Deactivate / End Session

```bash
memanto agent deactivate my-agent
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
| `API key missing` | `MOORCHEH_API_KEY` not set | Run `memanto config set api-key YOUR_KEY` |

## Python SDK

```python
import asyncio
from memanto.app.services.agent_service import AgentService
from memanto.app.services.session_service import SessionService

async def setup_agent():
    agent_svc = AgentService()
    session_svc = SessionService()

    # Create agent
    agent = await agent_svc.create_agent("my-agent", pattern="tool")
    print(f"Agent namespace: {agent.namespace}")

    # Activate session
    session = await session_svc.create_session(agent.agent_id)
    print(f"Session token: {session.session_token}")
    print(f"Expires: {session.expires_at}")

asyncio.run(setup_agent())
```
