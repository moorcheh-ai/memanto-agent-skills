# Cookbook: Session Continuity

Resume exactly where you left off across sessions, restarts, and new conversations. Never lose context again.

## The Problem

AI agents lose all context when a session ends. Tomorrow's session starts blank — no memory of decisions made, preferences stated, or work done. MEMANTO solves this.

## The Solution

MEMANTO maintains a persistent memory store that:
1. Survives session restarts
2. Is always searchable via semantic recall
3. Is exported to `MEMORY.md` for instant context loading
4. Summarizes recent activity via daily digests

## Session Continuity Protocol

### End of Session

```bash
# Store a session summary (the most important step)
memanto remember "Session 2025-03-15: [What was accomplished]. [Key decisions made]. [What's next]. [Blockers if any]. Phase X: Y% complete." \
  --type context --confidence 0.9 --provenance observed \
  --source claude_code --tags "session-summary,$(date +%Y-%m-%d)"

# Mark completed commitments
memanto remember "COMPLETED: Rate limiting added to /api/v1/search. PR #42 merged." \
  --type event --confidence 1.0 --provenance observed \
  --source claude_code --tags "completed,rate-limiting,pr-42"

# Sync MEMORY.md for next session
memanto memory sync --project-dir .
```

### Start of Next Session

```bash
# Activate session
memanto agent activate my-project

# Sync MEMORY.md (also done automatically if hook is set up)
memanto memory sync --project-dir .

# Load where we left off
memanto recall "session summary" --type context --limit 1

# Load all standing instructions
memanto recall "instructions" --type instruction --limit 10

# Check open commitments
memanto answer "What are my pending commitments?"

# Check goals
memanto answer "What are the current project goals?"
```

## MEMORY.md as Cold-Start Snapshot

`MEMORY.md` is the primary mechanism for instant context loading. It's a structured markdown file that the agent reads before doing any work.

The file is populated by `memanto memory sync` and contains:
- All standing instructions
- Active goals and commitments
- Recent decisions
- Key facts about the project
- Latest context summary

The agent MUST read this file at the start of every session.

## Session Token Lifecycle

```
Activate (6h default)
    ↓
Work (memories stored continuously)
    ↓
Extend if needed: memanto session extend --hours 4
    ↓
Session expires → re-activate: memanto agent activate my-project
    ↓
All memories persist — only the auth token expires
```

## Daily Summary for Long-Running Projects

For projects spanning weeks or months, enable automated daily summaries:

```bash
# Enable daily summary at 23:59 local time
memanto schedule enable

# Manual daily summary
memanto daily-summary

# Read last 7 days
memanto recall "daily summary" --type context --limit 7

# Weekly review
memanto answer "What did we accomplish this week?"
```

## Tracking Commitments to Completion

```bash
# Store commitment
memanto remember "Will add integration tests for auth endpoints by end of sprint." \
  --type commitment --confidence 1.0 --provenance explicit_statement \
  --source claude_code --tags "testing,auth,sprint,todo"

# When complete, mark it
memanto remember "COMPLETED: Auth endpoint integration tests added in tests/test_api.py. All passing. Commit def456." \
  --type event --confidence 1.0 --provenance observed \
  --source claude_code --tags "completed,testing,auth,commit-def456"
```

## Handling Interruptions

If work is interrupted mid-task:

```bash
memanto remember "INTERRUPTED: Mid-way through refactoring memory_write_service.py. Extracted store_memory() but batch_store_memories() not yet updated. Resume from line 85." \
  --type context --confidence 0.95 --provenance observed \
  --source claude_code --tags "interrupted,refactor,memory-write,resume-point"
```

Next session:
```bash
memanto recall "interrupted resume" --type context --limit 3
```
