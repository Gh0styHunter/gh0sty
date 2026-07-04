"""Base module class for all gh0sty framework modules."""

import argparse
from abc import ABC, abstractmethod


class BaseModule(ABC):
    """Abstract Base Class representing a framework module subcommand."""

    # Short summary displayed in the general help list
    help_summary: str = ""

    @staticmethod
    @abstractmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures the argparse subparser arguments for this module.

        Args:
            parser: The command-specific subparser.
        """
        pass

    @abstractmethod
    def run(self, args: argparse.Namespace) -> None:
        """Executes the core module functionality.

        Args:
            args: The parsed command-line arguments.
        """
        pass
