# Contributing to MEMANTO Agent Skills

Thank you for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-skill`)
3. Add or improve files following the structure below
4. Validate (see below) and submit a pull request

## Repository Structure

```
.claude-plugin/
├── plugin.json        # Claude Code plugin manifest
└── marketplace.json   # Marketplace entry
commands/              # Slash commands — one .md per command
hooks/hooks.json       # SessionStart hook (MEMORY.md sync)
skills/<skill-name>/
├── SKILL.md           # Skill definition (required, needs YAML frontmatter)
└── references/*.md    # Detailed reference guides
```

## SKILL.md Format

YAML frontmatter is **required** — without it the skill violates the
[Agent Skills spec](https://agentskills.io/specification) and other tools will not load it.

```markdown
---
name: my-skill
description: What it does and when to use it. Lead with the trigger, since this is what the model reads to decide whether to load the skill.
allowed-tools: Bash(memanto:*)
license: MIT
---

# Skill Name

Body content.
```

Keep `description` specific about *when* to use the skill, not just what it is. It is the only
part always in context.

## Command Format

Commands are **prompts**, not documentation. Write instructions addressed to the agent, and
consume the user's input via `$ARGUMENTS`.

```markdown
---
description: One line, shown in the / menu
argument-hint: <what the user should type>
allowed-tools: Bash(memanto:*)
disable-model-invocation: true
---

Do the thing with:

$ARGUMENTS

1. Step one...
```

All commands here set `disable-model-invocation: true`. The `memanto` skill is the single path
Claude takes on its own; commands are user-invoked shortcuts. This keeps eleven command
descriptions out of every conversation's context.

## Guidelines

- **Verify every command against the installed CLI** before documenting it. Run `memanto <cmd>
  --help`. Most bugs in this repo have been documentation drifting ahead of or behind the CLI.
- Prefer the `memanto` CLI over raw HTTP. The CLI talks to Moorcheh directly and needs no
  server; raw HTTP against `localhost:8000` requires `memanto serve` to be running. If a
  cookbook does show the REST API, state that prerequisite explicitly.
- Reference bundled files with `${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_SKILL_DIR}`, never
  repo-relative paths — those break once the plugin is installed elsewhere.
- Keep `plugin.json`, `marketplace.json`, and `package.json` versions in sync.
- Match the existing style in `skills/memanto/`.

## Validating

Before opening a PR:

```bash
# Manifests, skills, and commands
claude plugin validate . --strict

# Component-level check (skills and commands only)
claude plugin validate ./skills --strict
claude plugin validate ./commands --strict
```

`--strict` turns warnings into failures, which is what CI should use — missing frontmatter and
unknown manifest fields are warnings the runtime tolerates but that break other tools.

## Reporting Issues

Open an issue at
[github.com/moorcheh-ai/memanto-agent-skills](https://github.com/moorcheh-ai/memanto-agent-skills/issues).
