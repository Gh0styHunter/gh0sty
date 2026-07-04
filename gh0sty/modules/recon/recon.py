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
                f"Alvo inválido: '{raw_target}'"
            )

        logger.info("Iniciando auditoria...")

        session = ScanSession(module_name="recon", target=target)
        timer = Timer()
        timer.start()

        # 1. Passive collection
        collector = ReconCollector()
        recon_data = collector.gather_metadata(target)

        # 2. Port scan (top 5 essential ports for quick recon consolidation)
        logger.info("Verificando portas TCP...")
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
                logger.info("Gerando relatório...")
                generator = ReportGenerator(
                    session_dict=session.to_dict(), module_name="recon", target=target
                )
                generator.generate(out_format, args.output)
                console.print(
                    f"\n[bold green]Relatório gerado em: {args.output}[/bold green]"
                )
            except Exception as e:
                logger.error(f"Falha ao gerar relatório: {e}")
                raise ScanError(f"Falha ao gerar relatório: {e}") from e

    def _display_summary(self, target: str, data: dict[str, Any], duration: float) -> None:
        """Presents consolidated recon results in panels."""
        dns = data.get("dns_records", {})
        ptr_val = data.get("reverse_dns", "None")
        ptr_display = "Não encontrado" if ptr_val in ["None", "none", None] else ptr_val

        ports = data.get("open_ports", [])
        ports_list = [str(p.get("port")) for p in ports]
        ports_display = ", ".join(ports_list) if ports_list else "Nenhuma detectada"

        dns_lines = []
        for rtype, records in dns.items():
            if records:
                dns_lines.append(f"  [bold green]{rtype}:[/bold green] {', '.join(records)}")
        dns_infra_str = "\n" + "\n".join(dns_lines) if dns_lines else ""

        summary_text = (
            f"DNS Reverso (PTR):      {ptr_display}\n"
            f"Portas TCP abertas:     {ports_display}\n"
            f"Tempo de execução:      {duration:.2f} segundos"
        )
        if dns_infra_str.strip():
            summary_text += f"\n\n[bold green]Infraestrutura DNS:[/bold green]{dns_infra_str}"

        panel = Panel(summary_text, border_style="cyan", title="Resumo do Reconhecimento", expand=False)
        console.print(panel)
