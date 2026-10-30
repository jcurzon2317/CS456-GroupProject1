# CS456 Group Project 1 — Part 2
## Individual Contributions

**Name:** John Curzon  
**Project:** Redundancy, Recovery, and Adversarial Testing

### Overview

I completed Part 2 of the project independently. This involved expanding the authentication service from Part 1 by adding a backup service, checkpointing, automatic failure detection, and recovery. I also developed and tested attacks against the recovery system to identify possible weaknesses.

### Implementation

- Developed `backup.py` to take over authentication requests when the primary service fails.
- Modified `service.py` to save failed login attempts to `checkpoint.json` so the information could be recovered after a crash.
- Updated `monitor.py` to detect missing heartbeats and automatically launch the backup service.
- Added backup heartbeat messages and a readiness notification to verify successful recovery.
- Developed `client.py` to test authentication requests before and after failover.
- Used Python sockets for TCP authentication requests and UDP heartbeat communication.

### Adversarial Testing

I implemented and tested two attacks against the recovery system using `attacker_recovery.py`.

**Checkpoint Tampering**

I modified the saved checkpoint to reset the failed login counter for the admin account. This demonstrated that although checkpointing can preserve state, an attacker with access to the checkpoint file can manipulate the information that the backup restores.

**Heartbeat Disruption**

I created a method to stop the primary service from sending heartbeats without shutting down the authentication server. The monitor detected the missing heartbeats and attempted to start the backup even though the primary was still running.

Because the primary was still using TCP port 5000, the backup could not bind to that port. This demonstrated how heartbeat-based monitoring can incorrectly identify a working service as failed.

### Testing and Debugging

I tested the system to verify that:

- The monitor could detect a simulated primary crash.
- The backup service started automatically after failure detection.
- Failed login attempt counters were preserved through checkpointing.
- The client could continue making authentication requests after recovery.
- The backup sent its own heartbeat messages.
- The monitor could distinguish successful backup startup from a failed takeover.
- Both adversarial attacks produced the expected results.

During development, I also debugged issues involving socket binding, heartbeat control files, process management, and communication between the monitor and backup service.

### Documentation

I prepared the project documentation, including the README, architecture diagram, testing results, and technical write-up. I also organized the project files for submission through GitHub.

### Conclusion

I completed the implementation, testing, debugging, and documentation for Part 2 independently. The project helped me better understand fault tolerance, redundancy, checkpointing, and automatic recovery.

The adversarial testing also showed me that recovery mechanisms can introduce security weaknesses. In particular, missing heartbeats do not always mean a service has crashed, and saved checkpoints need protection against unauthorized modification.