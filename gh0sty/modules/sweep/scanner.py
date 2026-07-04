"""Web application path structure and resource mapping scanner."""

import argparse
from typing import Any

import httpx
from rich.table import Table

import gh0sty.utils.threads as threads_util
from gh0sty.core.config import config_manager
from gh0sty.core.exceptions import ScanError
from gh0sty.core.logger import logger
from gh0sty.core.output import console
from gh0sty.core.session import ScanSession
from gh0sty.modules.sweep.filters import filter_sweep_results
from gh0sty.modules.sweep.wordlist import load_wordlist
from gh0sty.utils.timer import Timer


class WebSweepScanner:
    """Orchestrates resource sweeps across web assets."""

    def run(self, args: argparse.Namespace) -> None:
        """Executes the concurrent path search."""
        target = args.target
        if not target.startswith("http://") and not target.startswith("https://"):
            target = f"https://{target}"

        # Clean trailing slash issues
        if not target.endswith("/"):
            target += "/"

        logger.info("Executando varredura web...")

        # Load paths wordlist
        paths = load_wordlist(args.wordlist)
        logger.info(f"Lista de {len(paths)} caminhos carregada.")

        threads = config_manager.get("threads")
        timeout = config_manager.get("timeout")
        session = ScanSession(module_name="sweep", target=target)

        # Worker tasks
        tasks = [target + p for p in paths]

        timer = Timer()
        timer.start()

        def worker(url_task: str) -> Any:
            try:
                # Use HEAD requests for speed sweeps
                with httpx.Client(timeout=timeout, verify=False) as client:
                    resp = client.head(url_task, follow_redirects=False)
                    return {
                        "url": url_task,
                        "status_code": resp.status_code,
                        "length": resp.headers.get("Content-Length", "0"),
                    }
            except Exception:
                return None

        # Execute
        raw_results = threads_util.run_concurrently(
            tasks=tasks,
            worker_func=worker,
            max_workers=threads,
            description="Varredura de Diretórios",
        )

        duration = timer.stop()
        logger.debug(f"Sweep concluído em {duration:.2f} segundos.")

        # Aggregate findings
        findings: list[dict[str, Any]] = [res for res in raw_results if res is not None]

        # Apply default filter (remove 404s)
        active_findings = filter_sweep_results(findings, [])

        self._display_results(active_findings)

        session.results = {
            "target": target,
            "scan_duration_seconds": duration,
            "total_endpoints_tested": len(paths),
            "findings": active_findings,
        }

        if args.output:
            out_format = args.format or "json"
            from gh0sty.modules.report.manager import ReportGenerator

            try:
                logger.info("Gerando relatório...")
                generator = ReportGenerator(
                    session_dict=session.to_dict(), module_name="sweep", target=target
                )
                generator.generate(out_format, args.output)
                console.print(
                    f"\n[bold green]Relatório gerado em: {args.output}[/bold green]"
                )
            except Exception as e:
                logger.error(f"Falha ao gerar relatório: {e}")
                raise ScanError(f"Falha ao gerar relatório: {e}") from e

    def _display_results(self, findings: list[dict[str, Any]]) -> None:
        """Presents active web sweep outcomes in a table."""
        if not findings:
            console.print(
                "\n[bold yellow]Nenhum diretório encontrado.[/bold yellow]"
            )
            return

        table = Table(
            title=f"Diretórios Encontrados ({len(findings)})",
            border_style="cyan",
        )
        table.add_column("URL", style="cyan")
        table.add_column("Status", style="bold green", justify="center")
        table.add_column("Tamanho (Bytes)", style="white", justify="right")

        for f in findings:
            status = f.get("status_code", 0)
            status_style = "bold green" if status == 200 else "yellow"
            table.add_row(
                f.get("url"),
                f"[{status_style}]{status}[/{status_style}]",
                str(f.get("length", "0")),
            )

        console.print(table)
