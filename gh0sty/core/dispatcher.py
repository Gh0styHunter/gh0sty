"""Command execution dispatcher routing CLI commands to their respective module classes."""

import argparse

from gh0sty.core.exceptions import Gh0styException


class CommandDispatcher:
    """Dispatches execution parameters to modules classes."""

    def __init__(self, args: argparse.Namespace) -> None:
        """Initializes parsed command line variables.

        Args:
            args: Parsed CLI namespace arguments.
        """
        self.args = args

    def dispatch(self) -> None:
        """Instantiates and executes the appropriate command module class."""
        cmd = self.args.command
        if not cmd:
            from gh0sty.modules.help.command import HelpCommand

            HelpCommand.display_general_help()
            return

        # Local imports to prevent startup loops
        from gh0sty.modules.config.command import ConfigCommand
        from typing import Union, Type
        from gh0sty.modules.dns.command import DnsCommand
        from gh0sty.modules.help.command import HelpCommand
        from gh0sty.modules.recon.command import ReconCommand
        from gh0sty.modules.report.manager import ReportCommand
        from gh0sty.modules.scan.command import ScanCommand
        from gh0sty.modules.sweep.command import SweepCommand
        from gh0sty.modules.web.command import WebCommand

        CommandType = Union[
            Type[ScanCommand],
            Type[SweepCommand],
            Type[ReconCommand],
            Type[WebCommand],
            Type[DnsCommand],
            Type[ReportCommand],
            Type[ConfigCommand],
            Type[HelpCommand],
        ]

        registry: dict[str, CommandType] = {
            "scan": ScanCommand,
            "sweep": SweepCommand,
            "recon": ReconCommand,
            "web": WebCommand,
            "dns": DnsCommand,
            "report": ReportCommand,
            "config": ConfigCommand,
            "help": HelpCommand,
        }

        cmd_class = registry.get(cmd)
        if cmd_class:
            module_instance = cmd_class()
            module_instance.run(self.args)
        else:
            raise Gh0styException(f"Comando desconhecido: '{cmd}'")
