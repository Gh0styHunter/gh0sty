"""CLI command interface for the scan module."""

import argparse

from gh0sty.modules.base import BaseModule
from gh0sty.modules.scan.scanner import AssetScanner


class ScanCommand(BaseModule):
    """Subcommand to execute port scans and host verification audits."""

    help_summary = "Faz o inventário das informações do host alvo e varre portas TCP abertas"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures the argparse arguments for the scan subcommand."""
        parser.add_argument("-t", "--target", required=True, help="Hostname ou endereço IP do alvo")
        parser.add_argument(
            "-p",
            "--ports",
            default="common",
            help="Portas separadas por vírgula ou intervalo (ex. 80,443,22-25) ou 'common' (Padrão: common)",
        )
        parser.add_argument("-o", "--output", help="Caminho do arquivo de destino para salvar os dados brutos")
        parser.add_argument(
            "-f",
            "--format",
            choices=["json", "csv", "html", "md", "pdf", "txt", "xml"],
            help="Tipo de formato de exportação para o relatório",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the asset scanning process."""
        scanner = AssetScanner()
        scanner.run(args)
