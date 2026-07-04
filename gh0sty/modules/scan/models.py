"""Data models representing port scan findings."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class PortFinding:
    """Represents a discovered TCP port state and its matched service."""

    ip: str
    port: int
    state: str
    service: str

    def to_dict(self) -> dict[str, Any]:
        """Converts finding parameters to dictionary format."""
        return asdict(self)
