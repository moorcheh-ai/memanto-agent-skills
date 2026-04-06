# MEMANTO Agent Skills — Setup Guide

This repository provides agent skills for giving AI agents persistent memory via MEMANTO.

## Prerequisites

- Python 3.10+
- A [Moorcheh](https://console.moorcheh.ai) account
- `MOORCHEH_API_KEY` environment variable set

## Quick Setup

```bash
# Install MEMANTO CLI
pip install memanto

# Set your API key
export MOORCHEH_API_KEY="your-api-key"

# Create and activate an agent
memanto agent create my-agent
memanto agent activate my-agent
```

## Skills in this Repository

| Skill | Description |
|-------|-------------|
| [memanto](skills/memanto/SKILL.md) | Core memory operations — remember, recall, answer, session management |
| [memanto-cookbooks](skills/memanto-cookbooks/SKILL.md) | Blueprints for memory-powered AI applications |

## Key Commands

```bash
# Store a memory
memanto remember "content" --type fact --confidence 0.9 --provenance explicit_statement --source agent_name

# Search memories
memanto recall "query"

# Ask a question (RAG)
memanto answer "question"

# Sync memories to MEMORY.md
memanto memory sync --project-dir .

# View session info
memanto session info
```

## Memory Types

`fact` · `decision` · `preference` · `instruction` · `goal` · `commitment` · `artifact` · `learning` · `event` · `relationship` · `observation` · `error` · `context`

## Resources

- [Documentation](https://docs.moorcheh.ai)
- [Agent Integration Guide](https://docs.moorcheh.ai/agent-integration)
- [CLI User Guide](https://docs.moorcheh.ai/cli)
