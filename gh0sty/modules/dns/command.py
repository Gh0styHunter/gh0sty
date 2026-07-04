"""CLI command interface for the dns module."""

import argparse

from gh0sty.modules.base import BaseModule
from gh0sty.modules.dns.resolver import DnsResolver


class DnsCommand(BaseModule):
    """Subcommand to execute DNS record lookups on a target host."""

    help_summary = "Resolve standard DNS records (A, AAAA, MX, TXT, etc.)"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures the argparse arguments for the dns subcommand."""
        parser.add_argument(
            "-t", "--target", required=True, help="Target domain name or IP address"
        )
        parser.add_argument(
            "-r",
            "--record",
            default="all",
            help="Specific record type (A, AAAA, MX, TXT, NS, SOA, CNAME, PTR) or 'all' (Default: all)",
        )
        parser.add_argument("-o", "--output", help="Target filename path to save raw data")
        parser.add_argument(
            "-f",
            "--format",
            choices=["json", "csv", "html", "md", "pdf", "txt", "xml"],
            help="Export format type for the report",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the DNS query module."""
        resolver = DnsResolver()
        resolver.run(args)
