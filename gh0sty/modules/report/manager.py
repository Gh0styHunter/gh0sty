"""Report manager class Coordinating format conversions and exports."""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Protocol

from gh0sty.core.exceptions import ReportError, ValidationError
from gh0sty.core.logger import logger
from gh0sty.core.output import console
from gh0sty.modules.base import BaseModule

# Format writers imports
from gh0sty.modules.report.csv import CSVWriter
from gh0sty.modules.report.html import HTMLWriter
from gh0sty.modules.report.json import JSONWriter
from gh0sty.modules.report.markdown import MarkdownWriter
from gh0sty.modules.report.pdf import PDFWriter
from gh0sty.modules.report.txt import TXTWriter
from gh0sty.modules.report.xml import XMLWriter


class ReportWriter(Protocol):
    """Protocol defining the interface for all report format writers."""

    def write(
        self, path: Path, data: Dict[str, Any], module_name: str, target: str, timestamp: str
    ) -> None:
        """Writes scan data in specific formats."""
        ...


class ReportGenerator:
    """Delegates formatting output tasks to format-specific writer classes."""

    def __init__(self, session_dict: Dict[str, Any], module_name: str, target: str) -> None:
        """Initializes report parameters.

        Args:
            session_dict: Fully structured scan session mapping.
            module_name: Originating scan module.
            target: Target domain or IP.
        """
        self.session_dict = session_dict
        self.module_name = module_name.lower()
        self.target = target

        # Pull metadata values if present
        meta = session_dict.get("metadata", {})
        self.timestamp = meta.get("timestamp", "")
        self.data = session_dict.get("results", session_dict)

    def generate(self, format_type: str, output_path: str) -> None:
        """Invokes specific format writer based on request.

        Args:
            format_type: json, csv, html, md, pdf, txt, or xml.
            output_path: Target path to write findings.
        """
        fmt = format_type.lower()
        path = Path(output_path)

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ReportError(f"Falha ao criar diretório de saída: {e}") from e

        writers: Dict[str, type[ReportWriter]] = {
            "json": JSONWriter,
            "csv": CSVWriter,
            "html": HTMLWriter,
            "md": MarkdownWriter,
            "markdown": MarkdownWriter,
            "pdf": PDFWriter,
            "txt": TXTWriter,
            "xml": XMLWriter,
        }

        writer_cls = writers.get(fmt)
        if not writer_cls:
            raise ReportError(f"Formato de relatório não suportado: '{format_type}'")

        try:
            writer = writer_cls()
            writer.write(path, self.data, self.module_name, self.target, self.timestamp)
        except Exception as e:
            raise ReportError(f"Falha ao gerar relatório {format_type.upper()}: {e}") from e


class ReportCommand(BaseModule):
    """Subcommand parser routing raw JSON scans conversion requests."""

    help_summary = "Compile raw JSON scan files into human-readable reports"

    @staticmethod
    def configure_parser(parser: argparse.ArgumentParser) -> None:
        """Configures the argparse arguments for the report subcommand."""
        parser.add_argument("-i", "--input", required=True, help="Path to raw JSON scan file")
        parser.add_argument(
            "-f",
            "--format",
            required=True,
            choices=["json", "csv", "html", "md", "pdf", "txt", "xml"],
            help="Target output format type",
        )
        parser.add_argument(
            "-o", "--output", required=True, help="Target report output filename path"
        )

    def run(self, args: argparse.Namespace) -> None:
        """Executes the report compiler subcommand."""
        input_path = Path(args.input)
        if not input_path.exists():
            raise ValidationError(f"Arquivo não encontrado: '{args.input}'")

        logger.info("Gerando relatório...")

        try:
            with open(input_path, encoding="utf-8") as f:
                raw_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ReportError(f"Arquivo de entrada inválido: {e}") from e
        except Exception as e:
            raise ReportError(f"Falha ao ler arquivo de entrada: {e}") from e

        module_name = ""
        target = "Alvo Desconhecido"
        session_dict = raw_data

        if isinstance(raw_data, dict) and "metadata" in raw_data and "results" in raw_data:
            metadata = raw_data["metadata"]
            module_name = metadata.get("module", "")
            target = metadata.get("target", "Alvo Desconhecido")
        else:
            # Structure guessing fallback
            if "open_ports" in raw_data:
                module_name = "scan"
                target = raw_data.get("target", "Alvo Desconhecido")
            elif "security_headers" in raw_data:
                module_name = "web"
                target = raw_data.get("host", raw_data.get("initial_target", "Alvo Desconhecido"))
            else:
                module_name = "dns"
                target = "Domínio Desconhecido"

            # Wrap in session format for dispatcher compatibility
            session_dict = {
                "metadata": {"module": module_name, "target": target, "timestamp": ""},
                "results": raw_data,
            }

        if not module_name:
            raise ReportError("Falha ao determinar o módulo de origem")

        logger.debug(
            f"Módulo: {module_name} | Alvo: {target}"
        )

        generator = ReportGenerator(
            session_dict=session_dict, module_name=module_name, target=target
        )
        generator.generate(args.format, args.output)
        console.print(
            f"[bold green]Sucesso:[/bold green] Relatório gerado em: [cyan]{args.output}[/cyan]"
        )
