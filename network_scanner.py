import socket

print("=======================")
print("  Network Scanner")
print("=======================")

target = "127.0.0.1"
print("Scanning target:",target)
ports = range(1, 101)
services = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS"
}
open_ports = 0

for port in ports:
    sock = socket.socket()
    sock.settimeout(0.1)
    result = sock.connect_ex((target, port))
    sock.close()
    if result == 0:
       open_ports += 1
       service = services.get(port, "Unknown")
       print("Port", port, "is open - Service:", service)

print("===================================")
print("Total open ports found:", open_ports)

if open_ports == 0:
    print("No open ports were found.")