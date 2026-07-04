"""Core business logic for resolving DNS records."""

import argparse
from typing import Any

from rich.table import Table

import gh0sty.utils.dns as dns_util
from gh0sty.core.exceptions import ScanError, ValidationError
from gh0sty.core.logger import logger
from gh0sty.core.output import console
from gh0sty.core.session import ScanSession
from gh0sty.modules.dns.records import SUPPORTED_RECORDS
from gh0sty.utils.validators import clean_target, is_valid_domain, is_valid_ip


class DnsResolver:
    """Orchestrates DNS name records and reverse IP lookups."""

    def run(self, args: argparse.Namespace) -> None:
        """Runs the query execution sequence based on parsed command args.

        Args:
            args: CLI parsed command Namespace.
        """
        raw_target = args.target
        target = clean_target(raw_target)

        is_ip = is_valid_ip(target)
        is_domain = is_valid_domain(target)

        if not is_ip and not is_domain:
            raise ValidationError(
                f"Alvo inválido: '{raw_target}'. Deve ser um domínio ou endereço IP válido."
            )

        logger.info(f"Iniciando consultas DNS para o alvo: [bold cyan]{target}[/bold cyan]")

        req_record = args.record.upper()
        records_to_query = []
        if req_record == "ALL":
            records_to_query = SUPPORTED_RECORDS.copy()
        elif req_record in SUPPORTED_RECORDS:
            records_to_query = [req_record]
        else:
            raise ValidationError(
                f"Tipo de registro não suportado: '{args.record}'. Suportados: {', '.join(SUPPORTED_RECORDS)} ou 'all'"
            )

        results: dict[str, Any] = {}
        session = ScanSession(module_name="dns", target=target)

        if is_ip:
            if "PTR" in records_to_query:
                results["PTR"] = dns_util.resolve_ptr_record(target)
                records_to_query.remove("PTR")
            if records_to_query:
                ptr_resolved = dns_util.resolve_ptr_record(target)
                if ptr_resolved:
                    resolved_domain = ptr_resolved[0].rstrip(".")
                    logger.info(
                        f"IP {target} resolvido para o domínio [cyan]{resolved_domain}[/cyan]. Executando outras consultas..."
                    )
                    for rtype in records_to_query:
                        results[rtype] = dns_util.resolve_dns_record(resolved_domain, rtype)
                else:
                    logger.warning(f"Não foi possível realizar a resolução reversa de {target} para executar outras consultas DNS.")
                    for rtype in records_to_query:
                        results[rtype] = []
        else:
            for rtype in records_to_query:
                if rtype == "PTR":
                    a_ips = dns_util.resolve_dns_record(target, "A")
                    aaaa_ips = dns_util.resolve_dns_record(target, "AAAA")
                    ptr_results = []
                    for ip in a_ips + aaaa_ips:
                        ptr_results.extend(dns_util.resolve_ptr_record(ip))
                    results["PTR"] = ptr_results
                else:
                    results[rtype] = dns_util.resolve_dns_record(target, rtype)

        session.results = results

        # Display results
        self._display_results(target, results)

        # Handle file export if requested
        if args.output:
            out_format = args.format or "json"
            from gh0sty.modules.report.manager import ReportGenerator

            try:
                generator = ReportGenerator(
                    session_dict=session.to_dict(), module_name="dns", target=target
                )
                generator.generate(out_format, args.output)
                console.print(
                    f"\n[bold green]Relatório exportado com sucesso para {args.output} ({out_format})[/bold green]"
                )
            except Exception as e:
                logger.error(f"Falha ao gerar a exportação do relatório: {e}")
                raise ScanError(f"Falha na geração do relatório: {e}") from e

    def _display_results(self, target: str, results: dict[str, list[str]]) -> None:
        """Presents resolved DNS records in a formatted table."""
        table = Table(title=f"Registros DNS para {target}", border_style="cyan")
        table.add_column("Tipo de Registro", style="bold green", width=15)
        table.add_column("Valor / Saída Resolvida", style="white")

        for rtype, records in results.items():
            if records:
                for idx, record in enumerate(records):
                    label = rtype if idx == 0 else ""
                    table.add_row(label, record)
            else:
                table.add_row(rtype, "[dim yellow]Nenhum registro encontrado[/dim yellow]")

        console.print(table)
