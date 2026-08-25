---
description: Set up MEMANTO for this project, end to end
allowed-tools: Bash(memanto:*), Bash(pip install memanto), Read
disable-model-invocation: true
---

Walk the user through MEMANTO setup for this project. Run each step, check the result before
moving on, and stop to ask if a step fails.

**1 — Is the CLI installed?**

```bash
memanto status
```

If the command is not found, install it: `pip install memanto` (Python 3.10–3.12 required).

**2 — Is it configured?**

`memanto status` reports configuration state. If there is no API key, the user needs one from
[console.moorcheh.ai](https://console.moorcheh.ai) (free). They then set it **either** by
exporting `MOORCHEH_API_KEY`, **or** by running bare `memanto`, which starts an interactive
setup wizard and writes the key to `~/.memanto/.env`.

The wizard is interactive, so **ask the user to run `memanto` themselves** in their terminal —
type `! memanto` in this session and the output lands right here. Do not try to drive an
interactive prompt through a tool call.

**3 — Create the agent.**

Name it after this project. Check `memanto agent list` first in case one already exists.

```bash
memanto agent create <project-name>
```

This creates **and** activates the agent — there is no separate activation step.

**4 — Verify the round trip.**

```bash
memanto remember "MEMANTO configured for this project." \
  --type context --confidence 1.0 --provenance explicit_statement \
  --source claude_code --tags "setup,onboarding"

memanto recall "setup" --limit 5
memanto answer "Is MEMANTO set up for this project?"
```

All three must succeed. If recall returns nothing, stop and diagnose before continuing.

**5 — Populate MEMORY.md.**

```bash
memanto memory sync --project-dir .
```

Read the file back and confirm it has content.

**6 — Offer the optional extras**, briefly, and only do them if the user says yes:

- `memanto schedule enable` — nightly daily-summary, conflict detection, and expiry sweep
- `memanto connect cursor` (or `codex`, `windsurf`, `gemini-cli`, …) — share this memory with
  other tools; `memanto connect list` shows all supported agents
- `memanto migrate mem0` / `letta` / `supermemory` — import memory from another provider

**7 — Point out what is already running**, briefly:

- `MEMORY.md` refreshes automatically at the start of every session, and again before
  compaction.
- The `👾 Memanto` status line installs itself on the first session. `/memanto:statusline
  preview` shows it; `/memanto:statusline remove` turns it off.
- The `memory-scout` subagent gathers deep background before big work — worth naming
  explicitly before a refactor.

Finish by telling them the commands they will actually use day to day: `/memanto:remember`,
`/memanto:recall`, `/memanto:answer`, and `/memanto:capture` at the end of a session.
