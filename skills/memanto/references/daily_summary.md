# Daily Summary — Automated Memory Digests

MEMANTO can generate compressed daily summaries of recent agent activity and store them as memory. This reduces context overhead in long-running projects.

## Enable Scheduling

```bash
memanto schedule enable    # enable the nightly job
memanto schedule status    # check it
memanto schedule disable   # turn it off
```

The nightly job is not just the summary. One run does three things:

1. **Daily summary** — compresses the day's memories into a `context` memory
2. **Conflict detection** — flags contradictions for review (see [conflicts.md](conflicts.md))
3. **Expiry sweep** — retires memories your policy matches (see [expiry_policy.md](expiry_policy.md))

Set your expiry policy deliberately *before* enabling the schedule — the nightly sweep does not
stop to ask. `memanto policy show` reports what is currently in force.

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

## Implementation Notes

The schedule manager runs a background process. Where background processes do not persist
(containers, serverless, CI), drive it from cron instead:

```bash
# crontab entry — nightly summary for a specific agent
55 23 * * * /usr/local/bin/memanto daily-summary --agent my-agent
```

Check `memanto schedule status` to confirm the job is actually registered rather than assuming
`enable` succeeded.
