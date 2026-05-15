# Recall — Search Persistent Memories

`memanto recall` searches all memories for the active agent, semantically or by time.

## Usage

```bash
memanto recall "query"
```

## Flags

| Flag | Description | Default |
|------|-------------|---------|
| `query` | Natural language search query | Required, except with the temporal flags |
| `--limit` / `-n` | Max results | 10 |
| `--type` / `-t` | Filter by memory type | All types |
| `--min-confidence` | Minimum stored confidence (0.0–1.0) | 0.0 |
| `--min-similarity` | Minimum semantic similarity score | None |
| `--tags` | Filter by tags (comma-separated) | None |
| `--as-of` | Point in time: what was true then | — |
| `--changed-since` | Differential: what changed since then | — |
| `--recent` | Newest first, chronological; needs no query | Off |
| `--active` | Active memories only | Off |
| `--expired` | Expired memories only | Off |

`--as-of`, `--changed-since`, and `--recent` are mutually exclusive, and none of them takes a
query.

## Active vs expired

By default recall returns **both** active and expired memories, each clearly labelled. An
expired memory is one that a policy sweep or a manual `memanto memory expire` retired — it still
carries its content and history. Narrow with `--active` or `--expired`.

```bash
memanto recall "deployment" --active     # only what is currently true
memanto recall "deployment" --expired    # only what used to be true
```

## Examples

```bash
# General search
memanto recall "database architecture"

# Decisions only
memanto recall "frontend framework" --type decision

# High-confidence facts
memanto recall "API authentication" --type fact --min-confidence 0.9

# Tag-scoped
memanto recall "token refresh" --tags "auth,security"

# Tighten semantic matching to cut loose results
memanto recall "rate limiting" --min-similarity 0.8

# What changed recently
memanto recall --changed-since "24h ago"

# What was true two days ago
memanto recall --as-of "2d ago"

# Newest first, no query
memanto recall --recent --limit 10
memanto recall --recent --type decision --limit 5

# Broad context load
memanto recall "instructions decisions goals" --limit 20
```

## Time formats

`--as-of` and `--changed-since` accept relative or ISO forms:

- `"1h ago"`, `"2d ago"`, `"1w ago"`, `"last 7 days"`
- `"2026-08-15"` or `"2026-08-15T12:00:00Z"`

## Session start pattern

```bash
memanto recall "instructions decisions goals" --limit 20
memanto recall "todo pending" --type commitment
```

## recall or answer?

`recall` returns raw memories for you to read and act on. `answer` synthesizes one grounded
response. If your next step is *"read these and act"*, use `recall`; if it is *"deliver this as
the answer"*, use `answer`. See [answer.md](answer.md).
