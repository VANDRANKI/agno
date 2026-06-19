# Input Validation Guide

This guide covers the input validation utilities available in `agno.utils.validation`.

## Available validators

### `validate_model_id(model_id: str) -> str`

Strips whitespace and raises `ValueError` if the result is empty. Use whenever an agent or team receives a model identifier from configuration.

### `validate_positive_int(value: Any, name: str) -> int`

Ensures a value is a positive integer. Raises `TypeError` for non-integers and `ValueError` for zero or negative values. Use for parameters like `max_tokens`, `num_retries`, `context_window`.

### `validate_optional_str(value: Optional[str], name: str) -> Optional[str]`

Passes `None` through unchanged. For non-`None` values, strips whitespace and raises `ValueError` if the result is empty. Use for optional description, name, and tag fields.

## Pattern

Validate at the boundary — in `__init__` or `model_post_init`, not deep inside execution methods:

```python
from agno.utils.validation import validate_model_id, validate_positive_int

class MyAgent:
    def __init__(self, model_id: str, max_tokens: int = 1024):
        self.model_id = validate_model_id(model_id)
        self.max_tokens = validate_positive_int(max_tokens, "max_tokens")
```
