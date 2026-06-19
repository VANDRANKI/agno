"""Input validation utilities for the Agno agent framework.

These helpers are used internally to validate configuration passed to
agents, teams, and tools before execution begins.
"""

from __future__ import annotations

from typing import Any, Optional


def validate_model_id(model_id: str) -> str:
    """Validate and normalise a model identifier string.

    Args:
        model_id: The model identifier (e.g. ``'gpt-5.4'``, ``'claude-sonnet-4-6'``).

    Returns:
        The model identifier stripped of surrounding whitespace.

    Raises:
        ValueError: If ``model_id`` is empty after stripping whitespace.
    """
    stripped = model_id.strip()
    if not stripped:
        raise ValueError("model_id must be a non-empty string")
    return stripped


def validate_positive_int(value: Any, name: str) -> int:
    """Validate that a value is a positive integer.

    Args:
        value: The value to validate.
        name: The parameter name, used in error messages.

    Returns:
        The validated integer value.

    Raises:
        TypeError: If ``value`` is not an integer.
        ValueError: If ``value`` is not positive.
    """
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value


def validate_optional_str(value: Optional[str], name: str) -> Optional[str]:
    """Validate an optional string parameter.

    Args:
        value: The value to validate (may be ``None``).
        name: The parameter name, used in error messages.

    Returns:
        The stripped string, or ``None`` if the input was ``None``.

    Raises:
        TypeError: If ``value`` is not a string and not ``None``.
        ValueError: If ``value`` is an empty string after stripping.
    """
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string or None, got {type(value).__name__}")
    stripped = value.strip()
    if not stripped:
        raise ValueError(f"{name} must not be empty when provided")
    return stripped
