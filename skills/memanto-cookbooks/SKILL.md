---
name: memanto-cookbooks
description: End-to-end blueprints for building memory-powered applications on MEMANTO — persistent agent memory, session continuity, memory export and audit, automated daily digests, conflict resolution, and memory-grounded RAG. Use when designing or scaffolding a project that needs agent memory, not for one-off remember/recall calls.
license: MIT
---

# MEMANTO Cookbooks — Memory-Powered Application Blueprints

Production-ready blueprints for building AI applications on MEMANTO. Each cookbook covers
architecture, setup, and working code for one complete use case.

For day-to-day memory operations (`remember`, `recall`, `answer`), use the **memanto** skill
instead. Reach for a cookbook when you are standing up a new memory-backed project or wiring
memory into an existing one.

## Prerequisites

A free Moorcheh account ([console.moorcheh.ai](https://console.moorcheh.ai)) and the CLI:

```bash
pip install memanto
memanto                    # interactive setup, stores the API key
memanto agent create my-project
```

Then review:
- [Project Setup](references/project_setup.md)
- [Environment Requirements](references/environment_requirements.md)

## Available Cookbooks

### 1. [Persistent Agent Memory](references/persistent_agent_memory.md)
End-to-end setup for an agent with long-term memory across sessions. Agent creation, session
lifecycle, the session-start recall pattern, proactive storage, and MEMORY.md sync. **Start here** —
the other cookbooks build on it.

### 2. [Session Continuity](references/session_continuity.md)
Resume exactly where you left off across restarts. Session token lifecycle and auto-renewal,
MEMORY.md as the cold-start snapshot, commitment tracking, and context summarization.

### 3. [Memory Export & Audit](references/memory_export.md)
Export, visualize, and audit everything an agent knows. Markdown and OKF bundle export,
confidence filtering, tag-based audits, and reversible pruning via expiry policy.

### 4. [Daily Summary Automation](references/daily_summary.md)
Automated nightly digests. The scheduled job covers daily summary, conflict detection, and the
expiry sweep in one pass.

### 5. [Memory-Powered RAG](references/memory_rag.md)
Question answering grounded in agent memory. The `memanto answer` pipeline, context window
management, and citation tracking.

### 6. [Conflict Resolution](references/conflict_resolution.md)
Detect and resolve contradictory memories before they poison retrieval. LLM-based detection,
interactive resolution, and correction provenance.

### 7. [Migrating from Another Provider](references/migration.md)
Move existing memory into MEMANTO from Mem0, Letta, Supermemory, Langfuse, or an OKF bundle,
and verify the import.
