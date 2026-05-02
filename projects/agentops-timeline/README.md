# AgentOps Timeline

AgentOps Timeline is a local-first CLI for recording what happened during an AI-assisted coding session.

`context-router` helps an agent start with better context. AgentOps Timeline focuses on the other side of the workflow: what the agent changed, which commands ran, what failed, what passed, and what should go into the handoff or PR description.

## Why this exists

AI coding sessions can move quickly. After a few prompts, it is easy to lose the thread:

- Which files changed?
- Which tests actually ran?
- What decisions were made?
- What risks remain?
- What should reviewers look at first?

AgentOps Timeline records those events locally and turns them into a clean Markdown timeline.

## Features

- Start named coding sessions
- Record notes, decisions, risks, and next steps
- Run and capture command output
- Snapshot git status and diff stats
- Generate session summaries
- Export PR notes from the session timeline
- Stores everything locally in `.agentops-timeline/`

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

agentops init
agentops start "fix login token refresh"
agentops note "Found token refresh logic in src/auth/session.ts"
agentops run -- npm test
agentops snapshot
agentops summary
agentops export-pr-notes --output PR_NOTES.md
```

## Example summary

```md
# AgentOps Timeline Summary

Goal: fix login token refresh

## Commands
- PASS `npm test`

## Changed Files
- src/auth/session.ts
- tests/auth/session.test.ts

## Notes
- Found token refresh logic in src/auth/session.ts
- Added regression coverage for expired access tokens

## Risks
- Refresh-token rotation still needs integration coverage
```

## Commands

```bash
agentops init
agentops start "describe the goal"
agentops note "important observation"
agentops decision "use retry budget instead of infinite retries"
agentops risk "integration coverage still missing"
agentops next-step "add e2e test for refresh-token rotation"
agentops run -- pytest -q
agentops snapshot
agentops summary
agentops export-pr-notes --output PR_NOTES.md
```

## Project status

This is an MVP CLI. The next useful features are:

- GitHub PR body generation from a branch diff
- Detection of stale sessions
- HTML timeline export
- Optional MCP server interface
- Repeated-review-pattern tracking
