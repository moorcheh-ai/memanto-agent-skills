# MEMANTO Agent Skills

<p align="center">
  <strong>Agent Skills for giving AI agents persistent memory with <a href="https://moorcheh.ai">MEMANTO</a> — the Universal Memory Layer for Agentic AI.</strong>
</p>

<p align="center">
  <a href="https://docs.memanto.ai">Documentation</a> ·
  <a href="https://console.moorcheh.ai">Console</a> ·
  <a href="https://docs.memanto.ai/cli/overview">CLI Guide</a> ·
  <a href="https://agentskills.io/specification">Agent Skills Spec</a>
</p>

---

Each skill is a folder of instructions and references that agents like Claude Code, Cursor,
GitHub Copilot, Codex, Windsurf, and Gemini CLI can discover, giving them persistent memory
across sessions.

Works with any agent that supports the [Agent Skills](https://agentskills.io/home#adoption)
format.

## What is MEMANTO?

MEMANTO is a memory companion agent built on Moorcheh, a semantic database with zero-indexing
latency. It gives AI agents:

- **Persistent memory** across sessions and restarts
- **Semantic and temporal recall** — search by meaning, or ask what was true last Tuesday
- **13 memory types** — facts, decisions, preferences, goals, errors, and more
- **Trust scoring** via confidence levels and provenance tracking
- **Conflict detection** so contradictory memories get caught instead of quietly poisoning recall
- **Expiry policy** so memory stays useful instead of only growing

## Installation

### Claude Code plugin (recommended)

```bash
/plugin marketplace add moorcheh-ai/memanto-agent-skills
/plugin install memanto
```

### Using npx skills (Cursor, Gemini CLI, Codex, etc.)

```bash
npx skills add moorcheh-ai/memanto-agent-skills
```

### Via the memanto CLI

```bash
pip install memanto
memanto connect claude-code   # or cursor, codex, windsurf, gemini-cli, cline, roo, goose, …
memanto connect list          # everything supported
```

### Manual

```bash
git clone https://github.com/moorcheh-ai/memanto-agent-skills.git
claude --plugin-dir ./memanto-agent-skills
```

## Setup

1. Create a free Moorcheh account at [console.moorcheh.ai](https://console.moorcheh.ai) and copy
   your API key.
2. Install and configure the CLI:

```bash
pip install memanto     # Python 3.10–3.12
memanto                 # interactive setup — writes the key to ~/.memanto/.env
```

   Or skip the wizard by exporting the key yourself:

```bash
export MOORCHEH_API_KEY="your-api-key"
```

3. Create an agent for the project. This **also activates it** — there is no separate activation
   step for a new agent:

```bash
memanto agent create my-project
memanto status
```

Or just run `/memanto:quickstart` in Claude Code and it will walk you through all of it.

## What you get in Claude Code

**`MEMORY.md` stays current on its own.** The plugin installs a `SessionStart` hook that runs
`memanto memory sync` whenever a session starts or resumes, so the agent has full context from
your first message — no command to remember.

**Claude reaches for memory unprompted.** The `memanto` skill loads automatically when you state
a decision worth keeping or ask what was decided earlier, and it forbids answering "I don't have
context on that" without checking memory first.

**Eleven commands** for when you want to drive it explicitly:

| Command | What it does |
|---|---|
| `/memanto:quickstart` | Set up MEMANTO for this project, end to end |
| `/memanto:remember` | Store something, with type/confidence/provenance chosen for you |
| `/memanto:recall` | Search by meaning, type, tag, or point in time |
| `/memanto:answer` | Answer a question grounded in memory (RAG) |
| `/memanto:capture` | Review this session and store what is worth keeping |
| `/memanto:forget` | Correct, expire, or delete a memory |
| `/memanto:upload` | Ingest a PDF/DOCX/XLSX/CSV/MD document into memory |
| `/memanto:conflicts` | Find and resolve contradictory memories |
| `/memanto:sync` | Refresh `MEMORY.md` (or export an OKF bundle) |
| `/memanto:session` | Show or switch the active agent |
| `/memanto:status` | Health check — config, session, agents, what is stored |

### Optional: capture memory automatically at session end

`/memanto:capture` is deliberately manual, because storing memories costs API calls and writes
data you may not want. If you would rather it happen on its own, add a `Stop` hook to your own
settings — this plugin will not do it for you:

```jsonc
// .claude/settings.json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "memanto daily-summary 2>/dev/null || true"
      }]
    }]
  }
}
```

## Skills

<details>
<summary><strong>memanto</strong> — core memory operations</summary>

Storing and retrieving memory: `remember`, `recall`, `answer`, `edit`/`forget`/`expire`, file
upload, conflict resolution, expiry policy, provider migration, and `MEMORY.md` sync. Loads
automatically when relevant.

</details>

<details>
<summary><strong>memanto-cookbooks</strong> — application blueprints</summary>

End-to-end guides for building on MEMANTO: persistent agent memory, session continuity, memory
export and audit, daily summary automation, memory-powered RAG, conflict resolution, and
migrating from Mem0/Letta/Supermemory.

</details>

## Usage in any compatible agent

The skill is discovered automatically. Just describe what you want:

- "Remember that we decided to use React for the frontend"
- "What do you remember about our authentication approach?"
- "What are my pending commitments?"
- "That's wrong — we switched to DynamoDB last month"
- "Load everything you know about this project"

## Requirements

- Python 3.10–3.12
- A [Moorcheh](https://console.moorcheh.ai) account and API key — or run
  [on-prem](https://docs.memanto.ai/on-prem/quickstart) with no key at all
- Claude Code (for the plugin), or any Agent Skills-compatible tool

## Resources

- [MEMANTO Documentation](https://docs.memanto.ai)
- [CLI Reference](https://docs.memanto.ai/cli/overview)
- [Claude Code Integration](https://docs.memanto.ai/integrations/claude-code)
- [All Integrations](https://docs.memanto.ai/integrations/overview)
- [Memory Types Reference](https://docs.memanto.ai/reference/memory-types)
- [API Reference](https://docs.memanto.ai/api-reference/authentication)
- [MCP Server](https://docs.memanto.ai/integrations/mcp)
- [Self-Hosting (On-Prem)](https://docs.memanto.ai/on-prem/quickstart)
- [Agent Skills Specification](https://agentskills.io/specification)

## License

MIT — see [LICENSE](LICENSE).
