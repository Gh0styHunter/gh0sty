"""CLI command interface to manage configurations."""

import argparse

from rich.table import Table

from gh0sty.core.config import config_manager
from gh0sty.core.exceptions import ConfigError
from gh0sty.core.output import console
from gh0sty.modules.base import BaseModule


class ConfigCommand(BaseModule):
    """Subcommand to view or update system configurations."""

    help_summary = "Manage and view configuration parameters"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures the argparse arguments for the config subcommand."""
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--show", action="store_true", help="Display all configuration settings")
        group.add_argument(
            "--set",
            nargs=2,
            metavar=("KEY", "VALUE"),
            help="Set configuration setting key to value (e.g. --set threads 25)",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the configuration view or updates."""
        if args.show:
            self._display_config()
        elif args.set:
            key, value = args.set
            self._update_config(key, value)

    def _display_config(self) -> None:
        """Displays config manager properties in a table."""
        all_settings = config_manager.get_all()
        table = Table(title="Configurações do gh0sty", border_style="cyan")
        table.add_column("Chave de Configuração", style="bold green")
        table.add_column("Valor Atual", style="white")

        for key, val in all_settings.items():
            table.add_row(key, str(val))

        console.print(table)

    def _update_config(self, key: str, value: str) -> None:
        """Saves target key setting with the provided value."""
        try:
            config_manager.set(key, value)
            console.print(
                f"[bold green]Sucesso:[/bold green] A chave de configuração '[cyan]{key}[/cyan]' foi atualizada para '[yellow]{value}[/yellow]'"
            )
        except ConfigError as e:
            console.print(f"[bold red]Erro de Configuração:[/bold red] {e}")
            raise
