"""Normalizing formatters for CLI logs and text outputs."""

from datetime import UTC, datetime


def format_bytes(size_bytes: int) -> str:
    """Formats numeric bytes size to human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes //= 1024
    return f"{size_bytes:.2f} TB"


def get_utc_timestamp() -> str:
    """Returns standard ISO formatting for active session logging."""
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
