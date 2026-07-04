"""Global framework constants and configuration defaults."""

from pathlib import Path

# Paths
DEFAULT_CONFIG_DIR = Path.home() / ".gh0sty"
CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.json"

# Package relative folders
PACKAGE_ROOT = Path(__file__).parent.parent
DEFAULT_OUTPUT_DIR = Path.cwd()
DEFAULT_TEMPLATES_DIR = PACKAGE_ROOT / "templates"
DEFAULT_LOGS_DIR = DEFAULT_CONFIG_DIR / "logs"

# Scanner settings
DEFAULT_THREADS = 10
DEFAULT_TIMEOUT = 5.0
DEFAULT_FORMAT = "json"

COMMON_PORTS = [
    21,
    22,
    23,
    25,
    53,
    80,
    110,
    111,
    135,
    139,
    143,
    443,
    445,
    993,
    995,
    1723,
    3306,
    3389,
    5900,
    8080,
]

PORT_SERVICES = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP-Server",
    68: "DHCP-Client",
    80: "HTTP",
    110: "POP3",
    111: "RPCBind",
    123: "NTP",
    135: "RPC",
    137: "NetBIOS-NS",
    138: "NetBIOS-DGM",
    139: "NetBIOS-SSN",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    587: "SMTP-Submission",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    1521: "Oracle",
    1723: "PPTP",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}
