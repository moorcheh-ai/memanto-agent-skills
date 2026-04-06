# Contributing to MEMANTO Agent Skills

Thank you for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-skill`)
3. Add or improve skill files following the structure below
4. Submit a pull request

## Skill Structure

Each skill lives in `skills/<skill-name>/` and must include:

```
skills/my-skill/
├── SKILL.md          # Main skill definition (required)
├── references/       # Detailed reference guides (recommended)
│   └── *.md
└── scripts/          # Python implementation scripts (optional)
    └── *.py
```

## SKILL.md Format

```markdown
# Skill Name — Short Description

Brief overview of what this skill enables.

## Key Capabilities
...

## Getting Started
...

## Usage Notes
...
```

## Guidelines

- Keep skill descriptions concise and actionable
- Include working code examples in reference files
- Scripts must use the `moorcheh-sdk` or `memanto` CLI — no raw HTTP calls
- All examples should work with `MOORCHEH_API_KEY` set in the environment
- Follow the existing patterns in `skills/memanto/`

## Reporting Issues

Open an issue at [github.com/moorcheh-ai/memanto-agent-skills](https://github.com/moorcheh-ai/memanto-agent-skills/issues).
