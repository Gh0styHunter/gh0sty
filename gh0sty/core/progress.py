"""Custom Rich progress bars helper for system tasks execution."""

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)


def create_progress_bar(description: str = "Executando...") -> Progress:
    """Instantiates a standardized Rich Progress instance.

    Args:
        description: Description text for the progress bar.

    Returns:
        Configure Rich Progress context manager object.
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    )
