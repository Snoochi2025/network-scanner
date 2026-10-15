"""Shared port scanning logic used by the command line script and the web page."""

import socket

# Commonly associated services, as used by the original scanner.
SERVICES = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
}

DEFAULT_TIMEOUT = 0.1


def scan_ports(target, start_port, end_port, timeout=DEFAULT_TIMEOUT):
    """Return the open TCP ports on `target` as a list of port/service dictionaries."""
    open_ports = []

    for port in range(start_port, end_port + 1):
        sock = socket.socket()
        sock.settimeout(timeout)
        try:
            if sock.connect_ex((target, port)) == 0:
                open_ports.append({
                    "port": port,
                    "service": SERVICES.get(port, "Unknown"),
                })
        finally:
            sock.close()

    return open_ports
