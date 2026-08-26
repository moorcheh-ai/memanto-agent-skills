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

Each skill is a folder of instructions and references that coding agents discover
automatically, giving them persistent memory across sessions.

Works with any agent that supports the [Agent Skills](https://agentskills.io/home#adoption)
format, plus native plugins for Claude Code and Cursor.

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

### Cursor plugin

```bash
# Add this repository as a Cursor plugin, then enable "memanto"
```

Ships skills, commands, an always-on rule, and `sessionStart` / `preCompact` hooks that keep
`MEMORY.md` current.

### Any other agent (npx skills)

```bash
npx skills add moorcheh-ai/memanto-agent-skills
```

### Via the memanto CLI

```bash
pip install memanto
memanto connect claude-code   # writes instructions, skills, and hooks into the project
memanto connect list          # every supported agent and its install status
memanto connect multi         # pick several at once
```

### Supported agents

`memanto connect <name>` wires memory into each of these. The **Plugin** column marks the two
that also install as a native plugin from this repository:

| Agent | `connect` name | Instructions land in | Plugin |
|---|---|---|:--:|
| Claude Code | `claude-code` | `CLAUDE.md` | ✅ |
| Cursor | `cursor` | `.cursor/rules/memanto.mdc` | ✅ |
| Codex CLI | `codex` | `AGENTS.md` | |
| OpenCode | `opencode` | `AGENTS.md` | |
| GitHub Copilot | `github-copilot` | `.github/copilot-instructions.md` | |
| Windsurf | `windsurf` | `.windsurfrules` | |
| Gemini CLI | `gemini-cli` | `GEMINI.md` | |
| Cline | `cline` | `.clinerules/memanto.md` | |
| Continue | `continue` | `.continue/rules/memanto.md` | |
| Roo Code | `roo` | `.roo/rules/memanto.md` | |
| Augment Code | `augment` | `.augment/rules/memanto.md` | |
| Antigravity | `antigravity` | `.agent/skills` | |
| Goose | `goose` | `.goose/skills` | |

Every agent gets the two skills and the memory instructions. Claude Code and Cursor also get
commands and hooks, so `MEMORY.md` refreshes without anyone asking.

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

**A status line showing what memory is doing.**

```
👾 Memanto · my-project · 42 memories · +3 this session · synced 2m ago
```

Installed automatically on the plugin's first session — it never overwrites a `statusLine` you
already have, and `/memanto:statusline remove` turns it off. It degrades honestly rather than
lying: `not configured`, `no active agent`, `session expired`, or `stale 2d ago` when
`MEMORY.md` has drifted.

**Memory operations read as English, not shell.** A `PostToolUse` hook replaces the raw
command in chat with what actually happened:

```
👾 Memanto · stored a decision (confidence 0.95)
👾 Memanto · recalled 7 memories
👾 Memanto · MEMORY.md synced — 42 memories
```

It stays silent on anything it cannot describe confidently, and never runs for non-MEMANTO
commands.

**`MEMORY.md` stays current on its own.** A `SessionStart` hook runs `memanto memory sync`
whenever a session starts or resumes, so the agent has full context from your first message.
A `PreCompact` hook re-syncs before compaction, so context about to be summarized away is
written to memory first — the one moment context is most likely to be lost.

**Cursor gets the same treatment.** The Cursor plugin ships the skills, the commands, an
always-on rule, and `sessionStart` / `preCompact` hooks running the same
`hooks/session_start.py` — so `MEMORY.md` is current there too. Cursor uses camelCase hook
names and Claude Code uses PascalCase, so the two live in separate files
(`hooks/cursor-hooks.json` and `hooks/hooks.json`); Claude Code's loader rejects a file
containing Cursor's event names.

**A `memory-scout` subagent** for deep background. It fans out several recalls at once —
task terms, standing conventions, past decisions, known traps, open commitments, recent
changes — and returns a short sourced brief instead of a memory dump. It also surfaces
contradictions rather than silently picking a winner. Ask for it by name, or let Claude
delegate before a refactor:

> "Use memory-scout to get background before we touch the auth module"

**Claude reaches for memory unprompted.** The `memanto` skill loads automatically when you state
a decision worth keeping or ask what was decided earlier, and it forbids answering "I don't have
context on that" without checking memory first.

**Twelve commands** for when you want to drive it explicitly:

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
| `/memanto:statusline` | Install, preview, or remove the status line |

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
