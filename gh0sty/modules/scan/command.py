"""CLI command interface for the scan module."""

import argparse

from gh0sty.modules.base import BaseModule
from gh0sty.modules.scan.scanner import AssetScanner


class ScanCommand(BaseModule):
    """Subcommand to execute port scans and host verification audits."""

    help_summary = "Inventory target host info and scan open TCP ports"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures the argparse arguments for the scan subcommand."""
        parser.add_argument("-t", "--target", required=True, help="Target hostname or IP address")
        parser.add_argument(
            "-p",
            "--ports",
            default="common",
            help="Comma-separated ports or range (e.g. 80,443,22-25) or 'common' (Default: common)",
        )
        parser.add_argument("-o", "--output", help="Target filename path to save raw data")
        parser.add_argument(
            "-f",
            "--format",
            choices=["json", "csv", "html", "md", "pdf", "txt", "xml"],
            help="Export format type for the report",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the asset scanning process."""
        scanner = AssetScanner()
        scanner.run(args)
