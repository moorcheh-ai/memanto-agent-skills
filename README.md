# MEMANTO Agent Skills

<p align="center">
  <strong>Agent Skills for giving AI agents persistent memory with <a href="https://moorcheh.ai">MEMANTO</a> — the Universal Memory Layer for Agentic AI.</strong>
</p>

<p align="center">
  <a href="https://docs.moorcheh.ai">Documentation</a> ·
  <a href="https://console.moorcheh.ai">Console</a> ·
  <a href="https://docs.moorcheh.ai/python-sdk/introduction">Python SDK</a> ·
  <a href="https://agentskills.io/specification">Agent Skills Spec</a>
</p>

---

Each skill is a folder containing instructions, scripts, and resources that agents like Claude Code, Cursor, GitHub Copilot, Codex, Windsurf, Gemini CLI, and others can discover to give them persistent, long-term memory across sessions.

Works with any agent that supports the [Agent Skills](https://agentskills.io/home#adoption) format.

## What is MEMANTO?

MEMANTO is a universal memory layer built on top of Moorcheh — a semantic database with zero-indexing latency. It gives AI agents:

- **Persistent memory** across sessions and restarts
- **Semantic search** over everything the agent has learned
- **13 memory types** (facts, decisions, preferences, goals, errors, and more)
- **Trust scoring** via confidence levels and provenance tracking
- **Session management** with JWT-based agent identity
- **Multi-agent memory sharing** across workspaces

## Installation

### Using npx skills (Cursor, Claude Code, Gemini CLI, Codex, etc.)

```bash
npx skills add moorcheh-ai/memanto-agent-skills
```

### Using Claude Code Plugin Manager

```bash
# Step 1 — Add the marketplace (one time only)
/plugin marketplace add moorcheh-ai/memanto-agent-skills

# Step 2 — Install the plugin
/plugin install memanto
```

### Manual: clone and point your agent to the directory

```bash
git clone https://github.com/moorcheh-ai/memanto-agent-skills.git
cd memanto-agent-skills
claude --plugin-dir .
```

### Via memanto CLI (recommended)

```bash
pip install memanto
memanto connect claude-code   # or cursor, codex, windsurf, gemini-cli, etc.
```

## Quickstart

New to MEMANTO? Run the interactive onboarding:

```bash
/memanto:quickstart
```

## Configuration

### MEMANTO Account & API Key

1. Create a free Moorcheh account at [console.moorcheh.ai](https://console.moorcheh.ai)
2. Copy your API key
3. Set the environment variable:

```bash
export MOORCHEH_API_KEY="your-api-key"
```

4. Run first-time setup:

```bash
memanto config set api-key YOUR_KEY
memanto agent create my-agent
memanto agent activate my-agent
```

### Required Environment Variables

```bash
export MOORCHEH_API_KEY="your-api-key"
```

## Available Skills

<details>
<summary><strong>memanto</strong></summary>

Core operations for giving agents persistent memory:

- **Agent & Session Management** — Create agents, activate sessions, manage identity
- **Store Memories** — Remember facts, decisions, preferences, goals, errors, and more
- **Search Memories** — Semantic search across all stored memories
- **RAG Answers** — Generate answers grounded in memory
- **Daily Summaries** — Auto-generated summaries of recent activity
- **Memory Sync** — Sync memories to `MEMORY.md` for agent context

</details>

<details>
<summary><strong>memanto-cookbooks</strong></summary>

Blueprints for complete memory-powered AI applications:

- **Persistent Agent Memory** — Full setup for an agent with long-term memory
- **Multi-Agent Memory Sharing** — Share memory across agents in a team
- **Session Continuity** — Resume exactly where you left off across sessions
- **Memory Export & Audit** — Export, visualize, and audit agent memories
- **Daily Summary Automation** — Automated memory digests on a schedule
- **Memory-Powered RAG** — Build Q&A systems grounded in agent memory

</details>

## Usage

### Commands (Claude Code Plugin)

```bash
# Interactive onboarding
/memanto:quickstart

# Store a memory
/memanto:remember content "Chose PostgreSQL for metadata storage" type decision

# Search memories
/memanto:recall query "database architecture"

# Ask a question from memory
/memanto:answer question "What database did we choose and why?"

# Start or resume a session
/memanto:session agent_id my-agent

# Sync memories to MEMORY.md
/memanto:sync
```

### Skills (Any Compatible Agent)

The skill is automatically discovered by compatible agents. Simply describe what you want:

- "Remember that we decided to use React for the frontend"
- "What do you remember about our authentication approach?"
- "Store that the user prefers tabs over spaces"
- "Search memory for anything about database decisions"
- "What are my pending commitments?"
- "Summarize what we worked on this week"

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A [Moorcheh](https://console.moorcheh.ai) account and API key

## Resources

- [MEMANTO Documentation](https://docs.moorcheh.ai)
- [Agent Integration Guide](https://docs.moorcheh.ai/agent-integration)
- [Memory Best Practices](https://docs.moorcheh.ai/best-practices)
- [Python SDK](https://docs.moorcheh.ai/python-sdk/introduction)
- [API Reference](https://docs.moorcheh.ai/api-reference/introduction)
- [CLI User Guide](https://docs.moorcheh.ai/cli)
- [MCP Server](https://docs.moorcheh.ai/integrations/mcp/overview)
- [Agent Skills Specification](https://agentskills.io/specification)
