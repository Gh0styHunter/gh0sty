"""Execution duration tracking helper."""

import time
from collections.abc import Generator
from contextlib import contextmanager


class Timer:
    """Calculates elapsed seconds of operations."""

    def __init__(self) -> None:
        self.start_time = time.time()
        self.end_time = 0.0

    def start(self) -> None:
        """Starts the timer."""
        self.start_time = time.time()
        self.end_time = 0.0

    def stop(self) -> float:
        """Stops the timer and returns duration in seconds."""
        self.end_time = time.time()
        return self.duration

    @property
    def duration(self) -> float:
        """Returns elapsed time in seconds."""
        if self.end_time > 0.0:
            return self.end_time - self.start_time
        return time.time() - self.start_time


@contextmanager
def time_execution() -> Generator[Timer, None, None]:
    """Context manager to measure block execution durations."""
    timer = Timer()
    yield timer
    timer.stop()
