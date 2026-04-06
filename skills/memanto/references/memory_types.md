# Memory Types Reference

MEMANTO supports 13 distinct memory types. Choose the most specific type that fits — this improves retrieval precision and confidence calibration.

## Complete Reference

### `fact`
**Confidence:** 0.9–1.0 | **Provenance:** `explicit_statement` or `validated`

Verified, objective information about the project, codebase, or environment. Use for things that are known to be true.

```bash
memanto remember "The API runs on Python 3.11 with FastAPI 0.104. Deployed on AWS ECS." \
  --type fact --confidence 0.95 --provenance explicit_statement --source claude_code \
  --tags "api,python,deployment,aws"
```

---

### `decision`
**Confidence:** 0.9–1.0 | **Provenance:** `explicit_statement`

Architectural choices, approach selections, or deliberate direction changes. Always include the reasoning and date.

```bash
memanto remember "Chose Redis for session caching over in-memory store. Reason: horizontal scaling required. Decision: 2025-03-10." \
  --type decision --confidence 0.95 --provenance explicit_statement --source claude_code \
  --tags "redis,caching,session,architecture"
```

---

### `instruction`
**Confidence:** 0.9–1.0 | **Provenance:** `explicit_statement`

Standing rules, guidelines, or conventions that must be followed consistently.

```bash
memanto remember "Always add type hints to all Python functions. No bare 'except' clauses. Use ruff for formatting." \
  --type instruction --confidence 1.0 --provenance explicit_statement --source claude_code \
  --tags "python,style,type-hints,ruff"
```

---

### `commitment`
**Confidence:** 1.0 | **Provenance:** `explicit_statement`

Promises made, TODOs agreed upon, or obligations. Always store at confidence 1.0.

```bash
memanto remember "Will add rate limiting to /api/v1/search before the v0.2 release. Agreed with team on 2025-03-12." \
  --type commitment --confidence 1.0 --provenance explicit_statement --source claude_code \
  --tags "rate-limiting,api,todo,v0.2"
```

---

### `preference`
**Confidence:** 0.8–1.0 | **Provenance:** `explicit_statement` or `observed`

User or team preferences for tools, styles, formats, or workflows.

```bash
memanto remember "User prefers concise responses without bullet points unless explicitly asked." \
  --type preference --confidence 1.0 --provenance explicit_statement --source claude_code \
  --tags "communication,style,response-format"
```

---

### `goal`
**Confidence:** 0.8–1.0 | **Provenance:** `explicit_statement`

Project objectives, milestones, targets, or aspirations.

```bash
memanto remember "Goal: Ship MEMANTO v0.2 with multi-agent support by end of April 2025." \
  --type goal --confidence 0.95 --provenance explicit_statement --source claude_code \
  --tags "roadmap,v0.2,deadline,multi-agent"
```

---

### `artifact`
**Confidence:** 0.9–1.0 | **Provenance:** `observed`

Generated outputs, file locations, reports, or tool outputs worth referencing later.

```bash
memanto remember "Architecture diagram saved at ./docs/architecture-v2.png. Updated 2025-03-14." \
  --type artifact --confidence 0.95 --provenance observed --source claude_code \
  --tags "architecture,diagram,docs"
```

---

### `learning`
**Confidence:** 0.7–0.9 | **Provenance:** `observed` or `inferred`

Knowledge gained through experience, debugging, or experimentation. Not yet a formal decision.

```bash
memanto remember "Storing 100 memories in a batch is ~100x faster than individual calls. Use batch_store_memories() for bulk imports." \
  --type learning --confidence 0.85 --provenance observed --source claude_code \
  --tags "performance,batch,memory-write"
```

---

### `event`
**Confidence:** 0.8–0.95 | **Provenance:** `observed`

Important conversations, milestones, or occurrences worth remembering.

```bash
memanto remember "Completed Phase 1: CLI + REST API. Demo with stakeholders on 2025-03-15. Approved for Phase 2." \
  --type event --confidence 0.9 --provenance observed --source claude_code \
  --tags "milestone,phase-1,demo,approval"
```

---

### `relationship`
**Confidence:** 0.85–0.95 | **Provenance:** `explicit_statement`

Team structure, responsibilities, or collaboration context.

```bash
memanto remember "Alice is lead backend engineer. Bob owns the frontend. Majid is the product owner." \
  --type relationship --confidence 0.9 --provenance explicit_statement --source claude_code \
  --tags "team,roles,org-structure"
```

---

### `observation`
**Confidence:** 0.6–0.85 | **Provenance:** `inferred` or `observed`

Patterns noticed, behavioral tendencies, or emerging signals. Lower confidence; not yet confirmed.

```bash
memanto remember "User tends to ask for implementation first, then tests. Rarely asks for docs upfront." \
  --type observation --confidence 0.7 --provenance inferred --source claude_code \
  --tags "user-pattern,workflow,testing"
```

---

### `error`
**Confidence:** 0.95–1.0 | **Provenance:** `observed`

Failures, bugs, wrong approaches, or lessons learned from mistakes. Always include how it was resolved.

```bash
memanto remember "Namespace names must use underscores. Hyphens cause ConflictError on create. Fixed by renaming memanto-agent-x to memanto_agent_x." \
  --type error --confidence 1.0 --provenance observed --source claude_code \
  --tags "namespace,bug,moorcheh,naming"
```

---

### `context`
**Confidence:** 0.9–1.0 | **Provenance:** `observed`

Session summaries or status snapshots that capture where things stand.

```bash
memanto remember "Session 2025-03-15: Implemented batch memory writes. API v2 complete. Next: add daily summaries. 70% of Phase 2 done." \
  --type context --confidence 0.9 --provenance observed --source claude_code \
  --tags "session-summary,phase-2,progress"
```
