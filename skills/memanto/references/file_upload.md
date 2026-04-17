# File Upload — Ingest Documents into Agent Memory

The `memanto upload` command ingests a document file into the active agent's Moorcheh namespace. Uploaded content is processed, embedded, and made immediately searchable via `memanto recall` and `memanto answer`.

## When to Use File Upload

Use file upload to ground your agent in large reference documents that would be impractical to store as individual memories:

- Architecture decision records, design docs, PRDs
- API specifications (OpenAPI/Swagger JSON)
- Meeting notes, interview transcripts
- Spreadsheets with project data
- Codebases exported as Markdown

## Basic Usage

```bash
memanto upload path/to/document.pdf
memanto upload path/to/spec.md
memanto upload path/to/data.xlsx
```

An active session is required. Run `memanto agent activate <agent-id>` first.

## Supported File Types

| Extension | Format |
|-----------|--------|
| `.pdf` | PDF document |
| `.docx` | Word document |
| `.xlsx` | Excel spreadsheet |
| `.json` | JSON data |
| `.txt` | Plain text |
| `.csv` | Comma-separated values |
| `.md` | Markdown |

Maximum file size: **5 GB**

Unsupported types (e.g. `.png`, `.zip`) will be rejected with a 400 error listing the allowed extensions.

## HTTP API

```
POST /api/v2/agents/{agent_id}/upload-file
Content-Type: multipart/form-data
Authorization: Bearer {moorcheh_api_key}
X-Session-Token: {session_token}

file: <binary>
```

### Response

```json
{
  "agent_id": "my-agent",
  "session_id": "sess-abc123",
  "namespace": "memanto_agent_my-agent",
  "file_name": "architecture.pdf",
  "file_size": 204800,
  "status": "uploaded",
  "message": "File processed and indexed successfully"
}
```

`status` is either `"uploaded"` (success) or `"failed"` (processing error).

## Python Script

```bash
uv run skills/memanto/scripts/upload_file.py path/to/document.pdf
```

Or directly:

```bash
python skills/memanto/scripts/upload_file.py path/to/notes.md
```

## curl Example

```bash
curl -X POST "http://localhost:8000/api/v2/agents/my-agent/upload-file" \
  -H "Authorization: Bearer $MOORCHEH_API_KEY" \
  -H "X-Session-Token: $SESSION_TOKEN" \
  -F "file=@/path/to/document.pdf"
```

## After Upload — Recall Uploaded Content

Once uploaded, the document's content is searchable using the same recall and answer commands:

```bash
# Search within uploaded content
memanto recall "authentication flow" --limit 10

# Ask questions grounded in the document
memanto answer "What are the rate limits described in the spec?"
```

Uploaded file content is stored as memories in the agent's namespace and follows the same confidence scoring and semantic search as manually stored memories.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Missing or invalid session token | Run `memanto agent activate <id>` |
| `400 Bad Request: unsupported file type` | File extension not in allowlist | Convert file to a supported format |
| `404 Not Found` | Agent ID doesn't exist | Run `memanto agent list` |
| `File not found` (local) | Path doesn't exist | Check the file path |
| Session scope mismatch | Token is for a different agent | Activate the correct agent session |

## Notes

- The upload endpoint requires both `Authorization` (API key) **and** `X-Session-Token` headers.
- Temporary files created during processing are automatically cleaned up by the server.
- Re-uploading the same file creates additional memory entries — check for existing content with `memanto recall` first if you want to avoid duplicates.
