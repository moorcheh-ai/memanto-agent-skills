# Conflict Detection & Resolution

Memory contradicts itself over time. A decision gets reversed, a preference changes, a fact is
corrected. Left alone, both versions stay in the namespace and every future `recall` surfaces
them side by side with no way to tell which is current — retrieval quality degrades and RAG
answers hedge or pick wrong.

MEMANTO detects contradictions with an LLM pass and lets you resolve them.

## Detect

```bash
memanto detect-conflicts
memanto detect-conflicts --date 2026-08-20
memanto detect-conflicts --agent my-agent
```

Runs conflict detection over that day's session memories and writes a JSON report to
`~/.memanto/conflicts/`. Defaults to today and the active agent.

## Review

```bash
memanto conflicts --list
```

Lists detected conflicts without entering the interactive resolver. Use this to see what is
outstanding before deciding how to spend time on it.

## Resolve

```bash
memanto conflicts
memanto conflicts --date 2026-08-20
memanto conflicts --agent my-agent
```

Walks each unresolved conflict and prompts for a resolution. **This is interactive** — it needs
a real terminal. Inside Claude Code, run it yourself with `! memanto conflicts` rather than
having the agent call it through a tool.

## Resolving non-interactively

If you already know which side wins, expire the loser directly:

```bash
memanto memory expire <losing-id> --reason "conflicts-with-<winning-id>"
```

Expiry keeps the memory visible in recall labelled `[EXPIRED]`, so the audit trail of what
changed survives. Reverse it with `memanto memory restore <id>`.

## Which side should win?

| Signal | Prefer |
|---|---|
| Recency | The newer memory, for decisions and status |
| Provenance | `explicit_statement` and `corrected` over `inferred` and `observed` |
| Confidence | The higher score, when recency and provenance are equal |
| Specificity | The more specific memory over the vaguer one |

Recency is not automatically right. A high-confidence `instruction` from the user ("always use
type hints") outranks a later `observation` that contradicts it — the observation is evidence
the instruction was violated, not that it was revoked.

## Preventing conflicts

- Recall before you remember; update an existing memory with `memanto edit` rather than storing
  a second version.
- When the user corrects you, expire the old memory *and* store the correction with
  `--provenance corrected`, so the reason survives.
- Enable the nightly job (`memanto schedule enable`) so detection runs on its own rather than
  only when someone remembers to check.

## Automation

```bash
memanto schedule enable
memanto schedule status
memanto schedule disable
```

The nightly job runs daily summary, conflict detection, and the expiry sweep together. It
*detects* conflicts; resolution stays manual by design, since picking a winner is a judgment
call.
