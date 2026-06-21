"""Datetime utility helpers for parsing, converting, and retrieving timestamps.

All functions that return aware datetimes use UTC as the canonical timezone.
Functions that return naive datetimes (e.g. :func:`current_datetime`) do so
for compatibility with callers that require naive objects and should be treated
as local time by those callers.

Key helpers
-----------
- :func:`parse_datetime_utc` — parse a datetime or ISO 8601 string to UTC.
- :func:`to_epoch_s` — coerce int/float/str/datetime to epoch seconds.
- :func:`now_epoch_s` — current UTC time as integer epoch seconds.
- :func:`current_datetime_utc_str` — current UTC time as ``"YYYY-MM-DDTHH:MM:SS"``.
"""

from datetime import datetime, timezone
from typing import Any, Union


def parse_datetime_utc(value: Any) -> datetime:
    """Parse a datetime or ISO 8601 string and return a UTC-aware datetime.

    - datetime with tzinfo -> converted to UTC
    - datetime without tzinfo -> assumed UTC
    - str -> parsed via fromisoformat, then converted to UTC
    - Other types -> raises TypeError

    Args:
        value: A :class:`datetime.datetime` instance or an ISO 8601 string.
            The trailing ``"Z"`` suffix is normalised to ``"+00:00"`` before
            parsing so both forms are accepted.

    Returns:
        A timezone-aware :class:`datetime.datetime` in UTC.

    Raises:
        TypeError: If *value* is not a ``datetime`` or ``str``.
        ValueError: If a string cannot be parsed as ISO 8601.
    """
    if isinstance(value, datetime):
        if value.tzinfo is not None:
            return value.astimezone(timezone.utc)
        return value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        s = value.strip()
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is not None:
            return dt.astimezone(timezone.utc)
        return dt.replace(tzinfo=timezone.utc)
    raise TypeError(f"Unsupported datetime value: {type(value)}")


def current_datetime() -> datetime:
    """Return the current local date and time as a naive datetime.

    Returns:
        A naive :class:`datetime.datetime` representing the current local time.
        Use :func:`current_datetime_utc` when a timezone-aware UTC value is
        required.
    """
    return datetime.now()


def current_datetime_utc() -> datetime:
    """Return the current UTC date and time as a timezone-aware datetime.

    Returns:
        A :class:`datetime.datetime` with ``tzinfo=timezone.utc``.
    """
    return datetime.now(timezone.utc)


def current_datetime_utc_str() -> str:
    """Return the current UTC time formatted as an ISO 8601 string.

    Returns:
        A string of the form ``"YYYY-MM-DDTHH:MM:SS"`` in UTC (no timezone
        suffix, no microseconds).
    """
    return current_datetime_utc().strftime("%Y-%m-%dT%H:%M:%S")


def now_epoch_s() -> int:
    """Return the current UTC time as integer epoch seconds.

    Returns:
        The number of whole seconds elapsed since the Unix epoch
        (1970-01-01 00:00:00 UTC).
    """
    return int(datetime.now(timezone.utc).timestamp())


def to_epoch_s(value: Union[int, float, str, datetime]) -> int:
    """Normalise various datetime representations to integer epoch seconds (UTC).

    Args:
        value: The value to convert.  Supported types:

            - ``int`` or ``float`` — assumed to already be epoch seconds;
              truncated to int.
            - :class:`datetime.datetime` — naive datetimes are assumed UTC;
              aware datetimes are converted to UTC.
            - ``str`` — parsed as an ISO 8601 string; trailing ``"Z"`` is
              accepted; naive strings are assumed UTC.

    Returns:
        The corresponding UTC timestamp as an ``int`` (whole seconds).

    Raises:
        ValueError: If a string value cannot be parsed as ISO 8601.
        TypeError: If *value* is none of the supported types.
    """
    if isinstance(value, (int, float)):
        # Assume value is already in seconds
        return int(value)

    if isinstance(value, datetime):
        dt = value
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())

    if isinstance(value, str):
        s = value.strip()
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        try:
            dt = datetime.fromisoformat(s)
        except ValueError as e:
            raise ValueError(f"Unsupported datetime string: {value!r}") from e
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())

    raise TypeError(f"Unsupported datetime value: {type(value)}")
