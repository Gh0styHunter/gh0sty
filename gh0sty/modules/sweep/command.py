"""CLI command interface for the sweep module."""

import argparse

from gh0sty.modules.base import BaseModule
from gh0sty.modules.sweep.scanner import WebSweepScanner


class SweepCommand(BaseModule):
    """Subcommand to execute path and endpoint sweep inventory mappings."""

    help_summary = "Perform scans/mapping of authorized web targets structures"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures subparser flags for web sweep mapping."""
        parser.add_argument(
            "-t", "--target", required=True, help="Target URL (e.g. https://example.com/)"
        )
        parser.add_argument("-w", "--wordlist", help="Path to dictionary wordlist file")
        parser.add_argument("-o", "--output", help="Target filename path to save findings")
        parser.add_argument(
            "-f",
            "--format",
            choices=["json", "csv", "html", "md", "pdf", "txt", "xml"],
            help="Export format type",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the web resources sweep process."""
        scanner = WebSweepScanner()
        scanner.run(args)
