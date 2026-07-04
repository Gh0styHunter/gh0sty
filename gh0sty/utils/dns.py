"""DNS resolver wrapper functions using dnspython."""

import dns.resolver
import dns.reversename
from dns.exception import DNSException

from gh0sty.core.exceptions import ScanError
from gh0sty.core.logger import logger


def resolve_dns_record(domain: str, rtype: str) -> list[str]:
    """Resolves a DNS record type for a domain name.

    Args:
        domain: Host domain.
        rtype: Record type (A, AAAA, MX, TXT, etc.).

    Returns:
        List of resolved output records.
    """
    logger.debug(f"Resolução DNS: {domain} ({rtype})")
    try:
        answers = dns.resolver.resolve(domain, rtype)
        return [str(rdata) for rdata in answers]
    except dns.resolver.NoAnswer:
        return []
    except dns.resolver.NXDOMAIN as e:
        raise ScanError(f"O domínio '{domain}' não existe.") from e
    except DNSException as e:
        logger.debug(f"Exceção de resolução DNS em {domain} ({rtype}): {e}")
        return []


def resolve_ptr_record(ip: str) -> list[str]:
    """Queries PTR records for a given IP address.

    Args:
        ip: Target IP address.

    Returns:
        List of reverse DNS resolved PTR records.
    """
    try:
        rev_name = dns.reversename.from_address(ip)
        answers = dns.resolver.resolve(rev_name, "PTR")
        return [str(rdata) for rdata in answers]
    except Exception as e:
        logger.debug(f"Consulta PTR falhou para {ip}: {e}")
        return []
