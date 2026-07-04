"""Logging configuration module for the gh0sty framework."""

import logging

from rich.logging import RichHandler

from gh0sty.core.constants import DEFAULT_LOGS_DIR

LOG_FILE = DEFAULT_LOGS_DIR / "gh0sty.log"
logger = logging.getLogger("gh0sty")


def setup_logging(verbose: bool = False) -> None:
    """Configures system-wide logging.

    Args:
        verbose: If True, set logging level to DEBUG. Otherwise, INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO

    # Set root logger level
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if setup is called multiple times
    if logger.handlers:
        logger.handlers.clear()

    # Console Handler using Rich
    console_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_path=False,
    )
    console_handler.setLevel(level)
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File Handler
    try:
        DEFAULT_LOGS_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # Always log everything to file
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Falha ao inicializar escrita de logs em arquivo: {e}")
