---
description: Show MEMANTO health — config, session, agents, memory counts
allowed-tools: Bash(memanto:*)
disable-model-invocation: true
---

Report the current state of MEMANTO.

```bash
memanto status
```

This covers environment, backend, configuration, the active session, and registered agents in
one pass. For a deeper look at what the active agent actually knows:

```bash
memanto agent bootstrap        # intelligence snapshot of the agent's memory
memanto recall --recent --limit 10
```

Summarize for the user:

1. Is MEMANTO configured and is an agent active?
2. How much does this agent remember, and what are the dominant themes?
3. Anything needing attention — no active agent, unresolved conflicts, a large expired backlog.

If MEMANTO is not configured, walk them through `/memanto:quickstart` rather than dumping the
raw error.
