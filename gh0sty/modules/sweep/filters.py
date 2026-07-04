"""Result filtering utilities sorting HTTP status responses."""

from typing import Any


def filter_sweep_results(
    results: list[dict[str, Any]], status_codes: list[int]
) -> list[dict[str, Any]]:
    """Filters web resource endpoints matches based on response status codes.

    Args:
        results: Raw sweep findings.
        status_codes: Status code integers to include.

    Returns:
        Filtered list of results.
    """
    if not status_codes:
        # Default filter: remove typical 404 Not Found responses
        return [r for r in results if r.get("status_code") != 404]
    return [r for r in results if r.get("status_code") in status_codes]
