# Agno Development Guide

This document supplements `CLAUDE.md` with practical setup instructions.

## Two Virtual Environments

| Environment | Purpose | Setup command |
|---|---|---|
| `.venv/` | Tests, formatting, validation | `./scripts/dev_setup.sh` |
| `.venvs/demo/` | Running cookbook examples | `./scripts/demo_setup.sh` |

Use `.venv` for all code-quality work. Use `.venvs/demo` only when
running cookbook scripts that require extra ML dependencies.

## Setup

```bash
git clone https://github.com/VANDRANKI/agno.git
cd agno
./scripts/dev_setup.sh   # creates .venv
source .venv/bin/activate
```

## Running Tests

```bash
pytest libs/agno/tests/ -v

# Specific file
pytest libs/agno/tests/unit/test_agent.py -v
```

## Code Quality

```bash
# Format (must pass before any PR)
./scripts/format.sh

# Lint + type check (must pass before any PR)
./scripts/validate.sh
```

Both scripts must exit cleanly before submitting a PR.

## Running Cookbooks

```bash
# Setup cookbook environment once
./scripts/demo_setup.sh

# Start any required services
./cookbook/scripts/run_pgvector.sh

# Run a cookbook
.venvs/demo/bin/python cookbook/<folder>/<file>.py
```

## Updating TEST_LOG.md

After running a cookbook, update its `TEST_LOG.md`:

```markdown
### filename.py

**Status:** PASS

**Description:** What the test does and what was observed.

**Result:** Summary of success or failure.

---
```

## Core Code Locations

| What | Where |
|---|---|
| Agent core | `libs/agno/agno/agent/` |
| Teams | `libs/agno/agno/team/` |
| Tools | `libs/agno/agno/tools/` |
| Models | `libs/agno/agno/models/` |
| Memory | `libs/agno/agno/memory/` |

## Key Rules

- Do **not** create agents inside loops — reuse them
- Every public method needs both sync and async variants
- Use `output_schema` for structured responses
- Do **not** use `OpenAIChat`; use `OpenAIResponses`
- Do **not** use `gpt-4o` or `gpt-4o-mini`; use `gpt-5.4`

## PR Title Format

```
feat: add tool retry logic with exponential backoff
fix: prevent duplicate tool calls in parallel agent
docs: add cookbook for multi-agent RAG pipeline
```
