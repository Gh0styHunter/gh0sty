"""CLI command interface to render custom system helps."""

import argparse

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from gh0sty.modules.base import BaseModule

console = Console()


class HelpCommand(BaseModule):
    """Subcommand providing custom styled general or module-specific help."""

    help_summary = "Show custom system help or module specific commands usage"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures the argparse arguments for the help subcommand."""
        parser.add_argument(
            "module_name",
            nargs="?",
            choices=["scan", "sweep", "recon", "web", "dns", "report", "config", "help"],
            help="Show detailed usage for a specific module command",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the help command."""
        if args.module_name:
            self.display_module_help(args.module_name)
        else:
            self.display_general_help()

    @staticmethod
    def display_general_help() -> None:
        """Prints a styled list of all available commands and options."""
        console.print("[bold cyan]Usage:[/bold cyan]")
        console.print("  gh0sty <command> [options]\n")

        console.print("[bold cyan]Global Options:[/bold cyan]")
        console.print("  -h, --help     Show this help message and exit")
        console.print("  -v, --verbose  Enable verbose (DEBUG) log messages\n")

        # Modules list table
        table = Table(title="Available Commands", border_style="cyan", box=None)
        table.add_column("Command", style="bold green", width=15)
        table.add_column("Description", style="white")

        table.add_row("scan", "Perform authorized asset scans (host resolve, TCP port checks)")
        table.add_row("sweep", "Perform scans/mapping of authorized web targets structures")
        table.add_row("recon", "Consolidate active and passive findings on target assets")
        table.add_row(
            "web", "Inspect HTTP/HTTPS application security configurations, TLS and cookies"
        )
        table.add_row("dns", "Query standard DNS records (A, AAAA, MX, TXT, NS, etc.)")
        table.add_row(
            "report", "Compile raw JSON scan outputs to HTML, MD, CSV, JSON, PDF, TXT or XML"
        )
        table.add_row(
            "config", "Show and update local options (threads, output dir, timeout, etc.)"
        )
        table.add_row("help", "Display general help or usage details for a specific command")

        console.print(table)
        console.print(
            "\nUse [bold yellow]gh0sty help <command>[/bold yellow] to view detailed help for that module."
        )

    def display_module_help(self, cmd: str) -> None:
        """Shows styled detailed help and examples for a module.

        Args:
            cmd: Command name.
        """
        panel_content = ""

        if cmd == "scan":
            panel_content = (
                "[bold green]Command:[/bold green] gh0sty scan\n"
                "[bold green]Description:[/bold green] Scans authorized hosts for active state and open TCP ports.\n\n"
                "[bold cyan]Options:[/bold cyan]\n"
                "  -t, --target  Target hostname or IP address (Required)\n"
                "  -p, --ports   Comma-separated ports or range (e.g. 80,443,22-25) or 'common' (Default: common)\n"
                "  -o, --output  Target filename path to save raw data\n"
                "  -f, --format  Direct export format: json, csv, html, md, pdf, txt, xml (Default: none)\n\n"
                "[bold cyan]Examples:[/bold cyan]\n"
                "  gh0sty scan -t example.com\n"
                "  gh0sty scan -t 192.168.1.10 -p 22,80,443 -f html -o scan.html\n"
            )
        elif cmd == "sweep":
            panel_content = (
                "[bold green]Command:[/bold green] gh0sty sweep\n"
                "[bold green]Description:[/bold green] Maps resource files, directory paths or endpoints of a web target.\n\n"
                "[bold cyan]Options:[/bold cyan]\n"
                "  -t, --target  Target web application URL (Required)\n"
                "  -w, --wordlist Path to custom dictionary wordlist file\n"
                "  -o, --output  Target filename path to save data\n"
                "  -f, --format  Direct export format type (Default: none)\n\n"
                "[bold cyan]Examples:[/bold cyan]\n"
                "  gh0sty sweep -t https://example.com/ -w common.txt\n"
            )
        elif cmd == "recon":
            panel_content = (
                "[bold green]Command:[/bold green] gh0sty recon\n"
                "[bold green]Description:[/bold green] Runs consolidated DNS, TCP, and web audits on an authorized host target.\n\n"
                "[bold cyan]Options:[/bold cyan]\n"
                "  -t, --target  Target domain or host IP (Required)\n"
                "  -o, --output  Path to save the consolidated scans\n"
                "  -f, --format  Export format type (Default: none)\n\n"
                "[bold cyan]Examples:[/bold cyan]\n"
                "  gh0sty recon -t example.com -f html -o reports/recon_domain.html\n"
            )
        elif cmd == "web":
            panel_content = (
                "[bold green]Command:[/bold green] gh0sty web\n"
                "[bold green]Description:[/bold green] Audits HTTP headers, redirection paths, cookie flags, and SSL cert details.\n\n"
                "[bold cyan]Options:[/bold cyan]\n"
                "  -t, --target  Target URL or domain (e.g. example.com or https://example.com) (Required)\n"
                "  -o, --output  Target filename path to save raw data\n"
                "  -f, --format  Direct export format type (Default: none)\n\n"
                "[bold cyan]Examples:[/bold cyan]\n"
                "  gh0sty web -t example.com\n"
                "  gh0sty web -t https://localhost:8443 -f json -o output.json\n"
            )
        elif cmd == "dns":
            panel_content = (
                "[bold green]Command:[/bold green] gh0sty dns\n"
                "[bold green]Description:[/bold green] Resolves domain records for the target host.\n\n"
                "[bold cyan]Options:[/bold cyan]\n"
                "  -t, --target  Target domain to query (Required)\n"
                "  -r, --record  Record type (A, AAAA, MX, TXT, NS, SOA, CNAME, PTR) or 'all' (Default: all)\n"
                "  -o, --output  Target filename path to save data\n"
                "  -f, --format  Direct export format type (Default: none)\n\n"
                "[bold cyan]Examples:[/bold cyan]\n"
                "  gh0sty dns -t google.com\n"
                "  gh0sty dns -t cloudflare.com -r MX -f md -o mx_records.md\n"
            )
        elif cmd == "report":
            panel_content = (
                "[bold green]Command:[/bold green] gh0sty report\n"
                "[bold green]Description:[/bold green] Compiles saved JSON scan results to other formats.\n\n"
                "[bold cyan]Options:[/bold cyan]\n"
                "  -i, --input   Source raw JSON scan output file (Required)\n"
                "  -f, --format  Format type (json, csv, html, md, pdf, txt, xml) (Required)\n"
                "  -o, --output  Target filename path to save compiled report (Required)\n\n"
                "[bold cyan]Examples:[/bold cyan]\n"
                "  gh0sty report -i raw_data.json -f html -o full_report.html\n"
            )
        elif cmd == "config":
            panel_content = (
                "[bold green]Command:[/bold green] gh0sty config\n"
                "[bold green]Description:[/bold green] Manages system configuration options.\n\n"
                "[bold cyan]Options:[/bold cyan]\n"
                "  --show        Print all configs\n"
                "  --set         Update configuration parameter\n"
            )
        elif cmd == "help":
            panel_content = (
                "[bold green]Command:[/bold green] gh0sty help\n"
                "[bold green]Description:[/bold green] Display system help or subcommand details.\n\n"
                "[bold cyan]Usage:[/bold cyan]\n"
                "  gh0sty help [command_name]\n"
            )

        panel = Panel(
            panel_content, border_style="cyan", title=f"Command Help: {cmd}", title_align="left"
        )
        console.print(panel)
