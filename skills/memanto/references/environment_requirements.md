# MEMANTO Environment Requirements

## Required

### API Key

`MOORCHEH_API_KEY` is the only mandatory environment variable. Obtain it from [console.moorcheh.ai](https://console.moorcheh.ai).

**Linux / macOS:**
```bash
export MOORCHEH_API_KEY="your-api-key"
```

**Windows (PowerShell):**
```powershell
$env:MOORCHEH_API_KEY = "your-api-key"
```

**Windows (CMD):**
```cmd
set MOORCHEH_API_KEY=your-api-key
```

**Persistent (add to shell profile):**
```bash
echo 'export MOORCHEH_API_KEY="your-api-key"' >> ~/.bashrc
source ~/.bashrc
```

**Via memanto CLI (stores in `~/.memanto/.env`):**
```bash
memanto
```

## Installation

### Using pip

```bash
pip install memanto
```

### Using uv (recommended)

```bash
uv pip install memanto
```

### Verify installation

```bash
memanto status
```

## Authentication Flow

MEMANTO uses two-layer authentication:

1. **API Key** — identifies your Moorcheh account (set once, stored in `~/.memanto/.env`)
2. **Session Token** — JWT identifying the active agent session (expires after 6 hours by default)

```bash
# Set API key (one time)
memanto

# Create agent (one time per project/agent)
memanto agent create my-agent

# Activate session (each time you start working)
memanto agent activate my-agent
```

## Security

- API keys are stored in `~/.memanto/.env` with 600 file permissions (user-readable only)
- Never commit `.env` files or API keys to version control
- Rotate keys periodically via [console.moorcheh.ai](https://console.moorcheh.ai)
- Session tokens expire automatically; re-activate as needed

## Optional Configuration

```bash
# View current config
memanto config show
```
