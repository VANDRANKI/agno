"""Debug mode helpers for the agno library.

Provides two public functions to toggle verbose debug logging on and off
for the entire agno framework at runtime.  Under the hood they delegate
to the logging utilities in :mod:`agno.utils.log`.

Example::

    from agno.debug import enable_debug_mode, disable_debug_mode

    enable_debug_mode()   # all agno loggers now emit DEBUG messages
    # ... run your agent ...
    disable_debug_mode()  # loggers return to INFO level
"""


def enable_debug_mode() -> None:
    """Enable debug mode for the agno library.

    Sets the root agno logger level to ``DEBUG`` so that verbose internal
    messages (prompt construction, tool calls, model requests, etc.) are
    emitted to the configured handler.

    This is a global, process-wide change and takes effect immediately.
    Call :func:`disable_debug_mode` to revert to the default ``INFO`` level.
    """
    from agno.utils.log import set_log_level_to_debug

    set_log_level_to_debug()


def disable_debug_mode() -> None:
    """Disable debug mode for the agno library.

    Resets the root agno logger level back to ``INFO``, suppressing the
    verbose ``DEBUG`` messages produced during agent execution.

    This is a global, process-wide change and takes effect immediately.
    """
    from agno.utils.log import set_log_level_to_info

    set_log_level_to_info()
