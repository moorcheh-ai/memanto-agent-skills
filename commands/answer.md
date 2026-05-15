---
description: Answer a question from MEMANTO memory (RAG)
argument-hint: <question>
allowed-tools: Bash(memanto:*)
disable-model-invocation: true
---

Answer this question using MEMANTO's memory-grounded RAG:

$ARGUMENTS

```bash
memanto answer "$ARGUMENTS"
```

Add `--type <type>` to restrict the context to one memory type (for example `--type commitment`
for "what did I promise?"), and `--limit <n>` to widen or narrow the retrieved context beyond
the default of 5.

Then:

- Relay the answer along with the memories it was grounded in, so the user can judge it.
- If the answer is thin or the sources look weak, follow up with
  `memanto recall "<topic>" --limit 20` and reason over the raw memories yourself.
- If MEMANTO genuinely has nothing on this, say so explicitly — and offer to store the answer
  once you work it out together.

Never answer this from your own conversation context alone. The point of the command is what
is in memory, not what is in this session.
