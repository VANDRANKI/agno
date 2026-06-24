import logging


def enable_debug_mode() -> None:
    """Enable debug mode for the agno library.

    Sets the logging level to DEBUG, which produces more verbose output
    including internal state transitions and model call details.

    Example:
        >>> import agno
        >>> agno.enable_debug_mode()
    """
    from agno.utils.log import set_log_level_to_debug

    set_log_level_to_debug()


def disable_debug_mode() -> None:
    """Disable debug mode for the agno library.

    Resets the logging level to INFO, which is the default for production
    use. Call this after a debugging session to reduce log verbosity.

    Example:
        >>> import agno
        >>> agno.disable_debug_mode()
    """
    from agno.utils.log import set_log_level_to_info

    set_log_level_to_info()


def toggle_debug_mode() -> bool:
    """Toggle the debug mode for the agno library.

    If debug mode is currently enabled (logging level is DEBUG), this
    function disables it (resets to INFO). If disabled, it enables it.

    Returns:
        True if debug mode is enabled after the call, False if disabled.

    Example:
        >>> import agno
        >>> is_debug = agno.toggle_debug_mode()
        >>> print(f"Debug mode is now {'on' if is_debug else 'off'}")
    """
    from agno.utils.log import logger

    if logger.level == logging.DEBUG:
        disable_debug_mode()
        return False
    enable_debug_mode()
    return True
