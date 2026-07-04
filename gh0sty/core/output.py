"""Rich console output wrapper and helper formatters."""

from rich.console import Console
from rich.panel import Panel

from typing import Literal

# Shared Rich Console
console = Console()


def print_panel(
    text: str,
    title: str,
    style: str = "cyan",
    title_align: Literal["left", "center", "right"] = "left",
) -> None:
    """Prints a styled Rich Panel card.

    Args:
        text: Inner text content.
        title: Title of the panel.
        style: Border style color.
        title_align: Align mode (left, center, right).
    """
    panel = Panel(text, title=title, title_align=title_align, border_style=style, expand=False)
    console.print(panel)


def print_success(message: str) -> None:
    """Prints a standardized success message."""
    console.print(f"[bold green]Sucesso:[/bold green] {message}")


def print_error(message: str) -> None:
    """Prints a standardized error message."""
    console.print(f"[bold red]Erro:[/bold red] {message}")


def print_warning(message: str) -> None:
    """Prints a standardized warning message."""
    console.print(f"[bold yellow]Aviso:[/bold yellow] {message}")
