"""Small standard library web server that puts the Network Scanner in the browser.

Serves the interactive page in `static/` on port 3000 and runs scans through the
shared `scanner.scan_ports` function, so the page and the command line script
always behave the same way.
"""

import json
import socket
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import scanner

PORT = 3000
STATIC_DIR = Path(__file__).resolve().parent / "static"

DEFAULT_TARGET = "127.0.0.1"
DEFAULT_START_PORT = 1
DEFAULT_END_PORT = 100
MAX_PORTS_PER_SCAN = 1024

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
}

ALLOWED_HOST_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_")


class ScanRequestError(ValueError):
    """Raised when a requested scan is not something we should run."""


def first_value(query, key):
    values = query.get(key)
    return values[0] if values else None


def parse_target(raw):
    """Validate the target and resolve it to an IPv4 address."""
    target = (raw or DEFAULT_TARGET).strip() or DEFAULT_TARGET

    if not set(target) <= ALLOWED_HOST_CHARS:
        raise ScanRequestError("Target must be a hostname or IPv4 address.")

    try:
        return target, socket.gethostbyname(target)
    except (OSError, UnicodeError):
        # A malformed name (for example "a..b") fails with UnicodeError from the
        # IDNA codec rather than the usual OSError, so both are treated as
        # "cannot resolve".
        raise ScanRequestError(f"Could not resolve '{target}'.")


def parse_port(raw, default, label):
    if raw is None or raw.strip() == "":
        return default

    if not raw.strip().isdigit():
        raise ScanRequestError(f"{label} must be a whole number.")

    value = int(raw)
    if not 1 <= value <= 65535:
        raise ScanRequestError(f"{label} must be between 1 and 65535.")

    return value


def build_scan_result(query):
    target, address = parse_target(first_value(query, "target"))
    start_port = parse_port(first_value(query, "start"), DEFAULT_START_PORT, "Start port")
    end_port = parse_port(first_value(query, "end"), DEFAULT_END_PORT, "End port")

    if start_port > end_port:
        raise ScanRequestError("Start port must not be greater than end port.")

    port_count = end_port - start_port + 1
    if port_count > MAX_PORTS_PER_SCAN:
        raise ScanRequestError(f"Please scan {MAX_PORTS_PER_SCAN} ports or fewer at a time.")

    started = time.perf_counter()
    open_ports = scanner.scan_ports(address, start_port, end_port)

    return {
        "target": target,
        "ip": address,
        "start": start_port,
        "end": end_port,
        "scanned": port_count,
        "open_ports": open_ports,
        "total_open": len(open_ports),
        "duration_ms": round((time.perf_counter() - started) * 1000),
    }


class ScanHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond(include_body=True)

    def do_HEAD(self):
        # Proxies and health probes use HEAD; without this the base class
        # answers 501 Unsupported method.
        self.respond(include_body=False)

    def respond(self, include_body):
        parsed = urlparse(self.path)

        if parsed.path == "/api/scan":
            if include_body:
                self.handle_scan(parse_qs(parsed.query))
            else:
                # A HEAD must not start a scan; report only that the endpoint exists.
                self.send_json({}, include_body=False)
            return

        relative = "index.html" if parsed.path in ("/", "/index.html") else parsed.path.lstrip("/")
        self.send_static(relative, include_body=include_body)

    def handle_scan(self, query):
        try:
            payload = build_scan_result(query)
        except ScanRequestError as error:
            self.send_json({"error": str(error)}, status=400)
            return

        self.send_json(payload)

    def send_static(self, relative, include_body=True):
        candidate = (STATIC_DIR / relative).resolve()

        if STATIC_DIR not in candidate.parents or not candidate.is_file():
            self.send_json({"error": "Not found"}, status=404, include_body=include_body)
            return

        body = candidate.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", CONTENT_TYPES.get(candidate.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(body)))
        # The page is read from disk on every request, so edits show up on reload.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if include_body:
            self.wfile.write(body)

    def send_json(self, payload, status=200, include_body=True):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if include_body:
            self.wfile.write(body)


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), ScanHandler)
    print(f"Network Scanner web page ready on port {PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
