# Environment Requirements

## Required Environment Variables

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `MOORCHEH_API_KEY` | Moorcheh platform API key | [console.moorcheh.ai](https://console.moorcheh.ai) |

## Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `MEMANTO_SERVER_URL` | Custom server URL (self-hosted) | `http://localhost:8000` |
| `MEMANTO_AGENT_ID` | Override active agent ID | From session file |

## Python Dependencies

```bash
# Minimal (CLI only)
pip install memanto

# With SDK for programmatic use
pip install memanto moorcheh-sdk

# With async support
pip install memanto moorcheh-sdk httpx

# Using uv (recommended)
uv pip install memanto moorcheh-sdk httpx
```

## Python Version

MEMANTO requires Python 3.10 or later. Tested on 3.10, 3.11, 3.12, 3.13.

```bash
python --version   # Must be >= 3.10
```

## Verifying the Environment

```bash
# Check MOORCHEH_API_KEY is set
echo $MOORCHEH_API_KEY

# Check memanto CLI is installed
memanto --version

# Check server is reachable (local development)
curl http://localhost:8000/health

# Run full status check
memanto status
```
