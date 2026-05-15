---
description: Store something in MEMANTO persistent memory
argument-hint: <what to remember>
allowed-tools: Bash(memanto:*)
disable-model-invocation: true
---

Store this in MEMANTO persistent memory:

$ARGUMENTS

Steps:

1. **Check for duplicates first.** Run `memanto recall` with the key terms. If a memory already
   covers this, update it with `memanto edit <id>` instead of storing a near-duplicate.

2. **Classify it.** Pick exactly one type:
   `fact` · `decision` · `preference` · `instruction` · `goal` · `commitment` · `artifact` ·
   `learning` · `event` · `relationship` · `observation` · `error` · `context`

3. **Score confidence.** `1.0` explicit user statement · `0.9–0.95` strong consensus ·
   `0.8–0.85` pattern seen 3+ times · `0.7–0.75` reasonable inference · `0.6–0.65` single
   uncertain observation. **Below 0.6, do not store** — say so and stop.

4. **Set provenance** to how you learned it: `explicit_statement`, `inferred`, `observed`,
   `corrected`, `validated`, or `imported`.

5. **Write the content so it stands alone.** Someone reading it in three months with no
   conversation context should understand it. Include the reason and any commit or file
   reference. "Fixed the bug" is a failure; "Fixed OAuth token expiry bug by refreshing 60s
   early, commit abc123" is not.

6. **Store it** with 2–5 specific lowercase-hyphenated tags:

```bash
memanto remember "<self-contained content>" \
  --type <type> --confidence <0.0-1.0> --provenance <provenance> \
  --source claude_code --tags "<tag1,tag2,tag3>"
```

Report back what you stored, with its type and confidence.
