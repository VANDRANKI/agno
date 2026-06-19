# Development Guide

This document covers everything you need to get started developing on Agno.

## Prerequisites

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) for environment management
- Git

## Virtual Environments

Agno uses **two separate virtual environments** for different purposes:

| Environment | Path | Purpose |
|-------------|------|---------|
| Development | `.venv/` | Tests, formatting, validation, linting |
| Cookbook demos | `.venvs/demo/` | Running cookbook examples (heavier deps) |

### Set Up Development Environment

```bash
# Create and populate the dev venv
./scripts/dev_setup.sh

# Activate it
source .venv/bin/activate
```

### Set Up Cookbook Environment

```bash
# Create and populate the demo venv
./scripts/demo_setup.sh
```

## Code Quality

Before pushing any code, run both scripts and fix all errors:

```bash
# Activate the dev venv first
source .venv/bin/activate

# Format all code (runs ruff format)
./scripts/format.sh

# Validate all code (runs ruff check + mypy)
./scripts/validate.sh
```

Both must pass with no errors before code review.

## Running Tests

```bash
source .venv/bin/activate

# Run all tests
pytest libs/agno/tests/

# Run a specific test file
pytest libs/agno/tests/unit/test_agent.py

# Run with verbose output
pytest libs/agno/tests/ -v
```

## Cookbook Testing

### Quick Start

```bash
# Start the PostgreSQL vector database (if needed)
./cookbook/scripts/run_pgvector.sh

# Run a cookbook example
.venvs/demo/bin/python cookbook/<folder>/<file>.py

# Tail long-running output
.venvs/demo/bin/python cookbook/<folder>/<file>.py 2>&1 | tail -100
```

### After Testing a Cookbook

Update the cookbook's `TEST_LOG.md` with:
- Test name and path
- Status: PASS or FAIL
- Brief description of what was tested
- Notable observations or issues

See `cookbook/08_learning/` for the golden-standard cookbook structure.

## Key Coding Rules

These rules are enforced during code review — follow them from the start:

1. **Never create agents in loops.** Agents should be instantiated once and reused across iterations. Creating them in loops wastes resources and degrades performance.

   ```python
   # Wrong
   for item in items:
       agent = Agent(model=OpenAIResponses(id="gpt-5.4"))
       agent.run(item)

   # Right
   agent = Agent(model=OpenAIResponses(id="gpt-5.4"))
   for item in items:
       agent.run(item)
   ```

2. **Both sync and async variants required.** Every public method that does I/O must have both a synchronous and an asynchronous implementation. Callers in async contexts need `await agent.arun(...)` to work.

3. **Use `OpenAIResponses`, not `OpenAIChat`.** In cookbooks and examples, import from `agno.models.openai` and use `OpenAIResponses`. Do not use the deprecated `OpenAIChat`.

4. **Use `gpt-5.4` as the default model.** Do not use `gpt-4o` or `gpt-4o-mini` in new cookbooks or examples.

5. **Use `output_schema` for structured responses.** When you need a structured output, use `output_schema` rather than prompt engineering.

6. **PostgreSQL in production, SQLite for dev only.** Use SQLite for quick local development, but write cookbook examples targeting PostgreSQL.

7. **No f-strings for print lines with no variables.** Use plain string literals: `print("Starting agent")` not `print(f"Starting agent")`.

8. **No emojis in examples and print lines.**

## PR Requirements

### Title Format

PR titles must follow one of these formats:
- `type: description` — e.g., `feat: add workflow serialization`
- `[type] description` — e.g., `[feat] add workflow serialization`

Valid types: `feat`, `fix`, `cookbook`, `test`, `refactor`, `chore`, `style`, `revert`, `release`

PRs with non-conforming titles will fail the title lint check in CI.

### PR Description

Always follow the PR template in `.github/pull_request_template.md`. Include:
- Summary of changes
- Type of change
- Completed checklist
- Any additional context

### Automated CI Review

Every non-draft PR automatically receives a review from Opus via the CI pipeline (10 specialized agents). This is expected behavior — the review appears as a sticky comment on the PR. You do not need to trigger it manually.

## Code Locations

| What | Where |
|------|-------|
| Core agent code | `libs/agno/agno/agent/` |
| Teams | `libs/agno/agno/team/` |
| Workflows | `libs/agno/agno/workflow/` |
| Tools | `libs/agno/agno/tools/` |
| Models | `libs/agno/agno/models/` |
| Knowledge/RAG | `libs/agno/agno/knowledge/` |
| Memory | `libs/agno/agno/memory/` |
| Database adapters | `libs/agno/agno/db/` |
| Vector databases | `libs/agno/agno/vectordb/` |
| Tests | `libs/agno/tests/` |

## Getting Help

- Check `CLAUDE.md` for additional project-specific guidelines
- Open an issue using the templates in `.github/ISSUE_TEMPLATE/`
- Review existing PRs for examples of well-formed contributions
