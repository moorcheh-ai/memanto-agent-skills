---
description: Detect and resolve contradictory MEMANTO memories
argument-hint: [YYYY-MM-DD]
allowed-tools: Bash(memanto:*)
disable-model-invocation: true
---

Find and resolve contradictions in MEMANTO memory. Date (default today): `$ARGUMENTS`

**1 — Run detection.** This is an LLM pass over the day's memories; it writes a JSON report to
`~/.memanto/conflicts/`.

```bash
memanto detect-conflicts
```

Add `--date $ARGUMENTS` if a date was given, `--agent <id>` for a non-active agent.

**2 — List what it found**, without entering the interactive resolver:

```bash
memanto conflicts --list
```

**3 — Summarize each conflict for the user**: what the two memories claim, when each was
stored, and their confidence. Recommend which should win — usually the more recent one, or the
one with `explicit_statement` provenance over `inferred`.

**4 — Resolve.** The interactive resolver needs a real terminal, so ask the user to run it
themselves — they can type `! memanto conflicts` in this session:

```bash
memanto conflicts
```

Alternatively, if they tell you which side wins, resolve it directly:

```bash
memanto memory expire <losing-id> --reason "conflicts-with-<winning-id>"
```

Unresolved conflicts degrade every future `recall` and `answer`, because retrieval surfaces both
sides and cannot tell which is current. Worth clearing.
