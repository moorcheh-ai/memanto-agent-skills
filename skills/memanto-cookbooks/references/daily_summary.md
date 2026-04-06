# Cookbook: Daily Summary Automation

Automatically generate compressed daily digests of agent activity. Reduce context overhead and make long project histories navigable.

## Enable Automatic Summaries

```bash
# Enable daily summary at 23:59 local time
memanto schedule enable

# Check status
memanto schedule status

# Disable
memanto schedule disable
```

## Manual Trigger

```bash
# Generate now (uses active agent)
memanto daily-summary

# For a specific agent
memanto daily-summary --agent my-project
```

## What Gets Summarized

The daily summary service compresses all activity from the day into a single `context` memory:

```
Daily Summary 2025-03-15:

COMPLETED:
- Implemented JWT session management
- Fixed namespace naming bug (hyphens → underscores)
- Added batch memory write endpoint

DECISIONS:
- Chose Redis for session caching (horizontal scaling)

COMMITMENTS ADDED:
- Add rate limiting to /api/v1/search before v0.2

FACTS LEARNED:
- Batch store is 100x faster than individual stores

STATUS: Phase 2 — 65% complete
```

## Reading Summaries

```bash
# Read last 7 daily summaries
memanto recall "daily summary" --type context --limit 7

# Weekly review
memanto answer "What did we accomplish this week?"

# Monthly trend
memanto answer "What major decisions did we make this month?"
```

## Cron Job Alternative

For systems where background processes are not persistent:

```bash
# Linux/macOS crontab
crontab -e
# Add:
55 23 * * * /usr/local/bin/memanto daily-summary my-project >> ~/.memanto/logs/daily-summary.log 2>&1
```

```bash
# Windows Task Scheduler (PowerShell)
$Action = New-ScheduledTaskAction -Execute "memanto" -Argument "daily-summary my-project"
$Trigger = New-ScheduledTaskTrigger -Daily -At "23:55"
Register-ScheduledTask -TaskName "MenantoDaily" -Action $Action -Trigger $Trigger
```

## Schedule Configuration

Stored at `~/.memanto/schedule.json`:

```json
{
  "enabled": true,
  "time": "23:55",
  "agent_id": "my-project",
  "timezone": "local",
  "last_run": "2025-03-14T23:55:00Z",
  "next_run": "2025-03-15T23:55:00Z"
}
```

## Integration with Session Protocol

Use the daily summary as the primary context loader:

```bash
# At session start (instead of manually recalling everything)
memanto recall "daily summary" --type context --limit 3   # Last 3 days
memanto answer "What are my pending commitments?"
```

This gives you a compressed view of recent history without overwhelming the context window.
