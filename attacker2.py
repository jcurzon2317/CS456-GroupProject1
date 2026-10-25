import socket
import time

MONITOR_IP = "127.0.0.1"
MONITOR_PORT = 5001

# Previously captured legitimate heartbeat
captured_heartbeat = b"HEARTBEAT"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        sock.sendto(
            captured_heartbeat,
            (MONITOR_IP, MONITOR_PORT)
        )

        print("[REPLAY] Captured heartbeat resent")
        time.sleep(1)

except KeyboardInterrupt:
    print("Replay stopped")

finally:
    sock.close()