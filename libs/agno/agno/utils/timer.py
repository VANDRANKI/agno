from time import perf_counter
from typing import Any, Dict, Optional


class Timer:
    """Timer class for timing code execution"""

    def __init__(self):
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.elapsed_time: Optional[float] = None

    @property
    def elapsed(self) -> float:
        """Return the elapsed time in seconds.

        If the timer has been stopped, returns the recorded `elapsed_time`.
        If the timer is still running, returns the time elapsed since `start()`.
        Returns 0.0 if the timer was never started.
        """
        return self.elapsed_time or (perf_counter() - self.start_time) if self.start_time else 0.0

    def start(self) -> float:
        self.start_time = perf_counter()
        return self.start_time

    def stop(self) -> float:
        self.end_time = perf_counter()
        if self.start_time is not None:
            self.elapsed_time = self.end_time - self.start_time
        return self.end_time

    def __enter__(self) -> "Timer":
        self.start_time = perf_counter()
        return self

    def __exit__(self, *args) -> None:
        self.end_time = perf_counter()
        if self.start_time is not None:
            self.elapsed_time = self.end_time - self.start_time

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the timer's start time, end time, and elapsed duration to a dict."""
        return {
            "start_time": str(self.start_time) if self.start_time is not None else None,
            "end_time": str(self.end_time) if self.end_time is not None else None,
            "elapsed": self.elapsed,
        }
