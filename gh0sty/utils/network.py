"""Network host resolution, socket connections, and certificate utilities."""

import socket
import ssl
from datetime import UTC, datetime
from typing import Any

from gh0sty.core.constants import PORT_SERVICES
from gh0sty.core.logger import logger


def get_service_name(port: int) -> str:
    """Returns typical service name for a port, fallback to socket lookup."""
    if port in PORT_SERVICES:
        return PORT_SERVICES[port]
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"


def resolve_host(host: str) -> dict[str, list[str]]:
    """Resolves a hostname to its IPv4 and IPv6 addresses.

    Args:
        host: Hostname to resolve.

    Returns:
        Dictionary mapping 'ipv4' and 'ipv6' to lists of resolved IP addresses.
    """
    ips: dict[str, list[str]] = {"ipv4": [], "ipv6": []}
    try:
        addr_info = socket.getaddrinfo(host, None, socket.AF_INET)
        ips["ipv4"] = sorted(list({str(info[4][0]) for info in addr_info}))
    except socket.gaierror as e:
        logger.debug(f"Falha na resolução IPv4 para {host}: {e}")

    try:
        addr_info = socket.getaddrinfo(host, None, socket.AF_INET6)
        ips["ipv6"] = sorted(list({str(info[4][0]) for info in addr_info}))
    except socket.gaierror as e:
        logger.debug(f"Falha na resolução IPv6 para {host}: {e}")

    return ips


def reverse_resolve(ip: str) -> str | None:
    """Resolves an IP address to a hostname.

    Args:
        ip: IP address.

    Returns:
        Hostname string or None if resolution fails.
    """
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except OSError as e:
        logger.debug(f"Falha no DNS reverso para {ip}: {e}")
        return None


def scan_port(ip: str, port: int, timeout: float = 2.0) -> dict[str, Any] | None:
    """Attempts a socket connection to checking if a port is open.

    Args:
        ip: Target IP address.
        port: Target port.
        timeout: Socket timeout in seconds.

    Returns:
        Dictionary with port info if open, otherwise None.
    """
    family = socket.AF_INET6 if ":" in ip else socket.AF_INET

    try:
        with socket.socket(family, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                return {"port": port, "state": "open", "service": get_service_name(port)}
    except Exception as e:
        logger.debug(f"Erro de socket na porta {port} em {ip}: {e}")

    return None


def parse_ssl_cert(cert_dict: dict[str, Any] | None) -> dict[str, Any]:
    """Normalizes the dictionary returned by getpeercert() into clean strings."""
    if not cert_dict:
        return {}

    parsed: dict[str, Any] = {}

    def parse_dn(dn_list: list[list[tuple[str, str]]] | None) -> str:
        if not dn_list:
            return "Unknown"
        for item in dn_list:
            for key, val in item:
                if key == "commonName":
                    return val
        if dn_list and dn_list[0]:
            return dn_list[0][0][1]
        return "Unknown"

    parsed["subject"] = parse_dn(cert_dict.get("subject"))
    parsed["issuer"] = parse_dn(cert_dict.get("issuer"))
    parsed["serial_number"] = cert_dict.get("serialNumber", "Unknown")
    parsed["version"] = cert_dict.get("version", "Unknown")

    # Dates parsing
    date_format = "%b %d %H:%M:%S %Y %Z"
    for date_key, clean_key in [("notBefore", "valid_from"), ("notAfter", "valid_to")]:
        date_str = cert_dict.get(date_key)
        if date_str:
            parsed[clean_key] = date_str
            try:
                cleaned_date_str = " ".join(date_str.split())
                dt = datetime.strptime(cleaned_date_str, date_format)
                parsed[f"{clean_key}_iso"] = dt.isoformat()
                if clean_key == "valid_to":
                    # Warning-free naive UTC comparison
                    now_utc_naive = datetime.now(UTC).replace(tzinfo=None)
                    days_left = (dt - now_utc_naive).days
                    parsed["days_remaining"] = days_left
                    parsed["expired"] = days_left < 0
            except Exception as e:
                logger.debug(f"Falha ao processar data do certificado SSL '{date_str}': {e}")
        else:
            parsed[clean_key] = "Unknown"

    san_list = cert_dict.get("subjectAltName", [])
    parsed["sans"] = [san[1] for san in san_list if len(san) > 1]

    return parsed


def get_ssl_details(host: str, port: int = 443, timeout: float = 5.0) -> dict[str, Any]:
    """Establishes a secure connection and pulls parsed TLS certificate metadata.

    Args:
        host: Target hostname.
        port: Target TLS port (default 443).
        timeout: Network timeout.

    Returns:
        Dictionary filled with certificate parameters or error trace.
    """
    ssl_info: dict[str, Any] = {"supported": False}
    context = ssl.create_default_context()
    try:
        socket.inet_aton(host)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    except OSError:
        pass

    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(
                sock, server_hostname=host if context.check_hostname else None
            ) as sslsock:
                cipher_info = sslsock.cipher()
                ssl_info["supported"] = True
                ssl_info["tls_version"] = sslsock.version()
                ssl_info["cipher_name"] = cipher_info[0] if cipher_info else "Unknown"
                ssl_info["cipher_bits"] = cipher_info[2] if cipher_info else 0

                raw_cert = sslsock.getpeercert()
                ssl_info["certificate"] = parse_ssl_cert(raw_cert)
    except Exception as e:
        ssl_info["error"] = str(e)
        logger.debug(f"Falha na obtenção de metadados SSL/TLS em {host}:{port} - {e}")

    return ssl_info
