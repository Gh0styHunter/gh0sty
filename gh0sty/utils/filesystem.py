"""Filesystem operations and directory path helper utilities."""

from pathlib import Path


def ensure_directory(path: str | Path) -> Path:
    """Ensures a directory path exists, creating parents if necessary.

    Args:
        path: Path object or string.

    Returns:
        Path object of the created directory.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_file(path: str | Path, content: str) -> None:
    """Writes textual content to a file, securing parent folder structures.

    Args:
        path: Output file target path.
        content: Text string content.
    """
    p = Path(path)
    ensure_directory(p.parent)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
