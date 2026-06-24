"""Unit tests for the agno.debug module."""

import logging

import pytest

from agno.debug import disable_debug_mode, enable_debug_mode, toggle_debug_mode
from agno.utils.log import logger


def test_enable_debug_mode_sets_debug_level():
    """enable_debug_mode() should set the agno logger to DEBUG."""
    disable_debug_mode()  # start from a known state
    enable_debug_mode()
    assert logger.level == logging.DEBUG


def test_disable_debug_mode_sets_info_level():
    """disable_debug_mode() should reset the agno logger to INFO."""
    enable_debug_mode()  # start from a known state
    disable_debug_mode()
    assert logger.level == logging.INFO


def test_toggle_debug_mode_enables_when_off():
    """toggle_debug_mode() should enable debug and return True when off."""
    disable_debug_mode()
    result = toggle_debug_mode()
    assert result is True
    assert logger.level == logging.DEBUG


def test_toggle_debug_mode_disables_when_on():
    """toggle_debug_mode() should disable debug and return False when on."""
    enable_debug_mode()
    result = toggle_debug_mode()
    assert result is False
    assert logger.level == logging.INFO


def test_toggle_debug_mode_idempotent_round_trip():
    """Two consecutive toggles should return to the original level."""
    disable_debug_mode()
    original_level = logger.level
    toggle_debug_mode()
    toggle_debug_mode()
    assert logger.level == original_level
