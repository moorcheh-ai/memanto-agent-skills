# MEMANTO Agent Skills — Setup Guide

This repository provides agent skills that give AI agents persistent memory via MEMANTO.

## Prerequisites

- Python 3.10–3.12
- A [Moorcheh](https://console.moorcheh.ai) account (free)

## Quick Setup

```bash
pip install memanto

# Configure — either run the interactive wizard...
memanto
# ...or set the key yourself
export MOORCHEH_API_KEY="your-api-key"

# Create the agent (this activates it too)
memanto agent create my-agent
memanto status
```

There is no `memanto config set` command; the wizard and the environment variable are the two
ways to supply an API key.

## Skills in this Repository

| Skill | Description |
|-------|-------------|
| [memanto](skills/memanto/SKILL.md) | Core memory operations — remember, recall, answer, correct, upload, sync |
| [memanto-cookbooks](skills/memanto-cookbooks/SKILL.md) | Blueprints for memory-powered AI applications |

## Key Commands

```bash
# Store
memanto remember "content" --type decision --confidence 0.9 \
  --provenance explicit_statement --source claude_code --tags "a,b"

# Retrieve
memanto recall "query" --limit 10 --type decision --tags "auth"
memanto recall --recent --limit 10          # newest first, no query
memanto recall --as-of "2026-01-15"         # what was true then
memanto answer "What did we decide about X?"

# Correct and retire
memanto edit <id> --content "..." --confidence 0.95
memanto memory expire <id> --reason superseded   # reversible
memanto forget <id> --force                      # permanent

# Documents
memanto upload report.pdf

# Project context
memanto memory sync --project-dir .

# Housekeeping
memanto detect-conflicts && memanto conflicts --list
memanto policy show
memanto schedule enable         # nightly summary + conflict detection + expiry sweep

# Session
memanto status
memanto session info
memanto agent list
```

## Memory Types

`fact` · `decision` · `preference` · `instruction` · `goal` · `commitment` · `artifact` ·
`learning` · `event` · `relationship` · `observation` · `error` · `context`

## Provenance

`explicit_statement` · `inferred` · `observed` · `corrected` · `validated` · `imported`

## Notes

- `memanto agent create` creates **and** activates. Only use `memanto agent activate` to switch
  back to an existing agent.
- Sessions auto-renew by default. There is no `session extend` command; set the lifetime up
  front with `memanto agent activate <id> --hours <n>`.
- The CLI talks to Moorcheh directly. `memanto serve` is only needed for the HTTP API and
  `memanto ui`, not for ordinary CLI use.

## Resources

- [Documentation](https://docs.memanto.ai)
- [CLI Reference](https://docs.memanto.ai/cli/overview)
- [Claude Code Integration](https://docs.memanto.ai/integrations/claude-code)
- [Memory Types Reference](https://docs.memanto.ai/reference/memory-types)
