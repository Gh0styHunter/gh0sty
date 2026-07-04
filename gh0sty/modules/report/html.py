"""HTML report writer implementation."""

from pathlib import Path
from typing import Any

from gh0sty.core.constants import DEFAULT_TEMPLATES_DIR
from gh0sty.core.exceptions import ReportError


class HTMLWriter:
    """Compiles HTML report templates using structured findings."""

    def write(
        self, path: Path, data: dict[str, Any], module_name: str, target: str, timestamp: str
    ) -> None:
        """Renders HTML report placeholders."""
        template_file = DEFAULT_TEMPLATES_DIR / "html" / "report.html"
        if not template_file.exists():
            raise ReportError(f"HTML report template file is missing: {template_file}")

        with open(template_file, encoding="utf-8") as f:
            template = f.read()

        content = self._generate_html_content(data, module_name, target)
        html = template.replace("{{TARGET}}", target)
        html = html.replace("{{MODULE}}", module_name.upper())
        html = html.replace("{{TIMESTAMP}}", timestamp)
        html = html.replace("{{CONTENT}}", content)

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    def _generate_html_content(self, data: dict[str, Any], module: str, target: str) -> str:
        """Assembles HTML blocks based on the active scanning module findings."""
        blocks: list[str] = []
        mod = module.lower()

        if mod in ["scan", "inventory"]:
            ips = ", ".join(data.get("ips", []))
            blocks.append(
                f'<div class="panel">\n'
                f'  <h2 class="panel-title">Asset Information</h2>\n'
                f'  <div class="summary-card"><span class="summary-label">Target Name:</span> <span>{data.get("target", target)}</span></div>\n'
                f'  <div class="summary-card"><span class="summary-label">Resolved Hostname:</span> <span>{data.get("hostname")}</span></div>\n'
                f'  <div class="summary-card"><span class="summary-label">Identified IPs:</span> <span>{ips}</span></div>\n'
                f'  <div class="summary-card"><span class="summary-label">Scan Duration:</span> <span>{data.get("scan_info", {}).get("duration_seconds", 0):.2f} seconds</span></div>\n'
                f"</div>"
            )

            ports_rows = []
            open_ports = data.get("open_ports", [])
            for p in open_ports:
                ports_rows.append(
                    f"<tr>\n"
                    f'  <td>{p.get("ip")}</td>\n'
                    f'  <td><strong>{p.get("port")}</strong></td>\n'
                    f'  <td><span class="badge badge-success">{p.get("state")}</span></td>\n'
                    f'  <td>{p.get("service")}</td>\n'
                    f"</tr>"
                )

            table_body = (
                "\n".join(ports_rows)
                if ports_rows
                else '<tr><td colspan="4" style="text-align: center;">No open ports identified.</td></tr>'
            )
            blocks.append(
                f'<div class="panel">\n'
                f'  <h2 class="panel-title">Active TCP Service Ports</h2>\n'
                f"  <table>\n"
                f"    <thead>\n"
                f"      <tr><th>IP Address</th><th>Port</th><th>State</th><th>Service</th></tr>\n"
                f"    </thead>\n"
                f"    <tbody>\n"
                f"      {table_body}\n"
                f"    </tbody>\n"
                f"  </table>\n"
                f"</div>"
            )

        elif mod in ["web", "webinfo"]:
            status = data.get("http_status", "Error/Inaccessible")
            server = data.get("server", "Unknown")
            techs = ", ".join(data.get("technologies", [])) or "None Identified"

            blocks.append(
                f'<div class="panel">\n'
                f'  <h2 class="panel-title">Web Application Basic Information</h2>\n'
                f'  <div class="summary-card"><span class="summary-label">Final URL:</span> <span>{data.get("url")}</span></div>\n'
                f'  <div class="summary-card"><span class="summary-label">HTTP Status Code:</span> <span>{status}</span></div>\n'
                f'  <div class="summary-card"><span class="summary-label">Server Signature:</span> <span>{server}</span></div>\n'
                f'  <div class="summary-card"><span class="summary-label">Estimated Technologies:</span> <span>{techs}</span></div>\n'
                f"</div>"
            )

            redirects = data.get("redirects", [])
            if redirects:
                redirect_flow = []
                for r in redirects:
                    redirect_flow.append(
                        f'<span class="badge badge-warning">{r.get("status_code")}</span> '
                        f'<code style="font-size:0.9rem;">{r.get("url")}</code>'
                    )
                redirect_flow.append(
                    f'<span class="badge badge-success">{status}</span> '
                    f'<code style="font-size:0.9rem;">{data.get("url")}</code>'
                )
                flow_html = " &rarr; ".join(redirect_flow)
                blocks.append(
                    f'<div class="panel">\n'
                    f'  <h2 class="panel-title">HTTP Redirection Chain</h2>\n'
                    f"  <div>{flow_html}</div>\n"
                    f"</div>"
                )

            header_rows = []
            for header, details in data.get("security_headers", {}).items():
                badge_class = "badge-success" if details.get("present") else "badge-danger"
                presence_str = "Present" if details.get("present") else "Missing"
                val = details.get("value") or "-"
                header_rows.append(
                    f"<tr>\n"
                    f"  <td><strong>{header}</strong></td>\n"
                    f'  <td><span class="badge {badge_class}">{presence_str}</span></td>\n'
                    f"  <td><code>{val}</code></td>\n"
                    f"</tr>"
                )
            headers_body = "\n".join(header_rows)
            blocks.append(
                f'<div class="panel">\n'
                f'  <h2 class="panel-title">Security Headers Audit</h2>\n'
                f"  <table>\n"
                f"    <thead>\n"
                f"      <tr><th>Header Parameter</th><th>Status</th><th>Configuration Directive</th></tr>\n"
                f"    </thead>\n"
                f"    <tbody>\n"
                f"      {headers_body}\n"
                f"    </tbody>\n"
                f"  </table>\n"
                f"</div>"
            )

            cookies = data.get("cookies", [])
            if cookies:
                cookie_rows = []
                for c in cookies:
                    sec_cls = "badge-success" if c.get("secure") else "badge-warning"
                    sec_lbl = "Yes" if c.get("secure") else "No"
                    http_cls = "badge-success" if c.get("httponly") else "badge-warning"
                    http_lbl = "Yes" if c.get("httponly") else "No"
                    cookie_rows.append(
                        f"<tr>\n"
                        f"  <td><strong>{c.get('name')}</strong></td>\n"
                        f'  <td><span class="badge {sec_cls}">{sec_lbl}</span></td>\n'
                        f'  <td><span class="badge {http_cls}">{http_lbl}</span></td>\n'
                        f"  <td>{c.get('domain')}</td>\n"
                        f"</tr>"
                    )
                cookies_body = "\n".join(cookie_rows)
                blocks.append(
                    f'<div class="panel">\n'
                    f'  <h2 class="panel-title">HTTP Application Cookies</h2>\n'
                    f"  <table>\n"
                    f"    <thead>\n"
                    f"      <tr><th>Cookie Name</th><th>Secure Flag</th><th>HttpOnly Flag</th><th>Domain Scope</th></tr>\n"
                    f"    </thead>\n"
                    f"    <tbody>\n"
                    f"      {cookies_body}\n"
                    f"    </tbody>\n"
                    f"  </table>\n"
                    f"</div>"
                )

            ssl = data.get("ssl_info", {})
            if ssl.get("supported"):
                cert = ssl.get("certificate", {})
                exp_cls = "badge-danger" if cert.get("expired") else "badge-success"
                exp_lbl = "Expired" if cert.get("expired") else "Valid/Active"
                blocks.append(
                    f'<div class="panel">\n'
                    f'  <h2 class="panel-title">SSL/TLS Security Certificate</h2>\n'
                    f'  <div class="summary-card"><span class="summary-label">TLS Version:</span> <span>{ssl.get("tls_version")}</span></div>\n'
                    f'  <div class="summary-card"><span class="summary-label">Cipher Suite:</span> <span>{ssl.get("cipher_name")} ({ssl.get("cipher_bits")} bits)</span></div>\n'
                    f'  <div class="summary-card"><span class="summary-label">Subject CN:</span> <span>{cert.get("subject")}</span></div>\n'
                    f'  <div class="summary-card"><span class="summary-label">Issuer Authority:</span> <span>{cert.get("issuer")}</span></div>\n'
                    f'  <div class="summary-card"><span class="summary-label">Certificate Status:</span> <span class="badge {exp_cls}">{exp_lbl}</span></div>\n'
                    f'  <div class="summary-card"><span class="summary-label">Days Left:</span> <span>{cert.get("days_remaining")} (Valid to {cert.get("valid_to")})</span></div>\n'
                    f"</div>"
                )

        elif mod == "dns":
            dns_rows = []
            for rtype, records in data.items():
                if records:
                    for record in records:
                        dns_rows.append(
                            f"<tr>\n"
                            f'  <td><span class="badge badge-info">{rtype}</span></td>\n'
                            f"  <td><code>{record}</code></td>\n"
                            f"</tr>"
                        )
                else:
                    dns_rows.append(
                        f"<tr>\n"
                        f'  <td><span class="badge badge-warning">{rtype}</span></td>\n'
                        f'  <td style="color:#555; font-style:italic;">No records resolved.</td>\n'
                        f"</tr>"
                    )

            dns_body = "\n".join(dns_rows)
            blocks.append(
                f'<div class="panel">\n'
                f'  <h2 class="panel-title">Resolved Name Records</h2>\n'
                f"  <table>\n"
                f"    <thead>\n"
                f"      <tr><th>Record Type</th><th>Record Target Value</th></tr>\n"
                f"    </thead>\n"
                f"    <tbody>\n"
                f"      {dns_body}\n"
                f"    </tbody>\n"
                f"  </table>\n"
                f"</div>"
            )

        return "\n".join(blocks)
