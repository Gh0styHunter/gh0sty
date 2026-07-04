"""Core business logic for target asset validation and TCP port scanning."""

import argparse
from typing import Any

from rich.panel import Panel
from rich.table import Table

import gh0sty.utils.network as net
from gh0sty.core.config import config_manager
from gh0sty.core.exceptions import ScanError, ValidationError
from gh0sty.core.logger import logger
from gh0sty.core.output import console
from gh0sty.core.session import ScanSession
from gh0sty.utils.threads import run_concurrently
from gh0sty.utils.timer import Timer
from gh0sty.utils.validators import clean_target, is_valid_domain, is_valid_ip, parse_ports


class AssetScanner:
    """Orchestrates asset port connectivity auditing scans."""

    def run(self, args: argparse.Namespace) -> None:
        """Runs the target port scan execution sequence.

        Args:
            args: Parsed CLI namespace arguments.
        """
        raw_target = args.target
        target = clean_target(raw_target)

        is_ip = is_valid_ip(target)
        is_domain = is_valid_domain(target)

        if not is_ip and not is_domain:
            raise ValidationError(
                f"Alvo inválido: '{raw_target}'"
            )

        try:
            ports = parse_ports(args.ports)
        except ValidationError as e:
            logger.error(str(e))
            raise

        logger.info("Coletando informações do alvo...")

        resolved_ips: list[str] = []
        hostname: str = "Desconhecido"

        if is_ip:
            resolved_ips.append(target)
            resolved_host = net.reverse_resolve(target)
            if resolved_host:
                hostname = resolved_host
                logger.info("Coletando informações do alvo...")
            else:
                logger.debug("DNS reverso não retornou nenhum hostname.")
        else:
            hostname = target
            resolution = net.resolve_host(target)
            resolved_ips.extend(resolution["ipv4"])
            resolved_ips.extend(resolution["ipv6"])

            if not resolved_ips:
                raise ScanError(f"Falha na resolução de DNS para '{target}'")

            logger.debug(
                f"IPs resolvidos para o domínio: " f"IPv4={resolution['ipv4']}, IPv6={resolution['ipv6']}"
            )

        self._print_target_panel(target, hostname, resolved_ips)

        threads = config_manager.get("threads")
        timeout = config_manager.get("timeout")
        logger.info("Verificando portas TCP...")

        tasks: list[tuple[str, int]] = []
        for ip in resolved_ips:
            for port in ports:
                tasks.append((ip, port))

        timer = Timer()
        timer.start()

        def worker(task: tuple[str, int]) -> Any:
            ip_addr, port_num = task
            return net.scan_port(ip_addr, port_num, timeout)

        scan_results = run_concurrently(
            tasks=tasks,
            worker_func=worker,
            max_workers=threads,
            description="Varredura de Portas TCP",
        )

        duration = timer.stop()
        logger.debug(f"Varredura concluída em {duration:.2f} segundos.")

        open_ports: list[dict[str, Any]] = [res for res in scan_results if res is not None]

        self._display_results(open_ports, duration)

        session = ScanSession(module_name="scan", target=target)
        session.results = {
            "target": target,
            "hostname": hostname,
            "ips": resolved_ips,
            "scan_info": {
                "duration_seconds": duration,
                "ports_scanned": len(ports),
                "threads_used": threads,
                "timeout": timeout,
            },
            "open_ports": open_ports,
        }

        if args.output:
            out_format = args.format or "json"
            from gh0sty.modules.report.manager import ReportGenerator

            try:
                logger.info("Gerando relatório...")
                generator = ReportGenerator(
                    session_dict=session.to_dict(), module_name="scan", target=target
                )
                generator.generate(out_format, args.output)
                console.print(
                    f"\n[bold green]Relatório gerado em: {args.output}[/bold green]"
                )
            except Exception as e:
                logger.error(f"Falha ao gerar relatório: {e}")
                raise ScanError(f"Falha ao gerar relatório: {e}") from e

    def _print_target_panel(self, target: str, hostname: str, resolved_ips: list[str]) -> None:
        """Presents summary metadata about the resolved asset."""
        ips_str = ", ".join(resolved_ips)
        panel_content = (
            f"[bold green]Alvo:[/bold green] {target}\n"
            f"[bold green]Hostname:[/bold green] {hostname}\n"
            f"[bold green]IPs:[/bold green] {ips_str}"
        )
        panel = Panel(
            panel_content,
            border_style="cyan",
            title="Informações Coletadas",
            expand=False,
        )
        console.print(panel)

    def _display_results(self, open_ports: list[dict[str, Any]], duration: float) -> None:
        """Renders open ports details in a clean table."""
        if not open_ports:
            console.print("\n[bold yellow]Nenhuma porta aberta encontrada.[/bold yellow]")
            return

        table = Table(
            title=f"Portas Abertas ({len(open_ports)} encontradas)",
            border_style="cyan",
        )
        table.add_column("IP", style="cyan")
        table.add_column("Porta", style="bold green", justify="right")
        table.add_column("Estado", style="bold white")
        table.add_column("Serviço", style="white")

        for entry in open_ports:
            state_display = "aberta" if entry["state"] == "open" else entry["state"]
            table.add_row(
                entry.get("ip", "desconhecido"),
                str(entry["port"]),
                state_display,
                entry["service"],
            )

        console.print(table)
