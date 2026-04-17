# MEMANTO — Persistent Memory for AI Agents

MEMANTO is a universal memory layer that gives AI agents long-term, persistent memory across sessions. Built on Moorcheh's semantic database, it provides zero-cost ingestion latency, instant recall, and a rich taxonomy of memory types with trust scoring.

## Key Capabilities

**Agent & Session Management** allows creating named agent identities, activating sessions with JWT tokens, maintaining continuity across restarts, and deleting agents. Deletion removes local metadata and prompts whether to also purge the Moorcheh cloud namespace.

**File Upload** ingests documents (.pdf, .docx, .xlsx, .json, .txt, .csv, .md) directly into the agent's memory namespace. Uploaded content is processed, embedded, and immediately searchable via recall and answer.

**Memory Storage** supports 13 distinct memory types — from facts and decisions to errors and commitments — each with confidence scoring and provenance tracking to prevent memory poisoning.

**Semantic Recall** enables querying all stored memories using natural language, with filtering by type, confidence threshold, time range, and tags.

**RAG Answers** generates grounded natural-language responses by retrieving relevant memories and synthesizing them into coherent answers.

**Memory Sync** exports the full memory snapshot to `MEMORY.md` in the project root, ensuring agents always start with full context.

**Daily Summaries** auto-generates compressed digests of recent activity, reducing context overhead for long-running agents.

## Getting Started

Users need a Moorcheh account with an API key. Create a free account at [console.moorcheh.ai](https://console.moorcheh.ai).

See [environment_requirements.md](references/environment_requirements.md) for full setup instructions.

### First-Time Setup

```bash
pip install memanto
export MOORCHEH_API_KEY="your-api-key"
memanto config set api-key YOUR_KEY
memanto agent create my-agent
memanto agent activate my-agent
```

### Session Start Pattern

```bash
memanto memory sync --project-dir .   # Populate MEMORY.md
memanto recall "instructions decisions goals" --limit 20
memanto answer "What are my pending commitments?"
```

## Usage Notes

**Memory Types Decision Matrix:**

| Type | When to Use | Confidence | Example |
|------|-------------|------------|---------|
| `fact` | Verified information, project status | 0.9–1.0 | "API uses PostgreSQL for metadata" |
| `decision` | Architecture choices, approach selections | 0.9–1.0 | "Chose React over Vue for frontend" |
| `instruction` | Standing rules, preferences, guidelines | 0.9–1.0 | "Always use type hints in Python" |
| `commitment` | Promises, TODOs, obligations | 1.0 | "Will deploy monitoring by Friday" |
| `preference` | User/team preferences | 0.8–1.0 | "User prefers dark mode" |
| `goal` | Objectives, targets, milestones | 0.8–1.0 | "Launch CLI by end of March" |
| `artifact` | Tool outputs, reports, file locations | 0.9–1.0 | "Report saved at ./reports/q1.md" |
| `learning` | Knowledge acquired from experience | 0.7–0.9 | "Batch operations 100x faster" |
| `event` | Important conversations, milestones | 0.8–0.95 | "Completed Phase 1 features" |
| `relationship` | Team context, collaboration patterns | 0.85–0.95 | "Alice is lead backend engineer" |
| `observation` | Patterns noticed, behaviors | 0.6–0.85 | "User prefers short responses" |
| `error` | Failures, bugs, lessons learned | 0.95–1.0 | "Namespace format bug — use underscores" |
| `context` | Session summaries, status updates | 0.9–1.0 | "Project 70% done, API complete" |

**Confidence Levels:**
- `1.0` — Explicit user statement, verified fact, standing instruction
- `0.9–0.95` — Strong consensus, well-tested approach
- `0.8–0.85` — Observed pattern (3+ times)
- `0.7–0.75` — Emerging pattern (2 times), reasonable inference
- `0.6–0.65` — Single observation, uncertain
- `< 0.6` — Do NOT store. Too uncertain.

**Provenance Types:** `explicit_statement` · `inferred` · `observed` · `corrected` · `validated`

Common errors relate to missing API keys, expired sessions (re-run `memanto agent activate`), and missing agent IDs. See individual reference files for details.
