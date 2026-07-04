"""Session tracking helper mapping target scans metadata and outputs."""

from datetime import UTC, datetime
from typing import Any


class ScanSession:
    """Maintains target details, timestamps, and findings of an execution session."""

    def __init__(self, module_name: str, target: str) -> None:
        """Initializes target scanning metadata parameters.

        Args:
            module_name: Originating module name.
            target: Target host or domain string.
        """
        self.module_name = module_name
        self.target = target
        self.timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        self.results: dict[str, Any] = {}

    def to_dict(self) -> dict[str, Any]:
        """Dumps metadata and raw results mapping into standard dictionaries."""
        return {
            "metadata": {
                "module": self.module_name,
                "target": self.target,
                "timestamp": self.timestamp,
            },
            "results": self.results,
        }
