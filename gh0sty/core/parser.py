"""Command Line parser configuration defining modules subparsers."""

import argparse
import sys

from gh0sty.core.banner import show_banner


def parse_arguments() -> argparse.Namespace:
    """Configures global parser options and hooks modules subparsers.

    Returns:
        argparse.Namespace holding parsed variables.
    """
    parser = argparse.ArgumentParser(
        description="gh0sty - Framework de Inventário e Auditoria de Segurança",
        add_help=False,
    )
    parser.add_argument("-h", "--help", action="store_true", help="exibe essa mensagem de ajuda")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Habilita mensagens de log detalhadas (DEBUG)"
    )

    subparsers = parser.add_subparsers(dest="command", title="Módulos disponíveis")

    # Local imports to prevent circular dependencies
    from gh0sty.modules.config.command import ConfigCommand
    from gh0sty.modules.dns.command import DnsCommand
    from gh0sty.modules.help.command import HelpCommand
    from gh0sty.modules.recon.command import ReconCommand
    from gh0sty.modules.report.manager import ReportCommand
    from gh0sty.modules.scan.command import ScanCommand
    from gh0sty.modules.sweep.command import SweepCommand
    from gh0sty.modules.web.command import WebCommand

    module_commands = {
        "scan": ScanCommand,
        "sweep": SweepCommand,
        "recon": ReconCommand,
        "web": WebCommand,
        "dns": DnsCommand,
        "report": ReportCommand,
        "config": ConfigCommand,
        "help": HelpCommand,
    }

    # Register each subcommand's parser arguments
    for cmd_name, cmd_class in module_commands.items():
        cmd_parser = subparsers.add_parser(cmd_name, help=cmd_class.help_summary, add_help=False)
        cmd_parser.add_argument("-h", "--help", action="help", help="exibe essa mensagem de ajuda")
        cmd_class.configure_parser(cmd_parser)

    # Direct fallback if help requested on general interface
    if len(sys.argv) == 1:
        show_banner()
        HelpCommand.display_general_help()
        sys.exit(0)

    if "-h" in sys.argv or "--help" in sys.argv:
        # Check if a command is specified to print specific command usage
        args, _ = parser.parse_known_args()
        if args.command:
            chosen_parser = subparsers.choices.get(args.command)
            if chosen_parser:
                chosen_parser.print_help()
                sys.exit(0)
        show_banner()
        HelpCommand.display_general_help()
        sys.exit(0)

    return parser.parse_args()
