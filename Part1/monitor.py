
import socket
import time
import logging
from datetime import datetime

# Monitor configuration
MONITOR_IP = "127.0.0.1"
MONITOR_PORT = 5001

HEARTBEAT_INTERVAL = 1
MISSED_HEARTBEATS = 3
TIMEOUT = HEARTBEAT_INTERVAL * MISSED_HEARTBEATS

# Configure incident logging
logging.basicConfig(
    filename="incidents.log",
    level=logging.WARNING,
    format="%(asctime)s - %(message)s"
)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((MONITOR_IP, MONITOR_PORT))
    sock.settimeout(0.5)

    print("Heartbeat Monitor Started")
    print(f"Listening on port {MONITOR_PORT}")
    print(f"Timeout threshold: {TIMEOUT} seconds\n")

    last_heartbeat = None
    service_online = False

    while True:
        try:
            data, address = sock.recvfrom(1024)

            if data == b"HEARTBEAT":
                last_heartbeat = time.monotonic()

                if not service_online:
                    print("[STATUS] Authentication Service ONLINE")
                    service_online = True

                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] Heartbeat received")

        except socket.timeout:
            pass

        if service_online and last_heartbeat is not None:
            elapsed = time.monotonic() - last_heartbeat

            if elapsed >= TIMEOUT:
                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                message = (
                    f"[ALERT] Authentication Service DOWN "
                    f"at {timestamp}"
                )

                print(message)
                logging.warning(message)

                service_online = False


if __name__ == "__main__":
    main()
