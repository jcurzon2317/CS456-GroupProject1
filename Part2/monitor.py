
import logging
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Configuration
MONITOR_IP = "127.0.0.1"
MONITOR_PORT = 5001

HEARTBEAT_INTERVAL = 1
MISSED_HEARTBEATS = 3
TIMEOUT = HEARTBEAT_INTERVAL * MISSED_HEARTBEATS

BACKUP_FILE = Path(__file__).with_name("backup.py")
LOG_FILE = Path(__file__).with_name("incidents.log")

# Logging configuration
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    logging.info(message)


def start_backup(sock):
    log_event("[Failover Triggered] Starting backup service")

    try:
        backup_process = subprocess.Popen(
            [sys.executable, str(BACKUP_FILE)],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        start_time = time.monotonic()

        # Wait up to 5 seconds for backup confirmation
        while time.monotonic() - start_time < 5:

            if backup_process.poll() is not None:
                log_event("[ERROR] Backup process stopped unexpectedly")
                return None

            try:
                data, address = sock.recvfrom(1024)

                if data == b"BACKUP_READY":
                    log_event(
                        "[Service Restored] Backup service ready"
                    )
                    return backup_process

            except socket.timeout:
                pass

        log_event("[ERROR] Backup did not confirm readiness")
        return None

    except (OSError, subprocess.SubprocessError) as error:
        log_event(f"[ERROR] Could not start backup: {error}")

    return None


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((MONITOR_IP, MONITOR_PORT))
    sock.settimeout(0.5)

    last_heartbeat = time.monotonic()
    service_online = False
    failover_started = False
    backup_process = None

    print("Heartbeat Monitor Started")
    print(f"Listening on UDP port {MONITOR_PORT}")

    try:
        while True:
            try:
                data, address = sock.recvfrom(1024)

                if data == b"HEARTBEAT":
                    last_heartbeat = time.monotonic()

                    if not service_online:
                        log_event("[ONLINE] Authentication service detected")
                        service_online = True

                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] Heartbeat received from {address}")

                elif data == b"BACKUP_HEARTBEAT":
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] Heartbeat received from backup {address}")

            except socket.timeout:
                pass

            if service_online:
                elapsed = time.monotonic() - last_heartbeat

                if elapsed >= TIMEOUT:
                    log_event(
                        "[Crash Detected] Primary authentication service DOWN"
                    )

                    service_online = False

                    if not failover_started:
                        failover_started = True
                        backup_process = start_backup(sock)

    except KeyboardInterrupt:
        print("\nHeartbeat monitor stopped")

    finally:
        sock.close()


if __name__ == "__main__":
    main()
