"""HTTP/HTTPS web client requests utilities."""

import httpx


def fetch_url(url: str, timeout: float = 5.0, verify_ssl: bool = False) -> httpx.Response:
    """Wrapper function to perform GET requests with redirects enabled.

    Args:
        url: Target web address.
        timeout: Socket request timeout in seconds.
        verify_ssl: Whether to verify target's SSL.

    Returns:
        httpx.Response object.
    """
    with httpx.Client(timeout=timeout, verify=verify_ssl) as client:
        return client.get(url, follow_redirects=True)
