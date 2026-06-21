"""High-resolution wall-clock timer for measuring code execution time.

Provides a simple :class:`Timer` that can be used either as an explicit
start/stop pair or as a context manager::

    # Explicit usage
    t = Timer()
    t.start()
    do_work()
    t.stop()
    print(t.elapsed)  # seconds as float

    # Context manager
    with Timer() as t:
        do_work()
    print(t.elapsed)
"""

from time import perf_counter
from typing import Any, Dict, Optional


class Timer:
    """Wall-clock timer backed by :func:`time.perf_counter`.

    Supports both explicit ``start()``/``stop()`` calls and the context-manager
    protocol.  While the timer is running (started but not stopped), reading
    :attr:`elapsed` returns the time since :meth:`start` was called; after
    :meth:`stop` it returns the final measured duration.

    Attributes:
        start_time: ``perf_counter`` value recorded at :meth:`start`, or
            ``None`` if the timer has not been started.
        end_time: ``perf_counter`` value recorded at :meth:`stop`, or
            ``None`` if the timer has not been stopped.
        elapsed_time: Final measured duration in seconds, set only after
            :meth:`stop` (or ``__exit__``) is called.

    Example::

        with Timer() as t:
            result = expensive_call()
        print(f"Took {t.elapsed:.3f}s")
    """

    def __init__(self) -> None:
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.elapsed_time: Optional[float] = None

    @property
    def elapsed(self) -> float:
        """Elapsed time in seconds.

        Returns the final duration if the timer has been stopped, the time
        since :meth:`start` was called if the timer is still running, or
        ``0.0`` if the timer has never been started.
        """
        if self.elapsed_time is not None:
            return self.elapsed_time
        if self.start_time is not None:
            return perf_counter() - self.start_time
        return 0.0

    def start(self) -> float:
        """Start (or restart) the timer.

        Returns:
            The ``perf_counter`` value at the moment the timer was started.
        """
        self.start_time = perf_counter()
        return self.start_time

    def stop(self) -> float:
        """Stop the timer and record the elapsed duration.

        Returns:
            The ``perf_counter`` value at the moment the timer was stopped.
        """
        self.end_time = perf_counter()
        if self.start_time is not None:
            self.elapsed_time = self.end_time - self.start_time
        return self.end_time

    def __enter__(self) -> "Timer":
        self.start_time = perf_counter()
        return self

    def __exit__(self, *args: Any) -> None:
        self.end_time = perf_counter()
        if self.start_time is not None:
            self.elapsed_time = self.end_time - self.start_time

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the timer state to a plain dictionary.

        Returns:
            A dict with ``start_time``, ``end_time`` (both as strings or
            ``None``), and ``elapsed`` (float, seconds).
        """
        return {
            "start_time": str(self.start_time) if self.start_time is not None else None,
            "end_time": str(self.end_time) if self.end_time is not None else None,
            "elapsed": self.elapsed,
        }
