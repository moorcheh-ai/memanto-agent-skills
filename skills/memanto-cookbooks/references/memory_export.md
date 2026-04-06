# Cookbook: Memory Export & Audit

Export, visualize, and audit all agent memories. Understand what your agent knows, clean up stale memories, and share knowledge snapshots with teammates.

## Export to Markdown

```bash
# Export to MEMORY.md in the current directory
memanto memory sync --project-dir .

# Export to a specific directory
memanto memory sync --project-dir /path/to/project

# Export with format options
memanto memory export --format markdown --output ./reports/memory-snapshot.md
```

## View All Memories by Type

```bash
# Instructions
memanto recall "." --type instruction --limit 50

# All decisions
memanto recall "." --type decision --limit 50

# All commitments
memanto recall "." --type commitment --limit 50

# High-confidence facts
memanto recall "." --type fact --min-confidence 0.9 --limit 50
```

## Timeline Visualization

```bash
# View memory timeline (recent activity)
memanto recall "session summary" --type context --limit 30

# See what changed recently
memanto recall "." --changed-since "7d ago"

# Historical state (what did we know last week?)
memanto recall "." --as-of "7d ago" --limit 20
```

## Audit by Confidence

```bash
# Find low-confidence memories (candidates for review or deletion)
memanto recall "." --max-confidence 0.7 --limit 50

# Find memories that may be stale (old observations)
memanto recall "." --type observation --as-of "30d ago" --limit 20
```

## Tag-Based Audit

```bash
# Find all memories tagged with a specific area
memanto recall "authentication oauth" --tags "auth"

# Find memories referencing a specific commit
memanto recall "commit-abc123"

# Find all "todo" commitments
memanto recall "todo" --type commitment
```

## Memory Quality Review

Run this periodic audit to keep memory healthy:

```bash
# 1. Review all commitments — are they still open?
memanto recall "." --type commitment --limit 20

# 2. Check for contradictions
memanto conflicts

# 3. Review old observations (may be stale)
memanto recall "." --type observation --as-of "14d ago" --limit 20

# 4. Sync updated MEMORY.md
memanto memory sync --project-dir .
```

## Share Memory Snapshot

To share memory context with a teammate or another agent:

```bash
# Generate a clean markdown export
memanto memory sync --project-dir .

# Commit MEMORY.md to the repo
git add MEMORY.md
git commit -m "chore: update agent memory snapshot for handoff"
```

The teammate's agent can read `MEMORY.md` at session start to have instant context about the project.

## Export for Reporting

```bash
# Generate a weekly summary report
memanto answer "Summarize all decisions made this week."
memanto answer "What commitments were completed this week?"
memanto answer "What errors or bugs did we encounter and resolve?"
```
