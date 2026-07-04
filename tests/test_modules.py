"""Unit and integration tests for gh0sty command modules."""

import argparse
import json
from typing import Any
from unittest.mock import MagicMock, patch

from gh0sty.modules.dns.command import DnsCommand
from gh0sty.modules.recon.command import ReconCommand
from gh0sty.modules.report.manager import ReportCommand
from gh0sty.modules.scan.command import ScanCommand
from gh0sty.modules.sweep.command import SweepCommand
from gh0sty.modules.web.command import WebCommand


@patch("gh0sty.utils.dns.resolve_dns_record")
def test_dns_module(mock_resolve: Any) -> None:
    mock_resolve.return_value = ["1.2.3.4"]

    module = DnsCommand()
    args = argparse.Namespace(target="example.com", record="A", output=None, format=None)
    module.run(args)
    mock_resolve.assert_called_with("example.com", "A")


@patch("gh0sty.utils.network.resolve_host")
@patch("gh0sty.utils.network.scan_port")
def test_scan_module(mock_scan: Any, mock_resolve: Any) -> None:
    mock_resolve.return_value = {"ipv4": ["1.2.3.4"], "ipv6": []}
    mock_scan.return_value = {"port": 80, "state": "open", "service": "HTTP"}

    module = ScanCommand()
    args = argparse.Namespace(target="example.com", ports="80", output=None, format=None)
    module.run(args)
    mock_resolve.assert_called_with("example.com")
    mock_scan.assert_called_with("1.2.3.4", 80, 5.0)


@patch("gh0sty.utils.http.fetch_url")
@patch("gh0sty.utils.network.get_ssl_details")
def test_web_module(mock_ssl: Any, mock_fetch: Any) -> None:
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.headers = {"Server": "MockServer", "Strict-Transport-Security": "max-age=31536000"}
    mock_resp.cookies = {}
    mock_resp.history = []
    mock_fetch.return_value = mock_resp
    mock_ssl.return_value = {"supported": False}

    module = WebCommand()
    args = argparse.Namespace(target="example.com", output=None, format=None)
    module.run(args)
    mock_fetch.assert_called()


def test_report_module(tmp_path: Any) -> None:
    scan_file = tmp_path / "scan.json"
    report_file = tmp_path / "report.html"

    scan_data = {
        "metadata": {
            "module": "scan",
            "target": "example.com",
            "timestamp": "2026-07-01 00:00:00 UTC",
        },
        "results": {
            "target": "example.com",
            "hostname": "example.com",
            "ips": ["1.2.3.4"],
            "scan_info": {"duration_seconds": 1.5},
            "open_ports": [{"ip": "1.2.3.4", "port": 80, "state": "open", "service": "HTTP"}],
        },
    }

    with open(scan_file, "w", encoding="utf-8") as f:
        json.dump(scan_data, f)

    module = ReportCommand()
    args = argparse.Namespace(input=str(scan_file), format="html", output=str(report_file))
    module.run(args)
    assert report_file.exists() is True


@patch("gh0sty.utils.threads.run_concurrently")
def test_sweep_module(mock_run: Any) -> None:
    mock_run.return_value = [
        {"url": "https://example.com/robots.txt", "status_code": 200, "length": "50"}
    ]

    module = SweepCommand()
    args = argparse.Namespace(target="example.com", wordlist=None, output=None, format=None)
    module.run(args)
    mock_run.assert_called()


@patch("gh0sty.utils.network.scan_port")
def test_recon_module(mock_scan: Any) -> None:
    mock_scan.return_value = {"port": 80, "state": "open", "service": "HTTP"}

    module = ReconCommand()
    args = argparse.Namespace(target="1.2.3.4", output=None, format=None)
    module.run(args)
    mock_scan.assert_called()
