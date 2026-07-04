"""Wordlist loading and normalization utilities."""

from pathlib import Path

# Standard default paths to test on web applications
DEFAULT_PATHS = [
    "robots.txt",
    "sitemap.xml",
    "admin/",
    "login/",
    "api/",
    "uploads/",
    "static/",
    ".env",
    ".git/",
    "index.html",
]


def load_wordlist(file_path: str | None = None) -> list[str]:
    """Loads a wordlist from file or falls back to top common paths.

    Args:
        file_path: Optional path to a dictionary file.

    Returns:
        List of path strings.
    """
    if not file_path:
        return DEFAULT_PATHS.copy()

    path = Path(file_path)
    if not path.exists():
        return DEFAULT_PATHS.copy()

    try:
        with open(path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except Exception:
        return DEFAULT_PATHS.copy()
