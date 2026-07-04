"""CLI command line executable entry point."""

import sys

from gh0sty.core.dispatcher import CommandDispatcher
from gh0sty.core.exceptions import Gh0styException
from gh0sty.core.logger import logger, setup_logging
from gh0sty.core.parser import parse_arguments


def main() -> None:
    """Entry execution loop parsing arguments and executing modules."""
    try:
        args = parse_arguments()

        # Set logger verbosity
        setup_logging(verbose=args.verbose)

        # Dispatch command
        dispatcher = CommandDispatcher(args)
        dispatcher.dispatch()

    except Gh0styException as e:
        logger.error(f"[bold red]Erro:[/bold red] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.warning("\n[bold yellow]Execução abortada pelo usuário.[/bold yellow]")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"[bold red]Erro Crítico Inesperado:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
