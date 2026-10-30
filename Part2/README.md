# CS456 Group Project 1 — Part 2
## Redundancy, Recovery, and Adversarial Testing

### Project Overview

This project expands on the authentication service developed in Part 1 by adding automatic failure detection, a backup authentication service, and checkpoint-based recovery.

The primary service accepts login requests from a client and keeps track of failed login attempts. It periodically sends heartbeat messages to a monitor to indicate that it is running.

If the monitor stops receiving heartbeats, it assumes the primary service has failed and attempts to launch a backup service. The backup loads the most recently saved checkpoint and continues handling authentication requests.

Part 2 also includes adversarial testing to demonstrate weaknesses in heartbeat-based failure detection and checkpoint integrity.

### Project Files

| File | Description |
|---|---|
| `service.py` | Primary authentication server. Handles login requests, saves checkpoints, and sends heartbeats. |
| `backup.py` | Backup authentication server. Loads saved state and takes over when the primary fails. |
| `monitor.py` | Monitors heartbeat messages and launches the backup when a failure is detected. |
| `client.py` | Allows users to send login requests to the authentication service. |
| `attacker_recovery.py` | Simulates heartbeat disruption and checkpoint tampering attacks. |
| `attacker.py` | Additional attack script carried over from Part 1. |
| `checkpoint.json` | Stores failed login attempt counters so the backup can recover state. |
| `incidents.log` | Records failure detection, failover, and recovery events. |
| `WriteUp.docx` | Project write-up and analysis. |

### Requirements

- Python 3
- Windows operating system
- PowerShell or the VS Code integrated terminal
- Python standard libraries (no additional packages required)

The project uses the following local network ports:

- **TCP 5000:** Authentication requests from the client
- **UDP 5001:** Heartbeat messages and backup readiness notifications

All communication takes place on `127.0.0.1` (localhost).

### Running the Project

Open the `Part2` folder in VS Code and create separate terminals for the programs.

**1. Start the heartbeat monitor**

```powershell
py monitor.py
```

The monitor listens for heartbeat messages from the authentication service.

**2. Start the primary authentication service**

```powershell
py service.py
```

The primary starts listening for client connections on TCP port 5000 and sends heartbeat messages to the monitor.

**3. Start the client**

```powershell
py client.py
```

The client prompts for a username and password and displays the authentication result.

Test accounts include:

| Username | Password |
|---|---|
| `admin` | `password123` |
| `bob` | `mypassword` |
| `user` | `12345` |

These accounts are for demonstration purposes only.

### Checkpointing and State Recovery

The primary service tracks failed login attempts for each user.

After authentication requests, it saves the current counters in `checkpoint.json`.

The checkpoint is first written to a temporary file and then replaces the previous checkpoint. This helps reduce the chance of leaving a partially written checkpoint if the program stops during a write.

When the backup service starts, it reads `checkpoint.json` to restore the failed login counters.

This allows the authentication service to preserve its saved state across a primary failure.

### Automatic Failure Detection and Recovery

The primary service sends heartbeat messages approximately once per second.

The monitor uses a three-second heartbeat timeout to detect a possible failure.

When the timeout is reached, the monitor:

1. Records the suspected failure in `incidents.log`.
2. Launches `backup.py` in a separate console.
3. Waits for the backup to confirm that it has started successfully.
4. Records whether the backup reported readiness.

The backup attempts to bind to the same TCP port previously used by the primary service.

If the primary has crashed and released the port, the backup can start accepting authentication requests.

The backup also sends heartbeat messages to the monitor.

**Note:** The backup is launched after failure detection rather than running continuously. This implementation uses checkpoint-based cold standby recovery.

### Testing Normal Recovery

The primary service includes a simulated random crash mechanism.

To test recovery:

1. Start `monitor.py`.
2. Start `service.py`.
3. Start `client.py`.
4. Make several failed login attempts to create checkpoint data.
5. Wait for the primary service to simulate a crash.
6. Observe the monitor detect the missing heartbeats and launch the backup.
7. Use the client again to verify that the backup accepts requests.
8. Check that the saved failed login counters were restored.

The primary service normally uses:

```python
CRASH_PROBABILITY = 0.05
```

The random crash check runs periodically, so the time until a crash varies.

### Adversarial Testing

Two recovery-related attacks were tested using `attacker_recovery.py`.

Run the script in another terminal:

```powershell
py attacker_recovery.py
```

**Attack 1: Checkpoint Tampering**

The attacker modifies `checkpoint.json` to reset the saved failed login counter for the `admin` account.

This demonstrates that checkpointing preserves state but does not automatically guarantee that the saved data is trustworthy.

An attacker with permission to modify the checkpoint can change the state that the backup later restores.

**Attack 2: Heartbeat Disruption / False Failover**

The attacker creates a file named `pause_heartbeat.txt`, which causes the primary service to stop sending heartbeat messages without actually crashing.

The monitor detects the missing heartbeats and attempts to start the backup.

However, the primary service is still running and using TCP port 5000. As a result, the backup cannot bind to that port and reports a Windows socket error (`WinError 10048`).

This demonstrates a false-failover condition in which the monitor mistakes missing heartbeat messages for a service failure.

The test does not produce two simultaneously active authentication servers because the operating system prevents both processes from listening on the same address and port.

For this test, temporarily set:

```python
CRASH_PROBABILITY = 