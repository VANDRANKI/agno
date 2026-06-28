"""Typed structured-output agent example.

Demonstrates using output_schema to receive strongly-typed Pydantic models
instead of raw text from an Agno agent.
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from agno.agent import Agent
from agno.models.openai import OpenAIResponses


# ---------------------------------------------------------------------------
# Output schemas
# ---------------------------------------------------------------------------


class ResearchPoint(BaseModel):
    """A single research finding."""

    heading: str = Field(description="Short heading for the finding.")
    detail: str = Field(description="One or two sentence explanation.")
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )


class ResearchReport(BaseModel):
    """Structured research report returned by the agent."""

    topic: str
    summary: str
    findings: List[ResearchPoint]
    sources_consulted: int


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

research_agent = Agent(
    model=OpenAIResponses(id="gpt-5.4"),
    description="You are a research analyst. Return only structured JSON.",
    output_schema=ResearchReport,
)


def run_research(topic: str) -> ResearchReport:
    """Run the research agent and return a typed ResearchReport."""
    response = research_agent.run(
        f"Research the following topic and produce a structured report: {topic}"
    )
    # When output_schema is set, response.content is the parsed Pydantic model.
    if not isinstance(response.content, ResearchReport):
        raise TypeError(f"Unexpected response type: {type(response.content)}")
    return response.content


if __name__ == "__main__":
    report = run_research("Applications of large language models in healthcare")
    print(f"Topic: {report.topic}")
    print(f"Summary: {report.summary}")
    print(f"Findings: {len(report.findings)}")
    for finding in report.findings:
        print(f"  - {finding.heading} (confidence={finding.confidence:.0%})")
        print(f"    {finding.detail}")
