# Memory Best Practices

Effective memory usage is the difference between an agent that grows smarter over time and one that accumulates noise. Follow these guidelines.

## The Golden Rules

### 1. Recall Before Storing

Always search before storing to avoid duplicates:

```bash
memanto recall "topic you're about to store"
```

If a similar memory exists, consider whether to update it instead of creating a new one.

### 2. Be Specific, Not Vague

| Bad | Good |
|-----|------|
| "better performance" | "API response time < 200ms after Redis caching. Commit abc123." |
| "fixed bug" | "Fixed OAuth token expiry bug in auth.py:145. Tokens now refresh 5min before expiry." |
| "user likes clean code" | "User prefers functions < 20 lines. Extract helpers aggressively." |
| "decided on database" | "Chose PostgreSQL 15 over SQLite. Reason: need JSONB and full-text search. Decision 2025-03-10." |

### 3. Always Include Context

Good memories are self-contained. Include:
- **What** happened or was decided
- **Why** (the reasoning or motivation)
- **When** (date or commit reference if relevant)
- **Where** (file path, PR, issue number if applicable)

### 4. Tag for Retrieval

Tags are the primary way memories are found in broad searches. Use 2–5 tags per memory.

```bash
# Good: specific, lowercase, hyphenated
--tags "oauth,session-tokens,auth-middleware,commit-abc123"

# Bad: generic, useless
--tags "important,code,stuff"
```

### 5. Calibrate Confidence Honestly

| Score | Meaning |
|-------|---------|
| 1.0 | Explicit user statement, verified fact, standing instruction |
| 0.9–0.95 | Strong consensus, tested, clear preference |
| 0.8–0.85 | Observed 3+ times, indirect but supported |
| 0.7–0.75 | Seen twice, reasonable inference |
| 0.6–0.65 | Single observation, uncertain |
| < 0.6 | Don't store. Too uncertain. |

### 6. Store Immediately, Not Later

Don't batch up memories to store at the end. Store important information the moment you encounter it:

```bash
# User just said: "I always prefer functional components over class components in React"
memanto remember "User prefers functional components over class components in React. Always." \
  --type preference --confidence 1.0 --provenance explicit_statement --source claude_code \
  --tags "react,components,functional,style"
```

### 7. Mark Corrections with `corrected` Provenance

When the user corrects you or contradicts a previous memory:

```bash
memanto remember "CORRECTION: User prefers pytest NOT unittest. Previous preference was wrong." \
  --type learning --confidence 1.0 --provenance corrected --source claude_code \
  --tags "testing,pytest,correction"
```

## Pitfalls to Avoid

1. **Memory hoarding** — Only store what will matter in a future session. Ask: "Would I want this in my context next week?"

2. **Duplicate memories** — Always recall first. Duplicates dilute search quality.

3. **Missing provenance** — Always set `--provenance`. It drives confidence calibration.

4. **Wrong memory type** — A "decision" stored as "fact" loses its retrieval context. Be precise.

5. **No tags** — Untagged memories are nearly invisible to recall queries.

6. **Stale commitments** — When a commitment is fulfilled, store a new memory noting completion:
   ```bash
   memanto remember "COMPLETED: Rate limiting added to /api/v1/search in PR #42. Commitment fulfilled." \
     --type event --confidence 1.0 --provenance observed --source claude_code \
     --tags "rate-limiting,api,completed,pr-42"
   ```

## Session Start Protocol

```bash
# 1. Sync MEMORY.md
memanto memory sync --project-dir .

# 2. Load instructions and standing context
memanto recall "instructions decisions goals" --limit 20

# 3. Check open commitments
memanto answer "What are my pending commitments?"

# 4. If returning to ongoing work
memanto recall "current work session context" --type context --limit 3
```

## Session End Protocol

```bash
# Store a context memory summarizing the session
memanto remember "Session YYYY-MM-DD: [what was accomplished]. Next: [what's next]. Status: [project status]." \
  --type context --confidence 0.9 --provenance observed --source claude_code \
  --tags "session-summary,YYYY-MM-DD"

# Sync MEMORY.md for next session
memanto memory sync --project-dir .
```

## Memory Quality Checklist

Before storing, verify:
- [ ] Content is specific and actionable (not vague)
- [ ] Type matches the nature of the memory
- [ ] Confidence reflects actual certainty
- [ ] Provenance is accurate
- [ ] 2–5 relevant tags included
- [ ] Source is set to your agent name
- [ ] No duplicate exists in memory (checked with `recall`)
