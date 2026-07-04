"""TXT report writer implementation."""

from pathlib import Path
from typing import Any


class TXTWriter:
    """Writes scan outputs in plain text format."""

    def write(
        self, path: Path, data: dict[str, Any], module_name: str, target: str, timestamp: str
    ) -> None:
        """Saves a structured plain text representation of the findings."""
        lines = [
            "=== gh0sty Security Scan Report ===",
            f"Target: {target}",
            f"Module: {module_name.upper()}",
            f"Timestamp: {timestamp}",
            "===================================\n",
        ]

        if module_name.lower() in ["scan", "inventory"]:
            lines.append("Active Open Ports:")
            open_ports = data.get("open_ports", [])
            for p in open_ports:
                lines.append(
                    f"  - IP: {p.get('ip')} | Port: {p.get('port')} | State: {p.get('state')} | Service: {p.get('service')}"
                )
            if not open_ports:
                lines.append("  No open ports found.")

        elif module_name.lower() in ["web", "webinfo"]:
            lines.append(f"URL: {data.get('url')}")
            lines.append(f"Status: {data.get('http_status')}")
            lines.append(f"Server: {data.get('server')}")
            lines.append(f"Technologies: {', '.join(data.get('technologies', []))}")
            lines.append("\nSecurity Headers:")
            for header, details in data.get("security_headers", {}).items():
                pres = "PRESENT" if details.get("present") else "MISSING"
                lines.append(f"  - {header}: {pres} ({details.get('value') or '-'})")

            cookies = data.get("cookies", [])
            if cookies:
                lines.append("\nCookies:")
                for c in cookies:
                    lines.append(
                        f"  - {c.get('name')} (Secure: {c.get('secure')} | HttpOnly: {c.get('httponly')})"
                    )

            ssl = data.get("ssl_info", {})
            if ssl.get("supported"):
                cert = ssl.get("certificate", {})
                lines.append("\nSSL/TLS Info:")
                lines.append(f"  Version: {ssl.get('tls_version')}")
                lines.append(f"  Cipher: {ssl.get('cipher_name')}")
                lines.append(f"  Subject CN: {cert.get('subject')}")
                lines.append(f"  Issuer: {cert.get('issuer')}")
                lines.append(f"  Days Remaining: {cert.get('days_remaining')}")

        elif module_name.lower() == "dns":
            lines.append("Resolved Records:")
            for rtype, records in data.items():
                if records:
                    for record in records:
                        lines.append(f"  - {rtype}: {record}")
                else:
                    lines.append(f"  - {rtype}: (none)")

        else:
            lines.append(str(data))

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
