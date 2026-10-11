# Network Scanner 🔐

## Description

This is a simple network port scanner built using Python.

The program scans ports on my local computer
(127.0.0.1) to identify which ports are open.

It also displays commonly associated services,
counts the number of open ports, and provides
a summary of the scan results.

This project was created to develop my Python
programming and cybersecurity skills.

## Features

- Scans ports 1 to 100 on the local computer.
- Identifies open TCP ports.
- Displays commonly associated services such as HTTP and SSH.
- Uses socket timeouts to avoid waiting too long.
- Counts the total number of open ports found.
- Displays a message when no open ports are detected.
- Closes sockets after checking each port.

## Cybersecurity Concepts

- **Port Scanning:** Checking network ports to identify which ones are open.
- **TCP Connections:** Understanding how computers establish network connections.
- **Localhost:** Using 127.0.0.1 to safely test my own computer.
- **Service Identification:** Learning which services are commonly associated with different port numbers.
- **Network Reconnaissance:** Gathering information about accessible network services.
- **Socket Programming:** Using Python's socket library to communicate over a network.


## How to Run

### Requirements
- Python 3 installed
- A terminal or PowerShell

### Instructions

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run the following command:

```powershell
py network_scanner.py
```

4. The scanner will check ports 1–100 on your local computer.
5. The results will display any open ports, their commonly associated services, and the total number found.

### Note
This scanner is designed for educational purposes and scans localhost (127.0.0.1) only. Only scan systems you own or have explicit permission to test.


## Example Output

The following output was produced when scanning my local computer:

```text
=======================
  Network Scanner
=======================
Scanning target: 127.0.0.1
Port 80 is open - Service: HTTP
===================================
Total open ports found: 1
```

This example shows that the scanner successfully identified one open port on localhost.

Port 80 is commonly associated with HTTP, although the scanner does not verify which service is running.


## Limitations

- The scanner currently checks only ports 1–100.
- It scans localhost (127.0.0.1) rather than other devices.
- It only checks TCP connections, not UDP.
- Service names are based on common port numbers and are not verified.
- A short connection timeout may cause slow or filtered ports to be missed.
- The scanner does not identify software versions or vulnerabilities.



## Future Improvements

- Allow users to select a custom port range.
- Add more commonly associated service names.
- Improve scanning speed.
- Add error handling for connection failures.
- Allow scan results to be saved to a text file.
- Add a simple graphical user interface (GUI).
- Explore more advanced service identification techniques.


## Technologies Used

- **Python 3** – Main programming language.
- **Socket Library** – Used to create TCP connections and check ports.
- **Visual Studio Code** – Used to write and edit the code.
- **Windows PowerShell** – Used to run and test the scanner.
- **Git and GitHub** – Used for version control and sharing the project.
