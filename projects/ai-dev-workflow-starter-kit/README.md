# AI Dev Workflow Starter Kit

A practical starter kit for setting up a local AI-assisted coding workflow with project memory, MCP-compatible context tools, and repeatable repository setup.

This project is designed for developers who want AI coding sessions to start with useful project context instead of re-reading the whole codebase every time.

## What this shows

- How to install and verify `context-router`
- How to initialize project memory with `.context-router/`
- How to generate focused context packs for implementation, debugging, review, and handover work
- How to keep useful observations and decisions in git
- How to document an AI-friendly workflow for future contributors

## Quickstart

```bash
# Install the CLI
pipx install context-router-cli

# Or with uv
uv tool install context-router-cli

# Inside a repository
context-router init
context-router setup --with-hooks
context-router index

# Generate a small focused pack
context-router pack --mode implement --query "add rate limiting"
```

## Verify the install

```bash
context-router --version
context-router doctor
```

A healthy install should print the installed version and `PASS` checks for language analyzers.

## Example workflow

```bash
# Before coding
context-router pack --mode implement --query "add retry handling to the billing API"

# During debugging
context-router pack --mode debug --error-file pytest.xml

# Before review
context-router pack --mode review

# Capture what was learned
context-router memory save "The billing API retries only idempotent requests to avoid duplicate invoice creation."
```

## Suggested repository layout

```text
.context-router/
  memory/
    observations/
    decisions/
docs/
  ai-workflow.md
  decision-template.md
.mcp.example.json
README.md
```

## Why it matters

AI coding tools work better when they can access a compact, relevant slice of the codebase plus the decisions behind it. This setup keeps that knowledge local, versioned, and easy to reuse across sessions.

## Next steps

- Add screenshots or terminal output from a real setup
- Add sample MCP configs for Claude Code, Cursor, Gemini CLI, and Codex
- Add a small demo repository and show before/after context packs
