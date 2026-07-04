"""Passive information collector logic for reconnaissance mapping."""

from typing import Any

from gh0sty.core.logger import logger
from gh0sty.utils.dns import resolve_dns_record, resolve_ptr_record
from gh0sty.utils.validators import is_valid_ip


class ReconCollector:
    """Collects metadata from passive lookups."""

    def gather_metadata(self, target: str) -> dict[str, Any]:
        """Runs basic DNS and IP discovery to build metadata baseline.

        Args:
            target: Domain or IP target.

        Returns:
            Dictionary detailing gathered recon details.
        """
        logger.info(f"ReconCollector obtendo perfil ativo para {target}...")
        meta: dict[str, Any] = {"target": target, "dns_records": {}, "reverse_dns": "None"}

        # IP reverse lookup
        if is_valid_ip(target):
            ptr = resolve_ptr_record(target)
            if ptr:
                meta["reverse_dns"] = ptr[0]
        else:
            # Domain lookup
            for rtype in ["A", "MX", "TXT", "NS"]:
                meta["dns_records"][rtype] = resolve_dns_record(target, rtype)

        return meta
