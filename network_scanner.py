"""Command line interface for the Network Scanner."""

import scanner

print("=======================")
print("  Network Scanner")
print("=======================")

target = "127.0.0.1"
print("Scanning target:", target)

open_ports = scanner.scan_ports(target, 1, 100)

for result in open_ports:
    print("Port", result["port"], "is open - Service:", result["service"])

print("===================================")
print("Total open ports found:", len(open_ports))

if not open_ports:
    print("No open ports were found.")
