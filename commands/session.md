---
description: Show or switch the active MEMANTO agent session
argument-hint: [agent-id]
allowed-tools: Bash(memanto:*)
disable-model-invocation: true
---

Manage the MEMANTO agent session. Target agent (may be empty): `$ARGUMENTS`

**If an agent id was given**, activate it:

```bash
memanto agent activate $ARGUMENTS
```

Add `--hours <n>` for a non-default lifetime (default 6). If the agent does not exist yet,
`memanto agent create $ARGUMENTS` creates **and** activates it in one step.

**If no agent id was given**, report the current state:

```bash
memanto session info
memanto agent list
```

Then summarize: which agent is active, how long the session has left, and what other agents
exist.

Notes:

- `memanto agent create <id>` activates immediately — there is no separate activate step for a
  brand-new agent.
- Sessions **auto-renew** by default, so an expired token usually recovers on its own. If a
  command still reports no active session, re-run `memanto agent activate <id>`.
- `memanto agent deactivate` ends the current session and takes **no** agent argument.
- Only one agent is active at a time.
