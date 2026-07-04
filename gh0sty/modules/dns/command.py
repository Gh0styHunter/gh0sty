"""CLI command interface for the dns module."""

import argparse

from gh0sty.modules.base import BaseModule
from gh0sty.modules.dns.resolver import DnsResolver


class DnsCommand(BaseModule):
    """Subcommand to execute DNS record lookups on a target host."""

    help_summary = "Resolve registros DNS padrão (A, AAAA, MX, TXT, etc.)"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures the argparse arguments for the dns subcommand."""
        parser.add_argument(
            "-t", "--target", required=True, help="Domínio ou endereço IP do alvo"
        )
        parser.add_argument(
            "-r",
            "--record",
            default="all",
            help="Tipo de registro específico (A, AAAA, MX, TXT, NS, SOA, CNAME, PTR) ou 'all' (Padrão: all)",
        )
        parser.add_argument("-o", "--output", help="Caminho do arquivo de destino para salvar os dados brutos")
        parser.add_argument(
            "-f",
            "--format",
            choices=["json", "csv", "html", "md", "pdf", "txt", "xml"],
            help="Tipo de formato de exportação para o relatório",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the DNS query module."""
        resolver = DnsResolver()
        resolver.run(args)
