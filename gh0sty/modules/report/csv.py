"""CSV report writer implementation."""

import csv
from pathlib import Path
from typing import Any


class CSVWriter:
    """Writes scan outputs in tabular CSV formats."""

    def write(
        self, path: Path, data: dict[str, Any], module_name: str, target: str, timestamp: str
    ) -> None:
        """Formats scan findings into CSV rows."""
        # Standardize module name comparisons
        mod = module_name.lower()

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if mod in ["scan", "inventory"]:
                writer.writerow(["Target IP", "Port", "State", "Service"])
                open_ports = data.get("open_ports", [])
                for p in open_ports:
                    writer.writerow([p.get("ip"), p.get("port"), p.get("state"), p.get("service")])

            elif mod in ["web", "webinfo"]:
                writer.writerow(
                    ["Metric Category", "Parameter Name", "Value Details", "Audit Status"]
                )
                writer.writerow(["General", "URL", data.get("url"), ""])
                writer.writerow(["General", "HTTP Status", data.get("http_status"), ""])
                writer.writerow(["General", "Server Banner", data.get("server"), ""])
                writer.writerow(
                    ["General", "Technologies", ", ".join(data.get("technologies", [])), ""]
                )

                for header, val in data.get("security_headers", {}).items():
                    writer.writerow(
                        [
                            "Security Header",
                            header,
                            val.get("value"),
                            "Present" if val.get("present") else "Missing",
                        ]
                    )

                for cookie in data.get("cookies", []):
                    writer.writerow(
                        [
                            "Cookie",
                            cookie.get("name"),
                            f"Secure={cookie.get('secure')};HttpOnly={cookie.get('httponly')}",
                            "",
                        ]
                    )

                ssl = data.get("ssl_info", {})
                if ssl.get("supported"):
                    cert = ssl.get("certificate", {})
                    writer.writerow(["SSL/TLS", "Version", ssl.get("tls_version"), ""])
                    writer.writerow(["SSL/TLS", "Cipher", ssl.get("cipher_name"), ""])
                    writer.writerow(["SSL/TLS", "Common Name", cert.get("subject"), ""])
                    writer.writerow(
                        [
                            "SSL/TLS",
                            "Days Left",
                            cert.get("days_remaining"),
                            "Expired" if cert.get("expired") else "Active",
                        ]
                    )

            elif mod == "dns":
                writer.writerow(["Record Type", "Resolved Output"])
                for rtype, records in data.items():
                    for record in records:
                        writer.writerow([rtype, record])

            else:
                # General key-value CSV output fallback
                writer.writerow(["Key", "Value"])
                for key, val in data.items():
                    writer.writerow([key, str(val)])
