"""XML report writer implementation."""

from pathlib import Path
from typing import Any


class XMLWriter:
    """Writes scan outputs in XML formats."""

    def write(
        self, path: Path, data: dict[str, Any], module_name: str, target: str, timestamp: str
    ) -> None:
        """Saves a structured XML representation of findings."""
        xml = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<report module="{module_name}" target="{target}" timestamp="{timestamp}">',
        ]

        def dict_to_xml(d: Any, indent: int = 1) -> str:
            lines = []
            spaces = "  " * indent
            if isinstance(d, dict):
                for k, v in d.items():
                    # Clean tag name (must start with letter, no brackets, spaces, colons)
                    tag = str(k).replace(" ", "_").replace(":", "_").replace("-", "_").lower()
                    if isinstance(v, (dict, list)):
                        lines.append(f"{spaces}<{tag}>")
                        lines.append(dict_to_xml(v, indent + 1))
                        lines.append(f"{spaces}</{tag}>")
                    else:
                        clean_v = (
                            str(v).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                        )
                        lines.append(f"{spaces}<{tag}>{clean_v}</{tag}>")
            elif isinstance(d, list):
                for idx, item in enumerate(d):
                    lines.append(f'{spaces}<item index="{idx}">')
                    lines.append(dict_to_xml(item, indent + 1))
                    lines.append(f"{spaces}</item>")
            else:
                clean_val = str(d).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                lines.append(f"{spaces}{clean_val}")
            return "\n".join(lines)

        xml.append(dict_to_xml(data))
        xml.append("</report>")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(xml))
