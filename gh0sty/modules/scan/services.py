"""Services mapping catalog utilities."""

from gh0sty.utils.network import get_service_name


def get_service_description(port: int) -> str:
    """Returns typical service description for a target port."""
    return get_service_name(port)
