
import os
import random
import socket
import threading
import time

# Configuration
MONITOR_IP = "127.0.0.1"
MONITOR_PORT = 5001
HEARTBEAT_INTERVAL = 1
CRASH_PROBABILITY = 0.05

# Dummy user credentials
users = {
    "admin": "password123",
    "bob": "mypassword",
    "user": "12345"
}


def authenticate(username, password):
    if username in users and users[username] == password:
        return True
    return False


def send_heartbeat():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        sock.sendto(
            b"HEARTBEAT",
            (MONITOR_IP, MONITOR_PORT)
        )

        # print("[HEARTBEAT] Sent to monitor")
        time.sleep(HEARTBEAT_INTERVAL)


def simulate_crash():
    while True:
        time.sleep(3)

        if random.random() < CRASH_PROBABILITY:
            print("CRITICAL ERROR: Service crashed!", flush=True)
            os._exit(1)


def main():
    print("Authentication Service Started")

    # Start heartbeat thread
    heartbeat_thread = threading.Thread(
        target=send_heartbeat,
        daemon=True
    )
    heartbeat_thread.start()

    # Start random crash thread
    crash_thread = threading.Thread(
        target=simulate_crash,
        daemon=True
    )
    crash_thread.start()

    # Main authentication loop
    while True:
        username = input("\nUsername: ")
        password = input("Password: ")

        if authenticate(username, password):
            print("ACCESS GRANTED")
        else:
            print("ACCESS DENIED")


if __name__ == "__main__":
    main()
