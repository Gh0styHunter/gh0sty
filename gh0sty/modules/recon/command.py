"""CLI command interface for the recon module."""

import argparse

from gh0sty.modules.base import BaseModule
from gh0sty.modules.recon.recon import ReconCoordinator


class ReconCommand(BaseModule):
    """Subcommand to execute consolidated reconnaissance scans on assets."""

    help_summary = "Consolida descobertas ativas e passivas em ativos alvo"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures subparser flags for reconnaissance audits."""
        parser.add_argument("-t", "--target", required=True, help="Domínio alvo ou IP do host")
        parser.add_argument("-o", "--output", help="Caminho para salvar as varreduras consolidadas")
        parser.add_argument(
            "-f",
            "--format",
            choices=["json", "csv", "html", "md", "pdf", "txt", "xml"],
            help="Tipo de formato de exportação",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the consolidated recon mapping process."""
        recon = ReconCoordinator()
        recon.run(args)
