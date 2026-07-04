"""Core business logic for inspecting HTTP web applications."""

import argparse
from typing import Any

import httpx
from rich.panel import Panel
from rich.table import Table

import gh0sty.utils.http as http_util
import gh0sty.utils.network as net
from gh0sty.core.config import config_manager
from gh0sty.core.exceptions import ScanError, ValidationError
from gh0sty.core.logger import logger
from gh0sty.core.output import console
from gh0sty.core.session import ScanSession
from gh0sty.modules.web.fingerprint import fingerprint_web_technologies
from gh0sty.modules.web.headers import SECURITY_HEADERS
from gh0sty.utils.validators import clean_target, is_valid_domain, is_valid_ip


class WebApplicationAnalyzer:
    """Orchestrates HTTP audit scans on authorized targets."""

    def run(self, args: argparse.Namespace) -> None:
        """Executes the web application analysis.

        Args:
            args: CLI Namespace arguments.
        """
        raw_target = args.target
        url = raw_target

        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"

        host = clean_target(raw_target)
        if not is_valid_domain(host) and not is_valid_ip(host):
            raise ValidationError(
                f"Host alvo inválido detectado a partir de '{raw_target}'. Verifique o formato."
            )

        logger.info(f"URL Alvo: [bold cyan]{url}[/bold cyan] (Host: {host})")

        timeout = config_manager.get("timeout")
        session = ScanSession(module_name="web", target=host)
        results: dict[str, Any] = {
            "initial_target": raw_target,
            "url": url,
            "host": host,
            "http_status": None,
            "server": "Unknown",
            "redirects": [],
            "headers": {},
            "security_headers": {},
            "cookies": [],
            "ssl_info": {"supported": False},
            "technologies": [],
        }

        logger.info(f"Enviando requisição HTTP GET (tempo limite={timeout}s)...")
        try:
            # Call http utility wrapper
            response = http_util.fetch_url(url, timeout=timeout, verify_ssl=False)

            results["http_status"] = response.status_code
            results["server"] = response.headers.get("Server", "Unknown")

            for resp in response.history:
                results["redirects"].append(
                    {
                        "status_code": resp.status_code,
                        "url": str(resp.url),
                        "location": resp.headers.get("location", ""),
                    }
                )

            results["headers"] = dict(response.headers)

            for header in SECURITY_HEADERS:
                val = response.headers.get(header)
                results["security_headers"][header] = {
                    "present": val is not None,
                    "value": val or "",
                }

            for name, cookie in response.cookies.items():
                cookie_data = {
                    "name": name,
                    "value": cookie,
                    "domain": cookie.domain if hasattr(cookie, "domain") else "",
                    "path": cookie.path if hasattr(cookie, "path") else "",
                    "secure": cookie.secure if hasattr(cookie, "secure") else False,
                    "httponly": False,
                    "samesite": "None",
                }
                if hasattr(cookie, "has_nonstandard_attr"):
                    cookie_data["httponly"] = cookie.has_nonstandard_attr("HttpOnly")
                results["cookies"].append(cookie_data)

            results["technologies"] = fingerprint_web_technologies(
                results["headers"], results["cookies"]
            )

        except httpx.HTTPError as e:
            logger.warning(f"A requisição HTTP GET encontrou um erro: {e}")
            results["error"] = str(e)
            if url.startswith("https://") and not raw_target.startswith("https://"):
                fallback_url = url.replace("https://", "http://")
                logger.info(
                    f"Tentando fallback para não criptografado: [yellow]{fallback_url}[/yellow]..."
                )
                try:
                    response = http_util.fetch_url(fallback_url, timeout=timeout, verify_ssl=False)
                    results["http_status"] = response.status_code
                    results["server"] = response.headers.get("Server", "Unknown")
                    results["headers"] = dict(response.headers)
                    for header in SECURITY_HEADERS:
                        val = response.headers.get(header)
                        results["security_headers"][header] = {
                            "present": val is not None,
                            "value": val or "",
                        }
                    results["technologies"] = fingerprint_web_technologies(results["headers"], [])
                except Exception as ex:
                    logger.error(f"A requisição de fallback falhou: {ex}")
        except Exception as e:
            logger.error(f"Falha ao concluir a inspeção HTTP: {e}")
            results["error"] = str(e)

        if url.startswith("https://") or "https" in [r["url"] for r in results["redirects"]]:
            logger.info("Extraindo detalhes do certificado TLS...")
            ssl_details = net.get_ssl_details(host, timeout=timeout)
            results["ssl_info"] = ssl_details

        session.results = results
        self._display_summary(results)

        if args.output:
            out_format = args.format or "json"
            from gh0sty.modules.report.manager import ReportGenerator

            try:
                generator = ReportGenerator(
                    session_dict=session.to_dict(), module_name="web", target=host
                )
                generator.generate(out_format, args.output)
                console.print(
                    f"\n[bold green]Relatório exportado com sucesso para {args.output} ({out_format})[/bold green]"
                )
            except Exception as e:
                logger.error(f"Falha ao gerar a exportação do relatório: {e}")
                raise ScanError(f"Falha na geração do relatório: {e}") from e

    def _display_summary(self, results: dict[str, Any]) -> None:
        """Presents webinfo audit results in rich panels and tables."""
        if results.get("error") and not results.get("http_status"):
            console.print(
                f"[bold red]A Auditoria Web Falhou:[/bold red] Não foi possível concluir a requisição HTTP. "
                f"Detalhes: {results['error']}"
            )
            return

        status = results.get("http_status", "Failed")
        status_display = "Falhou" if status == "Failed" else status
        server = results.get("server", "Unknown")
        server_display = "Desconhecido" if server == "Unknown" else server
        techs_str = ", ".join(results.get("technologies", [])) or "Nenhuma Identificada"

        summary_text = (
            f"[bold green]Status HTTP Final:[/bold green] [cyan]{status_display}[/cyan]\n"
            f"[bold green]Cabeçalho Server:[/bold green] {server_display}\n"
            f"[bold green]Tecnologias Estimadas:[/bold green] {techs_str}"
        )
        panel = Panel(
            summary_text,
            title="Informações Básicas da Aplicação Web",
            border_style="cyan",
            expand=False,
        )
        console.print(panel)

        if results.get("redirects"):
            console.print("\n[bold cyan]Cadeia de Redirecionamento:[/bold cyan]")
            flow = []
            for r in results["redirects"]:
                flow.append(f"[yellow]{r['status_code']}[/yellow] {r['url']}")
            flow.append(f"[green]{status_display}[/green] {results['url']}")
            console.print("  -> ".join(flow))

        headers_table = Table(title="Status dos Cabeçalhos de Segurança", border_style="cyan")
        headers_table.add_column("Cabeçalho de Segurança", style="bold green")
        headers_table.add_column("Presença", style="white")
        headers_table.add_column("Valor / Diretiva", style="white")

        for key, val in results.get("security_headers", {}).items():
            presence = (
                "[bold green]Presente[/bold green]"
                if val["present"]
                else "[bold red]Ausente[/bold red]"
            )
            headers_table.add_row(key, presence, val["value"])

        console.print(headers_table)

        if results.get("cookies"):
            cookies_table = Table(title="Auditoria de Cookies da Aplicação", border_style="cyan")
            cookies_table.add_column("Nome do Cookie", style="bold green")
            cookies_table.add_column("Fragmento do Valor", style="white")
            cookies_table.add_column("Seguro", style="white")
            cookies_table.add_column("HttpOnly", style="white")

            for c in results["cookies"]:
                val_snippet = c["value"][:15] + "..." if len(c["value"]) > 15 else c["value"]
                secure_lbl = (
                    "[bold green]Sim[/bold green]" if c["secure"] else "[yellow]Não[/yellow]"
                )
                httponly_lbl = (
                    "[bold green]Sim[/bold green]" if c["httponly"] else "[yellow]Não[/yellow]"
                )
                cookies_table.add_row(c["name"], val_snippet, secure_lbl, httponly_lbl)

            console.print(cookies_table)

        ssl_info = results.get("ssl_info", {})
        if ssl_info.get("supported"):
            cert = ssl_info.get("certificate", {})
            subject_display = "Desconhecido" if cert.get('subject') == "Unknown" else cert.get('subject')
            issuer_display = "Desconhecido" if cert.get('issuer') == "Unknown" else cert.get('issuer')
            valid_to_display = "Desconhecido" if cert.get('valid_to') == "Unknown" else cert.get('valid_to')
            ssl_text = (
                f"[bold green]Versão do TLS:[/bold green] {ssl_info.get('tls_version')}\n"
                f"[bold green]Suíte de Cifragem:[/bold green] {ssl_info.get('cipher_name')} ({ssl_info.get('cipher_bits')} bits)\n"
                f"[bold green]Assunto (CN):[/bold green] [cyan]{subject_display}[/cyan]\n"
                f"[bold green]Emissor:[/bold green] {issuer_display}\n"
                f"[bold green]Dias Restantes:[/bold green] {cert.get('days_remaining')} (Válido até {valid_to_display})"
            )
            ssl_panel = Panel(
                ssl_text, title="Informações do Certificado SSL/TLS", border_style="cyan", expand=False
            )
            console.print(ssl_panel)
        elif ssl_info.get("error"):
            console.print(
                f"\n[bold yellow]Consulta SSL/TLS ignorada ou falhou:[/bold yellow] {ssl_info['error']}"
            )
        else:
            console.print(
                "\n[bold yellow]Nenhum detalhe de SSL/TLS obtido (conexão HTTP).[/bold yellow]"
            )
