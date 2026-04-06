# Daily Summary — Automated Memory Digests

MEMANTO can generate compressed daily summaries of recent agent activity and store them as memory. This reduces context overhead in long-running projects.

## Enable Scheduling

```bash
# Enable daily summary at 23:59 local time
memanto schedule enable

# Check schedule status
memanto schedule status

# Disable
memanto schedule disable
```

## Manual Trigger

Generate a daily summary immediately:

```bash
memanto daily-summary
memanto daily-summary --agent my-agent   # For a specific agent
```

## What Gets Summarized

The daily summary service compresses:
- All memories stored that day
- Key decisions made
- Commitments added or completed
- Errors encountered and resolved
- Significant events

The result is stored as a `context` memory with high confidence:

```
Session summary 2025-03-15:
- Implemented batch memory writes (performance: 100x improvement)
- Decided on Redis for caching
- Fixed OAuth expiry bug in auth.py
- Commitment added: rate limiting before v0.2
- 4 new facts stored about deployment config
```

## Reading Daily Summaries

```bash
# Recall recent summaries
memanto recall "daily summary" --type context --limit 7

# Get a synthesized weekly review
memanto answer "What did we accomplish this week?"
```

## Schedule File

The schedule is stored at `~/.memanto/schedule.json`:

```json
{
  "enabled": true,
  "time": "23:55",
  "agent_id": "my-agent",
  "last_run": "2025-03-14T23:55:00Z",
  "next_run": "2025-03-15T23:55:00Z"
}
```

## Implementation Notes

The schedule manager uses a background process. On systems where background processes are not persistent (e.g., serverless), use a cron job instead:

```bash
# crontab entry
55 23 * * * /usr/local/bin/memanto daily-summary --agent my-agent
```
