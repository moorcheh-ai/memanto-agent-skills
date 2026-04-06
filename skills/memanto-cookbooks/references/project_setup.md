# Project Setup Contract

Before building any MEMANTO-powered application, complete this setup checklist.

## Required

- [ ] Python 3.10+ installed
- [ ] `MOORCHEH_API_KEY` environment variable set
- [ ] MEMANTO CLI installed: `pip install memanto`
- [ ] Agent created: `memanto agent create <project-name>`
- [ ] Session active: `memanto agent activate <project-name>`

## Verify Setup

```bash
# Check CLI is installed
memanto --version

# Check API key is configured
memanto config show

# Check active session
memanto session info

# Run a test store + recall
memanto remember "Project setup verified." --type fact --confidence 1.0 \
  --provenance explicit_statement --source setup --tags "setup,test"
memanto recall "project setup"
```

## Project Structure (Recommended)

```
my-project/
├── MEMORY.md           # Auto-synced by MEMANTO (read-only by humans)
├── .env                # MOORCHEH_API_KEY (gitignored)
├── .gitignore
└── src/
    └── ...
```

`.gitignore` entries:
```
.env
# Optional: ignore MEMORY.md if you don't want to commit it
# MEMORY.md
```

## Connect to Your Agent

```bash
# Claude Code
memanto connect claude-code

# Cursor
memanto connect cursor

# Codex
memanto connect codex

# All agents
memanto connect --list    # See all supported agents
```
