# AI-Assisted Development Workflow

Use this checklist when starting work in a repository that has `context-router` configured.

## 1. Check tool health

```bash
context-router --version
context-router doctor
```

## 2. Refresh the index

```bash
context-router index
```

Run this after major file changes or dependency changes.

## 3. Ask for the right context pack

```bash
context-router pack --mode implement --query "describe the task here"
context-router pack --mode debug --error-file pytest.xml
context-router pack --mode review
context-router pack --mode handover
```

## 4. Save useful project memory

Capture lessons that future sessions should not rediscover.

Examples:

```bash
context-router memory save "Authentication tokens are validated in middleware before request handlers run."
context-router decisions add "Use DynamoDB streams for async billing updates" --status accepted
```

## 5. Commit memory with code

When an observation or decision explains a code change, commit it with the implementation so teammates and future agents get the same context.
