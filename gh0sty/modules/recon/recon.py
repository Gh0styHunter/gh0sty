"""Core business logic for consolidating recon audits."""

import argparse
from typing import Any

from rich.panel import Panel

import gh0sty.utils.network as net
from gh0sty.core.config import config_manager
from gh0sty.core.exceptions import ScanError, ValidationError
from gh0sty.core.logger import logger
from gh0sty.core.output import console
from gh0sty.core.session import ScanSession
from gh0sty.modules.recon.collector import ReconCollector
from gh0sty.utils.timer import Timer
from gh0sty.utils.validators import clean_target, is_valid_domain, is_valid_ip


class ReconCoordinator:
    """Consolidates findings from DNS, socket scans, and web applications audits."""

    def run(self, args: argparse.Namespace) -> None:
        """Executes passive collection and active scans on target."""
        raw_target = args.target
        target = clean_target(raw_target)

        is_ip = is_valid_ip(target)
        is_domain = is_valid_domain(target)

        if not is_ip and not is_domain:
            raise ValidationError(
                f"Formato de alvo inválido: '{raw_target}'. Deve ser um domínio ou endereço IP válido."
            )

        logger.info(
            f"Iniciando auditoria consolidada de reconhecimento para o alvo: [bold cyan]{target}[/bold cyan]"
        )

        session = ScanSession(module_name="recon", target=target)
        timer = Timer()
        timer.start()

        # 1. Passive collection
        collector = ReconCollector()
        recon_data = collector.gather_metadata(target)

        # 2. Port scan (top 5 essential ports for quick recon consolidation)
        logger.info("Executando varredura básica de portas ativas...")
        resolved_ips = [target]
        if is_domain:
            res = net.resolve_host(target)
            resolved_ips = res["ipv4"] + res["ipv6"]

        open_ports = []
        essential_ports = [22, 80, 443, 8080, 8443]
        timeout = config_manager.get("timeout")
        for ip in resolved_ips[:2]:  # Limit IPs to keep recon quick
            for port in essential_ports:
                finding = net.scan_port(ip, port, timeout)
                if finding:
                    open_ports.append(finding)

        recon_data["open_ports"] = open_ports
        duration = timer.stop()

        # Display Summary
        self._display_summary(target, recon_data, duration)

        session.results = {
            "target": target,
            "duration_seconds": duration,
            "recon_metadata": recon_data,
        }

        if args.output:
            out_format = args.format or "json"
            from gh0sty.modules.report.manager import ReportGenerator

            try:
                generator = ReportGenerator(
                    session_dict=session.to_dict(), module_name="recon", target=target
                )
                generator.generate(out_format, args.output)
                console.print(
                    f"\n[bold green]Relatório exportado com sucesso para {args.output} ({out_format})[/bold green]"
                )
            except Exception as e:
                logger.error(f"Falha ao gerar a exportação do relatório: {e}")
                raise ScanError(f"Falha na geração do relatório: {e}") from e

    def _display_summary(self, target: str, data: dict[str, Any], duration: float) -> None:
        """Presents consolidated recon results in panels."""
        dns = data.get("dns_records", {})
        dns_lines = []
        for rtype, records in dns.items():
            if records:
                dns_lines.append(f"  [bold green]{rtype}:[/bold green] {', '.join(records)}")
        dns_str = (
            "\n".join(dns_lines) if dns_lines else f"  Host Reverso: {data.get('reverse_dns')}"
        )

        ports = data.get("open_ports", [])
        ports_lines = []
        for p in ports:
            ports_lines.append(
                f"  - IP: {p.get('ip')} | Port: {p.get('port')} | Service: {p.get('service')}"
            )
        ports_str = "\n".join(ports_lines) if ports_lines else "  Nenhuma porta padrão aberta detectada."

        summary_text = (
            f"[bold cyan]Resultados consolidados de Recon para {target}[/bold cyan]\n\n"
            f"[bold green]Base da Infraestrutura DNS:[/bold green]\n{dns_str}\n\n"
            f"[bold green]Portas TCP Essenciais Abertas:[/bold green]\n{ports_str}\n\n"
            f"[bold green]Tempo de execução:[/bold green] {duration:.2f} segundos"
        )
        panel = Panel(summary_text, border_style="cyan", title="Reconhecimento Básico", expand=False)
        console.print(panel)
