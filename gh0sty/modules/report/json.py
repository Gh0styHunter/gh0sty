"""JSON report writer implementation."""

import json
from pathlib import Path
from typing import Any


class JSONWriter:
    """Writes scan outputs in standard structured JSON."""

    def write(
        self, path: Path, data: dict[str, Any], module_name: str, target: str, timestamp: str
    ) -> None:
        """Dumps dictionary content wrapped in standard metadata tags."""
        output = {
            "metadata": {
                "module": module_name,
                "target": target,
                "timestamp": timestamp,
            },
            "results": data,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)
