---
description: Ingest a document into MEMANTO memory
argument-hint: <file-path>
allowed-tools: Bash(memanto:*)
disable-model-invocation: true
---

Ingest this file into the active agent's memory namespace:

$ARGUMENTS

```bash
memanto upload "$ARGUMENTS"
```

Supported formats: `.pdf` `.docx` `.xlsx` `.json` `.txt` `.csv` `.md`

Before uploading, confirm the file exists and is one of those types. If it is something else
(source code, a log, a config file), read it yourself and store the durable conclusions with
`memanto remember` instead — uploading raw code to a memory namespace rarely retrieves well.

The upload is processed and embedded server-side. Once it returns, verify it is searchable:

```bash
memanto recall "<a distinctive phrase from the document>" --limit 5
```

Memories created this way carry `imported` provenance. Tell the user what landed and how to
retrieve it.
