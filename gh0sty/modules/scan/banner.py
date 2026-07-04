"""Port service banner grabbing utility."""

import socket


def grab_banner(ip: str, port: int, timeout: float = 2.0) -> str | None:
    """Establishes connection and reads the initial data buffer returned by service."""
    try:
        family = socket.AF_INET6 if ":" in ip else socket.AF_INET
        with socket.socket(family, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((ip, port))
            # SSH and FTP return banner immediately, HTTP requires query
            if port in [80, 8080]:
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            elif port in [443, 8443]:
                # SSL handshakes are handled separately, banner grab is skipped
                return "SSL/TLS"
            banner = sock.recv(512).decode("utf-8", errors="ignore").strip()
            return banner.split("\n")[0] if banner else None
    except Exception:
        return None
