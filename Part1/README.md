# CS456 – Mini Group Project 1
## Resilient Security Systems – Part 1: Failure Detection

### Project Overview

This project demonstrates how a heartbeat monitoring system can detect failures in a security-critical service. I implemented a basic authentication service in Python that validates dummy usernames and passwords and experiences random crashes during operation.

A separate heartbeat monitor receives periodic messages from the authentication service. If the service stops sending heartbeats for a specified amount of time, the monitor detects the failure and records the incident in a log file.

The project also includes an attacker script that demonstrates a heartbeat spoofing vulnerability. By sending fake heartbeat messages, an attacker can trick the monitor into believing the authentication service is still running after it has crashed.

### Project Files

```text
CS456-GroupProject1/
├── service.py
├── monitor.py
├── attacker.py
├── incidents.log
├── README.md
└── CONTRIBUTIONS.md
```

- **service.py:** Authentication service that validates dummy credentials, sends heartbeats, and experiences random crashes.
- **monitor.py:** Independent monitoring process that receives heartbeats, detects timeouts, and logs failures.
- **attacker.py:** Sends fake heartbeat messages to test the monitor's vulnerability to spoofing.
- **incidents.log:** Records detected service failures with timestamps.
- **CONTRIBUTIONS.md:** Documents each team member's contributions.

### Requirements

- Python 3
- Windows, Linux, or macOS
- A terminal or development environment such as Visual Studio Code

The project uses Python's built-in libraries and does not require additional packages.

### Configuration

The authentication service and monitor communicate using UDP over the local loopback interface.

| Parameter | Value |
|---|---|
| Monitor IP | 127.0.0.1 |
| Monitor Port | 5001 |
| Heartbeat Interval (T) | 1 second |
| Missed Heartbeat Threshold (N) | 3 |
| Timeout Window (W) | 3 seconds |
| Random Crash Probability | 5% every 3 seconds (0.05) |

The heartbeat interval was chosen to allow relatively quick failure detection without generating excessive network traffic. The three-second timeout provides some tolerance for brief delays while still detecting service failures quickly. Failure rate can be adjusted to the users needs.

### How to Run

Open the project folder in Visual Studio Code and open three separate terminals.

**1. Start the heartbeat monitor**

In the first terminal, run:

```powershell
py .\monitor.py
```

The monitor begins listening for heartbeat messages on UDP port 5001.

Expected output:

```text
Heartbeat Monitor Started
Listening on port 5001
Timeout threshold: 3 seconds
```

**2. Start the authentication service**

In the second terminal, run:

```powershell
py .\service.py
```

The service starts sending heartbeat messages every second and accepts login attempts.

Example credentials:

| Username | Password |
|---|---|
| admin | password123 |
| bob | mypassword |
| user | 12345 |

Example authentication:

```text
Authentication Service Started

Username: admin
Password: password123
ACCESS GRANTED

Username: admin
Password: wrongpassword
ACCESS DENIED
```

The service also runs a background thread that randomly determines whether the process should crash.

When a crash occurs, the authentication service terminates. A termination can be done early by increasing the failure rate or by exiting the program such as ctrl + C.

3. Observe failure detection

While the authentication service is running, the monitor displays received heartbeats:

[STATUS] Authentication Service ONLINE
[15:20:01] Heartbeat received
[15:20:02] Heartbeat received
[15:20:03] Heartbeat received

If the service crashes and no heartbeats are received for three seconds, the monitor reports:

[ALERT] Authentication Service DOWN at 2026-10-24 15:20:06

The incident is also appended to incidents.log.

Adversarial Assessment: Heartbeat Spoofing

The attacker script tests whether the monitor can distinguish legitimate heartbeat messages from fake ones.

1. Start the monitor and authentication service.

2. Open a third terminal and run:

py .\attacker.py

The attacker begins sending fake heartbeat messages to the monitor every second.

Example output:

Heartbeat Spoofing Attack Started
Target: 127.0.0.1:5001

[15:25:01] Fake heartbeat sent
[15:25:02] Fake heartbeat sent
[15:25:03] Fake heartbeat sent

3. Wait for the authentication service to crash.

Even after the authentication service crashes, the monitor continues receiving the attacker's fake heartbeats.

Because the monitor does not authenticate incoming heartbeat messages, it incorrectly reports that the service is still online.

4. Stop the attacker using Ctrl+C.

Once the attacker stops transmitting, the monitor no longer receives heartbeats.

After approximately three seconds, the monitor detects the failure and records the incident in incidents.log.

Testing Results

Test

Expected Result

Observed Result

Valid login credentials

Access granted

Passed

Invalid login credentials

Access denied

Passed

Random service crash

Service terminates

Passed

Crash without attacker

Monitor detects failure

Passed

Crash with attacker running

Monitor accepts fake heartbeats

Attack successful

Attacker stops after service crash

Monitor detects and logs failure

Passed

Security Analysis

The heartbeat monitoring system successfully detects service failures under normal operating conditions. However, the adversarial assessment revealed that the monitor is vulnerable to heartbeat spoofing.

The monitor checks whether incoming UDP messages contain the expected heartbeat payload but does not verify their source. An attacker can exploit this by sending identical heartbeat messages to the monitor.

During testing, the authentication service crashed while the attacker continued sending fake heartbeats. The monitor failed to recognize the service failure because it continued receiving messages that appeared legitimate but were spoofed by the attacker.

When the attacker stopped sending messages, the monitor detected the missing heartbeats and logged the failure.

This demonstrates that heartbeat monitoring alone is insufficient when the communication channel is not authenticated.

A possible improvement would be to use message authentication codes (HMACs), sequence numbers, and timestamps to help prevent spoofing and replay attacks.

Limitations

This project is a simplified prototype intended to demonstrate failure detection and heartbeat security.

Authentication uses predefined dummy credentials rather than a secure database.

Heartbeat messages are not authenticated.

The monitor detects failures but does not automatically restart the authentication service.

All processes communicate over localhost for demonstration purposes.

Conclusion

This project demonstrates the importance of heartbeat monitoring for maintaining the availability of security-critical services. The monitor successfully identifies unexpected authentication service crashes by detecting missing heartbeat messages.

However, the spoofing experiment shows that attackers can exploit unauthenticated heartbeat protocols to hide service failures. Securing the monitoring channel is therefore an important part of designing resilient security systems.

Course Information

Course: CS456 – Modern Cybersecurity
Project: Mini Group Project 1 – Resilient Security Systems, Part 1
Language: Python

Team member responsibilities are documented in CONTRIBUTIONS.md.