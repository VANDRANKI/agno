"""Cookbook: Session-persistent memory agent.

Demonstrates using AgentMemory with a SQLite backend to persist conversation
history across multiple runs. Run this script twice to see the agent recall
facts from the previous session.

Requirements:
    pip install agno sqlalchemy
"""

from agno.agent import Agent
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# Memory backend: SQLite stores summaries and user facts across runs.
# Replace with PostgreSQL for production (agno.memory.v2.db.postgres).
# ---------------------------------------------------------------------------
memory_db = SqliteMemoryDb(
    table_name="agent_memories",
    db_file="/tmp/agno_session_demo.db",
)

memory = Memory(
    db=memory_db,
    # Automatically create user-level memory entries from conversation.
    create_user_memories=True,
    # Automatically summarise and update memories after each response.
    update_user_memories_after_run=True,
)

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    memory=memory,
    # Enable agentic memory management — the model decides what to store.
    enable_agentic_memory=True,
    # Inject stored memories into the system prompt for each request.
    add_memory_references=True,
    description="A helpful assistant that remembers facts about the user.",
    instructions=[
        "Greet the user by name if you know it.",
        "Reference past facts when relevant — e.g. the user's profession, preferences.",
        "When the user shares a new fact about themselves, acknowledge it explicitly.",
    ],
    markdown=True,
)

# ---------------------------------------------------------------------------
# Sample interaction — run this script twice; the second run will recall facts.
# ---------------------------------------------------------------------------
USER_ID = "demo-user-42"  # Unique identifier for this user session.

print("--- Session 1 ---")
agent.print_response(
    "Hi! My name is Alex and I work as a data engineer.",
    user_id=USER_ID,
    stream=True,
)

print("\n--- Session 2 (re-run to see memory recall) ---")
agent.print_response(
    "What do you know about me?",
    user_id=USER_ID,
    stream=True,
)
