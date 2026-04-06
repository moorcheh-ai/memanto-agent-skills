# MEMANTO Cookbooks — Memory-Powered AI Application Blueprints

MEMANTO Cookbooks provides complete implementation guides for building AI applications with persistent memory. Each cookbook is a production-ready blueprint covering architecture, setup, and working code.

## Account Setup

Users without an account should register at [console.moorcheh.ai](https://console.moorcheh.ai) to create a free Moorcheh account and obtain an API key.

## Prerequisites

Before starting any cookbook project, review:
- [Project Setup](references/project_setup.md)
- [Environment Requirements](references/environment_requirements.md)

## Available Cookbooks

### 1. [Persistent Agent Memory](references/persistent_agent_memory.md)
Full end-to-end setup for an AI agent with long-term memory across sessions. Covers agent creation, session management, the session-start recall pattern, proactive memory storage, and MEMORY.md sync. The foundation for all other cookbooks.

### 2. [Session Continuity](references/session_continuity.md)
How to resume exactly where you left off across sessions and agent restarts. Covers session token lifecycle, MEMORY.md as the cold-start snapshot, commitment tracking, and context summarization.

### 3. [Memory Export & Audit](references/memory_export.md)
Export, visualize, and audit all agent memories. Covers markdown export, timeline visualization, confidence filtering, tag-based audits, and memory pruning.

### 4. [Daily Summary Automation](references/daily_summary.md)
Set up automated daily memory digests on a schedule. Covers cron-based scheduling, the daily summary service, summary content structure, and reading summaries in context.

### 5. [Memory-Powered RAG](references/memory_rag.md)
Build a question-answering system grounded in agent memory. Covers the `memanto answer` RAG pipeline, context window management, and citation tracking.
