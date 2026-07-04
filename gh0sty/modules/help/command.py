"""Interface de linha de comando (CLI) para exibir ajudas personalizadas do sistema."""

import argparse

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from gh0sty.modules.base import BaseModule

console = Console()


class HelpCommand(BaseModule):
    """Subcomando que fornece ajuda personalizada estilizada geral ou específica de módulo."""

    help_summary = "Exibe a ajuda personalizada do sistema ou o uso de comandos específicos de módulos"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configura os argumentos do argparse para o subcomando help."""
        parser.add_argument(
            "module_name",
            nargs="?",
            choices=["scan", "sweep", "recon", "web", "dns", "report", "config", "help"],
            help="Exibe o uso detalhado de um comando de módulo específico",
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executa o comando de ajuda."""
        if args.module_name:
            self.display_module_help(args.module_name)
        else:
            self.display_general_help()

    @staticmethod
    def display_general_help() -> None:
        """Exibe uma lista estilizada com todos os comandos e opções disponíveis."""
        console.print("[bold cyan]Uso:[/bold cyan]")
        console.print("  gh0sty <comando> [opções]\n")

        console.print("[bold cyan]Opções Globais:[/bold cyan]")
        console.print("  -h, --help     Exibe esta mensagem de ajuda e sai")
        console.print("  -v, --verbose  Habilita mensagens de log detalhadas (DEBUG)\n")

        # Tabela com a lista de módulos
        table = Table(title="Comandos Disponíveis", border_style="cyan", box=None)
        table.add_column("Comando", style="bold green", width=15)
        table.add_column("Descrição", style="white")

        table.add_row("scan", "Realiza varreduras autorizadas em ativos (resolução de host, verificações de portas TCP)")
        table.add_row("sweep", "Realiza varreduras/mapeamento de estruturas de alvos web autorizados")
        table.add_row("recon", "Consolida descobertas ativas e passivas em ativos alvo")
        table.add_row(
            "web", "Inspeciona configurações de segurança de aplicações HTTP/HTTPS, TLS e cookies"
        )
        table.add_row("dns", "Consulta registros DNS padrão (A, AAAA, MX, TXT, NS, etc.)")
        table.add_row(
            "report", "Compila saídas brutas de varredura em JSON para HTML, MD, CSV, JSON, PDF, TXT ou XML"
        )
        table.add_row(
            "config", "Exibe e atualiza opções locais (threads, diretório de saída, timeout, etc.)"
        )
        table.add_row("help", "Exibe a ajuda geral ou detalhes de uso de um comando específico")

        console.print(table)
        console.print(
            "\nUse [bold yellow]gh0sty help <comando>[/bold yellow] para visualizar a ajuda detalhada do módulo."
        )

    def display_module_help(self, cmd: str) -> None:
        """Exibe ajuda estilizada detalhada e exemplos para um módulo.

        Args:
            cmd: Nome do comando.
        """
        panel_content = ""

        if cmd == "scan":
            panel_content = (
                "[bold green]Comando:[/bold green] gh0sty scan\n"
                "[bold green]Descrição:[/bold green] Varre hosts autorizados para verificar se estão ativos e identificar portas TCP abertas.\n\n"
                "[bold cyan]Opções:[/bold cyan]\n"
                "  -t, --target  Hostname ou endereço IP do alvo (Obrigatório)\n"
                "  -p, --ports   Portas separadas por vírgula ou intervalo (ex. 80,443,22-25) ou 'common' (Padrão: common)\n"
                "  -o, --output  Caminho do arquivo de destino para salvar os dados brutos\n"
                "  -f, --format  Formato de exportação direta: json, csv, html, md, pdf, txt, xml (Padrão: nenhum)\n\n"
                "[bold cyan]Exemplos:[/bold cyan]\n"
                "  gh0sty scan -t exemplo.com\n"
                "  gh0sty scan -t 192.168.1.10 -p 22,80,443 -f html -o scan.html\n"
            )
        elif cmd == "sweep":
            panel_content = (
                "[bold green]Comando:[/bold green] gh0sty sweep\n"
                "[bold green]Descrição:[/bold green] Mapeia arquivos de recursos, caminhos de diretório ou endpoints de um alvo web.\n\n"
                "[bold cyan]Opções:[/bold cyan]\n"
                "  -t, --target  URL da aplicação web do alvo (Obrigatório)\n"
                "  -w, --wordlist Caminho para arquivo de lista de palavras (wordlist) personalizado\n"
                "  -o, --output  Caminho do arquivo de destino para salvar os dados\n"
                "  -f, --format  Tipo de formato de exportação direta (Padrão: nenhum)\n\n"
                "[bold cyan]Exemplos:[/bold cyan]\n"
                "  gh0sty sweep -t https://exemplo.com/ -w wordlist.txt\n"
            )
        elif cmd == "recon":
            panel_content = (
                "[bold green]Comando:[/bold green] gh0sty recon\n"
                "[bold green]Descrição:[/bold green] Executa auditorias consolidadas de DNS, TCP e web em um host alvo autorizado.\n\n"
                "[bold cyan]Opções:[/bold cyan]\n"
                "  -t, --target  Domínio ou IP do host alvo (Obrigatório)\n"
                "  -o, --output  Caminho para salvar as varreduras consolidadas\n"
                "  -f, --format  Tipo de formato de exportação (Padrão: nenhum)\n\n"
                "[bold cyan]Exemplos:[/bold cyan]\n"
                "  gh0sty recon -t exemplo.com -f html -o relatorios/recon_dominio.html\n"
            )
        elif cmd == "web":
            panel_content = (
                "[bold green]Comando:[/bold green] gh0sty web\n"
                "[bold green]Descrição:[/bold green] Audita cabeçalhos HTTP, caminhos de redirecionamento, flags de cookies e detalhes do certificado SSL.\n\n"
                "[bold cyan]Opções:[/bold cyan]\n"
                "  -t, --target  URL ou domínio do alvo (ex. exemplo.com ou https://exemplo.com) (Obrigatório)\n"
                "  -o, --output  Caminho do arquivo de destino para salvar os dados brutos\n"
                "  -f, --format  Tipo de formato de exportação direta (Padrão: nenhum)\n\n"
                "[bold cyan]Exemplos:[/bold cyan]\n"
                "  gh0sty web -t exemplo.com\n"
                "  gh0sty web -t https://localhost:8443 -f json -o output.json\n"
            )
        elif cmd == "dns":
            panel_content = (
                "[bold green]Comando:[/bold green] gh0sty dns\n"
                "[bold green]Descrição:[/bold green] Resolve registros de domínio para o host alvo.\n\n"
                "[bold cyan]Opções:[/bold cyan]\n"
                "  -t, --target  Domínio alvo para consultar (Obrigatório)\n"
                "  -r, --record  Tipo de registro (A, AAAA, MX, TXT, NS, SOA, CNAME, PTR) ou 'all' (Padrão: all)\n"
                "  -o, --output  Caminho do arquivo de destino para salvar os dados\n"
                "  -f, --format  Tipo de formato de exportação direta (Padrão: nenhum)\n\n"
                "[bold cyan]Exemplos:[/bold cyan]\n"
                "  gh0sty dns -t google.com\n"
                "  gh0sty dns -t cloudflare.com -r MX -f md -o mx_registros.md\n"
            )
        elif cmd == "report":
            panel_content = (
                "[bold green]Comando:[/bold green] gh0sty report\n"
                "[bold green]Descrição:[/bold green] Compila resultados de varreduras salvos em JSON para outros formatos.\n\n"
                "[bold cyan]Opções:[/bold cyan]\n"
                "  -i, --input   Arquivo de origem com a varredura bruta em JSON (Obrigatório)\n"
                "  -f, --format  Tipo de formato (json, csv, html, md, pdf, txt, xml) (Obrigatório)\n"
                "  -o, --output  Caminho do arquivo de destino para salvar o relatório compilado (Obrigatório)\n\n"
                "[bold cyan]Exemplos:[/bold cyan]\n"
                "  gh0sty report -i dados_brutos.json -f html -o relatorio_completo.html\n"
            )
        elif cmd == "config":
            panel_content = (
                "[bold green]Comando:[/bold green] gh0sty config\n"
                "[bold green]Descrição:[/bold green] Gerencia as opções de configuração do sistema.\n\n"
                "[bold cyan]Opções:[/bold cyan]\n"
                "  --show        Exibe todas as configurações\n"
                "  --set         Atualiza um parâmetro de configuração\n"
            )
        elif cmd == "help":
            panel_content = (
                "[bold green]Comando:[/bold green] gh0sty help\n"
                "[bold green]Descrição:[/bold green] Exibe a ajuda do sistema ou detalhes de um subcomando.\n\n"
                "[bold cyan]Uso:[/bold cyan]\n"
                "  gh0sty help [nome_do_comando]\n"
            )

        panel = Panel(
            panel_content, border_style="cyan", title=f"Ajuda do Comando: {cmd}", title_align="left"
        )
        console.print(panel)
