"""Typed agent responses using output_schema.

This cookbook demonstrates how to use Pydantic models with Agno agents
to get structured, type-safe outputs instead of raw text responses.

Key patterns:
- Define output_schema on the agent for structured responses
- Both sync and async variants are shown
- Proper type annotations throughout
"""

from typing import Optional

from pydantic import BaseModel, Field

from agno.agent import Agent
from agno.models.openai import OpenAIResponses


class MovieReview(BaseModel):
    """Structured movie review with typed fields."""

    title: str = Field(description="The movie title")
    year: int = Field(description="Release year")
    rating: float = Field(description="Rating from 0.0 to 10.0", ge=0.0, le=10.0)
    summary: str = Field(description="Brief summary of the plot without spoilers")
    pros: list[str] = Field(description="List of positive aspects")
    cons: list[str] = Field(description="List of negative aspects")
    recommended: bool = Field(description="Whether to recommend this movie")
    suitable_for: Optional[str] = Field(
        default=None, description="Target audience description"
    )


class ResearchSummary(BaseModel):
    """Structured research output with citations."""

    topic: str = Field(description="The research topic")
    key_findings: list[str] = Field(description="Main findings, 3-5 bullet points")
    confidence: float = Field(
        description="Confidence level from 0.0 to 1.0", ge=0.0, le=1.0
    )
    sources_needed: bool = Field(
        description="Whether external sources should be consulted"
    )
    follow_up_questions: list[str] = Field(
        description="Questions for deeper investigation"
    )


def get_movie_review(movie_title: str) -> MovieReview:
    """Get a structured movie review from the agent.

    Args:
        movie_title: The name of the movie to review.

    Returns:
        A fully typed MovieReview object.
    """
    agent = Agent(
        model=OpenAIResponses(id="gpt-5.4"),
        output_schema=MovieReview,
        instructions=[
            "You are a film critic. Provide honest, balanced reviews.",
            "Always provide specific pros and cons, not vague statements.",
        ],
    )

    response = agent.run(f"Review the movie: {movie_title}")
    return response.content  # type: ignore[return-value]


async def get_research_summary(topic: str) -> ResearchSummary:
    """Async version of structured research output.

    Args:
        topic: The research topic to summarize.

    Returns:
        A fully typed ResearchSummary object.
    """
    agent = Agent(
        model=OpenAIResponses(id="gpt-5.4"),
        output_schema=ResearchSummary,
        instructions=[
            "You are a research assistant.",
            "Provide concise, factual summaries.",
            "Be honest about confidence levels.",
        ],
    )

    response = await agent.arun(f"Summarize research on: {topic}")
    return response.content  # type: ignore[return-value]


if __name__ == "__main__":
    import asyncio

    # Sync example
    review = get_movie_review("Inception")
    print(f"Movie: {review.title} ({review.year})")
    print(f"Rating: {review.rating}/10")
    print(f"Recommended: {review.recommended}")
    print(f"Pros: {', '.join(review.pros[:2])}")

    # Async example
    summary = asyncio.run(get_research_summary("transformer attention mechanisms"))
    print(f"\nTopic: {summary.topic}")
    print(f"Confidence: {summary.confidence:.0%}")
    print(f"Key findings: {len(summary.key_findings)} items")
