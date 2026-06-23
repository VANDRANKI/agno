# Agent Development Quickstart

This guide helps you get started building agents with Agno.

## Prerequisites

```bash
# Set up the development environment
./scripts/dev_setup.sh
source .venv/bin/activate
```

## Your First Agent

```python
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

agent = Agent(
    model=OpenAIResponses(id="gpt-5.4"),
    description="A helpful assistant",
    instructions=["Answer questions concisely and accurately."],
)

agent.print_response("What is the capital of France?")
```

## Using Tools

```python
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=OpenAIResponses(id="gpt-5.4"),
    tools=[DuckDuckGoTools()],
    description="A web-search enabled assistant",
    show_tool_calls=True,
)

agent.print_response("What happened in AI today?")
```

## Structured Output

Use `output_schema` for structured, type-safe responses:

```python
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.openai import OpenAIResponses

class MovieReview(BaseModel):
    title: str
    rating: float
    summary: str
    recommended: bool

agent = Agent(
    model=OpenAIResponses(id="gpt-5.4"),
    output_schema=MovieReview,
)

review = agent.run("Review the movie Inception")
print(review.content)  # MovieReview instance
```

## Agent Memory

```python
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory

memory = Memory(db=SqliteMemoryDb(table_name="agent_memory"))

agent = Agent(
    model=OpenAIResponses(id="gpt-5.4"),
    memory=memory,
    enable_agentic_memory=True,
)
```

## Best Practices

- **Reuse agent instances** — never create agents inside loops
- **Use `output_schema`** for any structured data (not string parsing)
- **Prefer PostgreSQL** in production; SQLite only for local dev
- **Always test both sync and async** variants of public methods
- **Avoid f-strings** in print lines when there are no variables
