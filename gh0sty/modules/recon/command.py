"""CLI command interface for the recon module."""

import argparse

from gh0sty.modules.base import BaseModule
from gh0sty.modules.recon.recon import ReconCoordinator


class ReconCommand(BaseModule):
    """Subcommand to execute consolidated reconnaissance scans on assets."""

    help_summary = "Consolidate active and passive findings on target assets"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures subparser flags for reconnaissance audits."""
        parser.add_argument("-t", "--target", required=True, help="Target domain name or host IP")
        parser.add_argument("-o", "--output", help="Path to save the consolidated scans")
        parser.add_argument(
            "-f",
            "--format",
            choices=["json", "csv", "html", "md", "pdf", "txt", "xml"],
            help="Export format type",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the consolidated recon mapping process."""
        recon = ReconCoordinator()
        recon.run(args)
