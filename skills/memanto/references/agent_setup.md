# Agent Setup — Create and Activate an Agent

An **agent** in MEMANTO is a named identity with its own isolated memory namespace. Create one per project or per AI agent instance.

## Create an Agent

```bash
memanto agent create my-agent
```

With a pattern hint (influences initial bootstrap):
```bash
memanto agent create my-agent --pattern tool      # Tool-use agent (default)
memanto agent create my-agent --pattern project   # Project-scoped agent
memanto agent create my-agent --pattern support   # Support agent

# Optional description
memanto agent create my-agent --description "Memory for the billing service"
```

**What this does:**
- Creates a Moorcheh namespace `memanto_agent_my-agent`
- Saves agent metadata to `~/.memanto/agents/my-agent.json`
- **Activates the agent immediately** — a new agent needs no separate activate step

## Activate a Session

Activation is only needed for an agent that already exists — switching back to it, or restoring
a session that could not auto-renew.

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
- Removes `~/.memanto/agents/{agent_id}.json`
- Clears active session if this agent was currently active

**What happens only if you choose to purge cloud memories:**
- Deletes the Moorcheh namespace `memanto_agent_{agent_id}`
- All stored memories are permanently removed

**Note:** Cloud memories at [console.moorcheh.ai/namespaces](https://console.moorcheh.ai/namespaces) survive local deletion by default. A re-created agent with the same ID can access them again.


## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `No active session` | Session expired or never activated | Run `memanto agent activate <id>` |
| `Agent not found` | Agent ID doesn't exist locally | Run `memanto agent list` to see available agents |
| `Session expired` | Token lifetime exceeded | Run `memanto agent activate <id>` again |
| `API key missing` | `MOORCHEH_API_KEY` not set | Run `memanto` to configure interactively |
