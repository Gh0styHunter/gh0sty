"""Markdown report writer implementation."""

from pathlib import Path
from typing import Any

from gh0sty.core.constants import DEFAULT_TEMPLATES_DIR
from gh0sty.core.exceptions import ReportError


class MarkdownWriter:
    """Compiles Markdown report templates using structured findings."""

    def write(
        self, path: Path, data: dict[str, Any], module_name: str, target: str, timestamp: str
    ) -> None:
        """Renders Markdown report placeholders."""
        template_file = DEFAULT_TEMPLATES_DIR / "markdown" / "report.md"
        if not template_file.exists():
            raise ReportError(f"Markdown report template file is missing: {template_file}")

        with open(template_file, encoding="utf-8") as f:
            template = f.read()

        content = self._generate_markdown_content(data, module_name)
        markdown = template.replace("{{TARGET}}", target)
        markdown = markdown.replace("{{MODULE}}", module_name.upper())
        markdown = markdown.replace("{{TIMESTAMP}}", timestamp)
        markdown = markdown.replace("{{CONTENT}}", content)

        with open(path, "w", encoding="utf-8") as f:
            f.write(markdown)

    def _generate_markdown_content(self, data: dict[str, Any], module: str) -> str:
        """Compiles formatted markdown strings based on the scanning command findings."""
        blocks: list[str] = []
        mod = module.lower()

        if mod in ["scan", "inventory"]:
            ips = ", ".join(data.get("ips", []))
            blocks.append(
                f"## Asset Inventory Summary\n\n"
                f"- **Target Name:** `{data.get('target')}`\n"
                f"- **Resolved Hostname:** `{data.get('hostname')}`\n"
                f"- **Resolved IPs:** `{ips}`\n"
                f"- **Scan Time:** `{data.get('scan_info', {}).get('duration_seconds', 0):.2f} seconds`\n"
            )

            ports = data.get("open_ports", [])
            ports_table = [
                "## Active Open Ports\n",
                "| IP Address | Port | State | Service |",
                "| --- | --- | --- | --- |",
            ]
            for p in ports:
                ports_table.append(
                    f"| {p.get('ip')} | {p.get('port')} | {p.get('state')} | {p.get('service')} |"
                )

            if not ports:
                ports_table.append("| - | - | No Open Ports Found | - |")

            blocks.append("\n".join(ports_table))

        elif mod in ["web", "webinfo"]:
            status = data.get("http_status", "Error")
            server = data.get("server", "Unknown")
            techs = ", ".join(data.get("technologies", [])) or "None identified"

            blocks.append(
                f"## HTTP Audit Profile\n\n"
                f"- **Target URL:** `{data.get('url')}`\n"
                f"- **Final HTTP Status:** `{status}`\n"
                f"- **Server Signature:** `{server}`\n"
                f"- **Identified Technologies:** `{techs}`\n"
            )

            redirects = data.get("redirects", [])
            if redirects:
                redirect_flow = []
                for r in redirects:
                    redirect_flow.append(f"[{r.get('status_code')}] {r.get('url')}")
                redirect_flow.append(f"[{status}] {data.get('url')}")
                blocks.append("### HTTP Redirect Flow\n\n" + " -> ".join(redirect_flow) + "\n")

            headers_table = [
                "### Security Headers Status\n",
                "| Security Header | Status | Configuration Directive |",
                "| --- | --- | --- |",
            ]
            for header, details in data.get("security_headers", {}).items():
                status_lbl = "PRESENT" if details.get("present") else "MISSING"
                headers_table.append(
                    f"| **{header}** | {status_lbl} | `{details.get('value') or '-'}` |"
                )
            blocks.append("\n".join(headers_table))

            cookies = data.get("cookies", [])
            if cookies:
                cookies_table = [
                    "\n### Cookie Security Audit\n",
                    "| Cookie Name | Secure Flag | HttpOnly Flag | Domain Scope |",
                    "| --- | --- | --- | --- |",
                ]
                for c in cookies:
                    sec = "YES" if c.get("secure") else "NO"
                    http = "YES" if c.get("httponly") else "NO"
                    cookies_table.append(
                        f"| `{c.get('name')}` | {sec} | {http} | `{c.get('domain')}` |"
                    )
                blocks.append("\n".join(cookies_table))

            ssl = data.get("ssl_info", {})
            if ssl.get("supported"):
                cert = ssl.get("certificate", {})
                blocks.append(
                    f"\n### SSL/TLS Certificate Metadata\n\n"
                    f"- **TLS Protocol:** `{ssl.get('tls_version')}`\n"
                    f"- **Cipher Suite:** `{ssl.get('cipher_name')} ({ssl.get('cipher_bits')} bits)`\n"
                    f"- **Subject Common Name (CN):** `{cert.get('subject')}`\n"
                    f"- **Issuer CA:** `{cert.get('issuer')}`\n"
                    f"- **Validation Period:** Valid from `{cert.get('valid_from')}` to `{cert.get('valid_to')}`\n"
                    f"- **Time Remaining:** `{cert.get('days_remaining')} days` (Expired: `{cert.get('expired')}`)\n"
                )

        elif mod == "dns":
            dns_table = [
                "## Resolved Record Values\n",
                "| Record Type | Resolved Target Value |",
                "| --- | --- |",
            ]
            for rtype, records in data.items():
                if records:
                    for record in records:
                        dns_table.append(f"| **{rtype}** | `{record}` |")
                else:
                    dns_table.append(f"| **{rtype}** | *No records found* |")
            blocks.append("\n".join(dns_table))

        else:
            # General fallback
            blocks.append("## Raw Scan Results\n")
            for key, val in data.items():
                blocks.append(f"- **{key}:** {val}")

        return "\n".join(blocks)
