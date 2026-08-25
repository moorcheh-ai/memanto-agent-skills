---
description: Install, preview, or remove the MEMANTO status line
argument-hint: [install | remove | preview]
allowed-tools: Bash, Read, Edit
disable-model-invocation: true
---

Manage the MEMANTO status line. Action (default `install`): `$ARGUMENTS`

The status line renders as:

```
👾 Memanto · my-project · 42 memories · +3 this session · synced 2m ago
```

It reads the active agent from `~/.memanto/sessions/active` and the memory count from the
project's `MEMORY.md`. No background process, no cooperating hooks.

## preview

Run it directly against the current project to see the output:

```bash
python "${CLAUDE_PLUGIN_ROOT}/statusline.py" <<'EOF'
{"session_id":"preview","workspace":{"project_dir":"."}}
EOF
```

If `python` is not found, try `python3`. Show the user the rendered line.

## install

A plugin cannot ship a `statusLine` — plugin `settings.json` only honors `agent` and
`subagentStatusLine` — so the entry goes in the user's own settings.

1. Read `~/.claude/settings.json` (create `{}` if missing).

2. **If a `statusLine` already exists and is not MEMANTO's, stop and ask** before replacing
   it. Show them what is currently configured. Never silently overwrite another status line.

3. Resolve the interpreter that actually exists on this machine — do not guess between
   `python` and `python3`:

   ```bash
   python -c "import sys; print(sys.executable)" || python3 -c "import sys; print(sys.executable)"
   ```

4. Set `statusLine`, using the absolute interpreter path from step 3 and the absolute path
   to `${CLAUDE_PLUGIN_ROOT}/statusline.py`:

   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "\"<interpreter>\" \"<plugin root>/statusline.py\"",
       "refreshInterval": 5
     }
   }
   ```

   `refreshInterval` keeps the sync age ticking while the session is idle. Preserve every
   other key in the file, and keep the existing indentation.

5. Tell the user it takes effect the next time Claude Code starts.

## remove

Delete the `statusLine` key from `~/.claude/settings.json`, leaving the rest of the file
untouched. Also clear the install marker so the plugin does not silently reinstall it on the
next session:

```bash
rm -f ~/.memanto/.claude-statusline/installed
```

Confirm what you removed.

---

The plugin installs this automatically on its first session and never overwrites an existing
`statusLine`. Use this command to re-install after removing it, to switch from another status
line, or to preview the output before committing to it.
