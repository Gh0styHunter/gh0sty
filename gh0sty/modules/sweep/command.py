"""CLI command interface for the sweep module."""

import argparse

from gh0sty.modules.base import BaseModule
from gh0sty.modules.sweep.scanner import WebSweepScanner


class SweepCommand(BaseModule):
    """Subcommand to execute path and endpoint sweep inventory mappings."""

    help_summary = "Realiza varreduras/mapeamento de estruturas de alvos web autorizados"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures subparser flags for web sweep mapping."""
        parser.add_argument(
            "-t", "--target", required=True, help="URL do alvo (ex. https://exemplo.com/)"
        )
        parser.add_argument("-w", "--wordlist", help="Caminho para o arquivo de lista de palavras (wordlist)")
        parser.add_argument("-o", "--output", help="Caminho do arquivo de destino para salvar as descobertas")
        parser.add_argument(
            "-f",
            "--format",
            choices=["json", "csv", "html", "md", "pdf", "txt", "xml"],
            help="Tipo de formato de exportação",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the web resources sweep process."""
        scanner = WebSweepScanner()
        scanner.run(args)
