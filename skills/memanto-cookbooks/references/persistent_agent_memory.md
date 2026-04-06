# Cookbook: Persistent Agent Memory

Give any AI agent long-term memory that persists across sessions, restarts, and new conversations.

## Overview

This cookbook covers the full lifecycle of an agent with persistent memory:
1. Create agent identity
2. Activate session
3. Load context at session start
4. Store memories proactively during work
5. End session with a context snapshot
6. Resume the next day with full continuity

## Prerequisites

See [environment_requirements.md](environment_requirements.md) and [project_setup.md](project_setup.md).

## Step 1: Create Agent Identity (One Time)

```bash
memanto agent create my-project --pattern tool
```

The `--pattern` hint is optional but improves bootstrap intelligence:
- `tool` — Coding assistant, file editor, CLI tool
- `chat` — Conversational assistant
- `research` — Research and analysis agent

## Step 2: Session Start Protocol

Run this at the beginning of every work session:

```bash
# 1. Activate session
memanto agent activate my-project

# 2. Sync MEMORY.md to project root
memanto memory sync --project-dir .

# 3. Load standing context
memanto recall "instructions decisions goals" --limit 20

# 4. Check open commitments
memanto answer "What are my pending commitments?"

# 5. (If resuming work) Load recent context
memanto recall "session context status" --type context --limit 3
```

## Step 3: Store Memories Proactively

Store important information as it comes up — don't wait until the end.

### User states a preference
```bash
memanto remember "User prefers tabs over spaces for indentation." \
  --type preference --confidence 1.0 --provenance explicit_statement \
  --source claude_code --tags "formatting,indentation,style"
```

### Architecture decision made
```bash
memanto remember "Chose FastAPI over Flask for the REST API. Reason: native async, automatic OpenAPI docs. Decision: 2025-03-15." \
  --type decision --confidence 0.95 --provenance explicit_statement \
  --source claude_code --tags "fastapi,flask,architecture,rest-api"
```

### Bug fixed, lesson learned
```bash
memanto remember "Namespace names in Moorcheh must use underscores, not hyphens. ConflictError otherwise. Fixed in commit abc123." \
  --type error --confidence 1.0 --provenance observed \
  --source claude_code --tags "namespace,moorcheh,naming,bug-fix"
```

### Commitment made
```bash
memanto remember "Will add input validation to /api/v1/remember endpoint before next PR review." \
  --type commitment --confidence 1.0 --provenance explicit_statement \
  --source claude_code --tags "validation,api,todo,pr-review"
```

## Step 4: Session End Protocol

Before ending a session, store a context snapshot:

```bash
memanto remember "Session 2025-03-15: Implemented agent activation endpoint. Added JWT session management. Fixed namespace naming bug. Next: add batch memory write endpoint. 60% of Phase 2 complete." \
  --type context --confidence 0.9 --provenance observed \
  --source claude_code --tags "session-summary,2025-03-15,phase-2"

# Sync MEMORY.md for next session
memanto memory sync --project-dir .
```

## Step 5: Resume Next Session

Picking up exactly where you left off:

```bash
memanto agent activate my-project
memanto recall "session context" --type context --limit 1
memanto answer "What were we working on and what's next?"
```

## Connecting to Your Agent

To automate the session start protocol:

```bash
memanto connect claude-code   # Injects MEMORY.md sync hook + instructions into CLAUDE.md
memanto connect cursor        # Injects Cursor rules
memanto connect codex         # Injects AGENTS.md instructions
```

## Full Python Example

```python
import asyncio
from memanto.cli.client.sdk_client import SdkClient

async def main():
    client = SdkClient()

    # Activate session
    await client.activate_session("my-project")

    # Load context (recall recent decisions)
    memories = await client.recall("database architecture decisions", limit=5)
    for mem in memories:
        print(f"[{mem['type']}] {mem['content'][:80]}")

    # Store a new memory
    await client.remember(
        content="Implemented Redis caching layer. Cache hit rate: 85%.",
        memory_type="fact",
        confidence=0.9,
        provenance="observed",
        source="my_agent",
        tags=["redis", "caching", "performance"],
    )

asyncio.run(main())
```
