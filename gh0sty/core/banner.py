"""Rich CLI startup banners for the gh0sty framework."""

from rich.panel import Panel
from rich.text import Text

from gh0sty import __codename__, __version__
from gh0sty.core.output import console

BANNER = r"""
        __    ___       __
  ___ _/ /_  / _ \ ___ / /_ __ __
 / _ `/ _  \/ // /(_-</ __// // /
 \_, /_//_//____//___/\__/ \_, /
/___/                     /___/
"""


def show_banner() -> None:
    """Displays the initial startup banner."""
    banner_text = Text(BANNER, style="bold cyan")
    sub_text = Text(
        f"\n  [ gh0sty Security Auditing Framework v{__version__} ]\n"
        f"  Codename: {__codename__} | Auditor de Ativos Autorizado pelo Alvo\n",
        style="bold white",
    )
    panel = Panel(
        Text.assemble(banner_text, sub_text),
        border_style="cyan",
        expand=False,
    )
    console.print(panel)
