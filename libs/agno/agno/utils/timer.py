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
        """Return the elapsed time in seconds, computing it on the fly if the timer is still running."""
        return self.elapsed_time or (perf_counter() - self.start_time) if self.start_time else 0.0

    def start(self) -> float:
        """Start the timer and return the start timestamp."""
        self.start_time = perf_counter()
        return self.start_time

    def stop(self) -> float:
        """Stop the timer, record the elapsed time, and return the end timestamp."""
        self.end_time = perf_counter()
        if self.start_time is not None:
            self.elapsed_time = self.end_time - self.start_time
        return self.end_time

    def __enter__(self) -> "Timer":
        """Start the timer when entering a `with` block."""
        self.start_time = perf_counter()
        return self

    def __exit__(self, *args) -> None:
        """Stop the timer and record the elapsed time when exiting a `with` block."""
        self.end_time = perf_counter()
        if self.start_time is not None:
            self.elapsed_time = self.end_time - self.start_time

    def to_dict(self) -> Dict[str, Any]:
        """Return the timer's start time, end time, and elapsed time as a dictionary."""
        return {
            "start_time": str(self.start_time) if self.start_time is not None else None,
            "end_time": str(self.end_time) if self.end_time is not None else None,
            "elapsed": self.elapsed,
        }
