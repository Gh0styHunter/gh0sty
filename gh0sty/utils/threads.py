"""Multi-threaded task runners executing tasks concurrently."""

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TypeVar

from gh0sty.core.progress import create_progress_bar

T = TypeVar("T")
R = TypeVar("R")


def run_concurrently(
    tasks: list[T],
    worker_func: Callable[[T], R],
    max_workers: int = 10,
    description: str = "Processando...",
) -> list[R]:
    """Runs tasks concurrently using ThreadPoolExecutor while displaying a Rich progress bar.

    Args:
        tasks: List of inputs/tasks to execute.
        worker_func: Callable worker executing a single task.
        max_workers: Maximum thread worker count.
        description: Description text for the progress bar.

    Returns:
        List of results returned by the worker_func.
    """
    results: list[R] = []
    if not tasks:
        return results

    progress = create_progress_bar(description)
    with progress:
        task_id = progress.add_task(description, total=len(tasks))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {executor.submit(worker_func, task): task for task in tasks}

            for future in as_completed(future_to_task):
                try:
                    result = future.result()
                    if result is not None:
                        results.append(result)
                except Exception:
                    # Exceptions are caught by caller or logged, we prevent thread pool crash
                    pass
                finally:
                    progress.update(task_id, advance=1)

    return results
