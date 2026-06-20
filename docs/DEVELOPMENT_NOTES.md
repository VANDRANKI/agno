# Development Notes

Practical notes for contributors working on the Agno codebase.

## Environment Setup

```bash
# Clone and set up the dev environment
git clone https://github.com/agno-agi/agno.git
cd agno
./scripts/dev_setup.sh
source .venv/bin/activate

# Verify the setup
python scripts/check_agent_setup.py
```

## Running Tests

```bash
# Run all unit tests
pytest libs/agno/tests/

# Run a single test file with verbose output
pytest libs/agno/tests/unit/test_agent.py -v

# Run with coverage
pytest libs/agno/tests/ --cov=libs/agno/agno --cov-report=term-missing
```

## Code Style Conventions

- **No f-strings on print lines without variables** — use plain string concatenation.
- **Both sync and async** — every public method needs a synchronous *and* an async variant.
- **Never create agents inside loops** — instantiate once, reuse.
- **Type hints are required** on all public API surfaces.

## Common Pitfalls

### Missing async variant

If you add a new public method, always pair it with an `async` version:

```python
def run(self, message: str) -> str:
    """Run the agent synchronously."""
    ...

async def arun(self, message: str) -> str:
    """Run the agent asynchronously."""
    ...
```

### Database setup for integration tests

Start the local PostgreSQL container before running integration tests:

```bash
./cookbook/scripts/run_pgvector.sh
```

## Releasing

Version bumps are handled by the core team. Contributors should open a PR
against `main` and wait for a maintainer to trigger the release workflow.
