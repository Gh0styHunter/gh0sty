"""Fingerprinting engines parsing HTTP headers and cookies signatures."""

from typing import Any

from gh0sty.modules.web.technologies import COOKIE_SIGNATURES, HEADER_SIGNATURES, SERVER_SIGNATURES


def fingerprint_web_technologies(
    headers: dict[str, str], cookies: list[dict[str, Any]]
) -> list[str]:
    """Identifies estimated web technologies using banner signature rules."""
    techs = []
    server = headers.get("Server", "").lower()
    powered_by = headers.get("X-Powered-By", "").lower()

    # Check Server
    for key, val in SERVER_SIGNATURES.items():
        if key in server:
            techs.append(val)

    # Check X-Powered-By
    for key, val in HEADER_SIGNATURES["x-powered-by"].items():
        if key in powered_by:
            techs.append(val)

    # Check Cookies
    cookie_names = [c["name"].lower() for c in cookies]
    for name in cookie_names:
        for key, val in COOKIE_SIGNATURES.items():
            if key in name:
                techs.append(val)

    return sorted(list(set(techs)))
