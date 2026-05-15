# File Upload — Ingest Documents into Agent Memory

`memanto upload` ingests a document into the active agent's Moorcheh namespace. The content is
processed, embedded, and immediately searchable via `memanto recall` and `memanto answer`.

## When to use it

Ground the agent in large reference documents that would be impractical to store as individual
memories:

- Architecture decision records, design docs, PRDs
- API specifications (OpenAPI/Swagger JSON)
- Meeting notes, interview transcripts
- Spreadsheets with project data
- Documentation exported as Markdown

**When not to use it:** source code, logs, and config files. Read those yourself and store the
durable conclusions with `memanto remember`. Raw code chunks retrieve poorly against natural
language queries, and they bloat the namespace.

## Usage

```bash
memanto upload path/to/document.pdf
memanto upload path/to/spec.md
memanto upload path/to/data.xlsx
```

Requires an active agent. Run `memanto agent activate <agent-id>` first if `memanto status`
shows none.

## Supported formats

| Extension | Format |
|-----------|--------|
| `.pdf` | PDF document |
| `.docx` | Word document |
| `.xlsx` | Excel spreadsheet |
| `.json` | JSON data |
| `.txt` | Plain text |
| `.csv` | Comma-separated values |
| `.md` | Markdown |

Maximum file size: **5 GB**. Anything else (`.png`, `.zip`, …) is rejected with the allowed
list.

## Verify the ingest

```bash
memanto recall "<a distinctive phrase from the document>" --limit 5
memanto answer "What are the rate limits described in the spec?"
```

Uploaded content becomes ordinary memories in the agent's namespace, carrying `imported`
provenance, and is subject to the same semantic search and confidence scoring as anything you
store by hand.

## Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `MEMANTO not configured` | No API key | Run `memanto`, or export `MOORCHEH_API_KEY` |
| `No active agent` | Nothing activated | `memanto agent activate <id>` |
| Unsupported file type | Extension not in the allowlist | Convert to a supported format |
| File exceeds maximum upload size | Over 5 GB | Split the document |
| `File not found` | Bad path | Check the path |

## Notes

- Re-uploading the same file creates **additional** memory entries. Recall first if you are
  unsure whether a document is already ingested — there is no dedupe on upload.
- After a large ingest, run `memanto detect-conflicts`; imported documents frequently contradict
  memories the agent already holds.
