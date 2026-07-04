"""CLI command interface for the web module."""

import argparse

from gh0sty.modules.base import BaseModule
from gh0sty.modules.web.analyzer import WebApplicationAnalyzer


class WebCommand(BaseModule):
    """Subcommand to audit authorized HTTP applications and fetch security details."""

    help_summary = "Audita aplicações web (cabeçalhos, redirecionamentos, cookies, SSL/TLS, tecnologias)"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures the argparse arguments for the web subcommand."""
        parser.add_argument(
            "-t", "--target", required=True, help="URL, domínio ou endereço IP do alvo"
        )
        parser.add_argument("-o", "--output", help="Caminho do arquivo de destino para salvar os dados brutos")
        parser.add_argument(
            "-f",
            "--format",
            choices=["json", "csv", "html", "md", "pdf", "txt", "xml"],
            help="Tipo de formato de exportação para o relatório",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the web application audit."""
        analyzer = WebApplicationAnalyzer()
        analyzer.run(args)
