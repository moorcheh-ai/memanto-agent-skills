# /memanto:quickstart

Interactive onboarding for MEMANTO — sets up your environment, creates an agent, and walks through core operations.

## Steps

1. **Check environment** — Verify `MOORCHEH_API_KEY` is set
2. **Install MEMANTO CLI** — Confirm `memanto` is installed and working
3. **Create an agent** — Set up a named agent identity for this project
4. **Activate session** — Start a session with a JWT token
5. **Store a test memory** — Verify the store → recall → answer pipeline works
6. **Sync MEMORY.md** — Export memory snapshot to the project root
7. **Connect to your agent** — Optionally connect Claude Code, Cursor, or other tools

## What to Do

Run through these commands step by step:

```bash
# Step 1: Verify API key
echo $MOORCHEH_API_KEY   # Should print your key

# Step 2: Install
pip install memanto
memanto status

# Step 3: Set API key in MEMANTO config
memanto config set api-key $MOORCHEH_API_KEY

# Step 4: Create an agent (replace 'my-project' with your project name)
memanto agent create my-project

# Step 5: Activate session
memanto agent activate my-project

# Step 6: Store a test memory
memanto remember "MEMANTO setup complete for this project. Ready to use persistent memory." \
  --type fact --confidence 1.0 --provenance explicit_statement --source setup --tags "setup,onboarding"

# Step 7: Recall the memory
memanto recall "setup"

# Step 8: Test RAG answer
memanto answer "Is MEMANTO set up for this project?"

# Step 9: Sync MEMORY.md
memanto memory sync --project-dir .

# Step 10: Connect to Claude Code (optional)
memanto connect claude-code
```

## Next Steps

- Read `MEMORY.md` to see your first memory
- Explore memory types: `/memanto:remember`
- Search memories: `/memanto:recall`
- Set up daily summaries: `memanto schedule enable`
- Connect other agents: `memanto connect cursor`
