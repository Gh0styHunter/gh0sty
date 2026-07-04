"""Validation utilities for domain names, IP addresses, and port definitions."""

import ipaddress
import re

from gh0sty.core.constants import COMMON_PORTS
from gh0sty.core.exceptions import ValidationError

# Regex pattern for a valid RFC 1035 domain name
DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-_]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]$"
)


def is_valid_ipv4(ip: str) -> bool:
    """Checks if a string is a valid IPv4 address."""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


def is_valid_ipv6(ip: str) -> bool:
    """Checks if a string is a valid IPv6 address."""
    try:
        ipaddress.IPv6Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


def is_valid_ip(ip: str) -> bool:
    """Checks if a string is a valid IPv4 or IPv6 address."""
    return is_valid_ipv4(ip) or is_valid_ipv6(ip)


def is_valid_domain(domain: str) -> bool:
    """Checks if a string is a valid domain name."""
    if len(domain) > 253:
        return False
    clean_domain = (
        domain.rsplit("://", maxsplit=1)[-1].split("/", maxsplit=1)[0].split(":", maxsplit=1)[0]
    )
    return bool(DOMAIN_REGEX.match(clean_domain))


def clean_target(target: str) -> str:
    """Extracts raw host or IP from potential URLs or target strings."""
    if "://" in target:
        target = target.rsplit("://", maxsplit=1)[-1]
    target = target.split("/")[0]
    if "]" in target:
        target = target.split("]")[0].replace("[", "")
    else:
        target = target.split(":")[0]
    return target.strip()


def parse_ports(ports_str: str) -> list[int]:
    """Parses ports, list of ports or ranges into unique sorted integers.

    Args:
        ports_str: Ports spec (e.g. 'common', '80,443', '22-25').

    Returns:
        Sorted list of port integers.
    """
    if not ports_str or ports_str.strip().lower() == "common":
        return COMMON_PORTS.copy()

    ports: set[int] = set()
    parts = ports_str.split(",")

    for part in parts:
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            sub_parts = part.split("-")
            if len(sub_parts) != 2:
                raise ValidationError(f"Formato de intervalo de portas inválido: '{part}'")
            try:
                start = int(sub_parts[0])
                end = int(sub_parts[1])
            except ValueError as e:
                raise ValidationError(f"O limite do intervalo de portas deve ser numérico: '{part}'") from e

            if start > end:
                start, end = end, start

            if start < 1 or end > 65535:
                raise ValidationError(f"As portas devem estar entre 1 e 65535. Fora do intervalo: '{part}'")

            ports.update(range(start, end + 1))
        else:
            try:
                port = int(part)
            except ValueError as e:
                raise ValidationError(f"A porta deve ser um número inteiro: '{part}'") from e

            if port < 1 or port > 65535:
                raise ValidationError(f"A porta deve estar entre 1 e 65535. Fora do intervalo: '{port}'")

            ports.add(port)

    return sorted(list(ports))
