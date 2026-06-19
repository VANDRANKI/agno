"""Unit tests for agno.utils.validation."""

import pytest
from agno.utils.validation import (
    validate_model_id,
    validate_positive_int,
    validate_optional_str,
)


class TestValidateModelId:
    def test_valid_model_id(self):
        assert validate_model_id("gpt-5.4") == "gpt-5.4"

    def test_strips_whitespace(self):
        assert validate_model_id("  claude-sonnet-4-6  ") == "claude-sonnet-4-6"

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            validate_model_id("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            validate_model_id("   ")


class TestValidatePositiveInt:
    def test_valid_positive_int(self):
        assert validate_positive_int(5, "max_tokens") == 5

    def test_zero_raises(self):
        with pytest.raises(ValueError, match="positive"):
            validate_positive_int(0, "max_tokens")

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="positive"):
            validate_positive_int(-1, "max_tokens")

    def test_non_int_raises(self):
        with pytest.raises(TypeError, match="integer"):
            validate_positive_int("5", "max_tokens")


class TestValidateOptionalStr:
    def test_none_returns_none(self):
        assert validate_optional_str(None, "description") is None

    def test_valid_string(self):
        assert validate_optional_str("hello", "description") == "hello"

    def test_strips_whitespace(self):
        assert validate_optional_str("  hello  ", "description") == "hello"

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="not be empty"):
            validate_optional_str("", "description")

    def test_non_string_raises(self):
        with pytest.raises(TypeError, match="string"):
            validate_optional_str(123, "description")
