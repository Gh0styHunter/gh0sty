"""CLI command interface for the web module."""

import argparse

from gh0sty.modules.base import BaseModule
from gh0sty.modules.web.analyzer import WebApplicationAnalyzer


class WebCommand(BaseModule):
    """Subcommand to audit authorized HTTP applications and fetch security details."""

    help_summary = "Audit web applications (headers, redirects, cookies, SSL/TLS, tech)"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures the argparse arguments for the web subcommand."""
        parser.add_argument(
            "-t", "--target", required=True, help="Target URL, domain name or IP address"
        )
        parser.add_argument("-o", "--output", help="Target filename path to save raw data")
        parser.add_argument(
            "-f",
            "--format",
            choices=["json", "csv", "html", "md", "pdf", "txt", "xml"],
            help="Export format type for the report",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the web application audit."""
        analyzer = WebApplicationAnalyzer()
        analyzer.run(args)
