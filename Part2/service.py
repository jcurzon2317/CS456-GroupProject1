
import json
import os
import random
import socket
import threading
import time
from pathlib import Path

# Configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

MONITOR_IP = "127.0.0.1"
MONITOR_PORT = 5001

HEARTBEAT_INTERVAL = 1
CRASH_PROBABILITY = 0.05

CHECKPOINT_FILE = Path(__file__).with_name("checkpoint.json")

HEARTBEAT_CONTROL_FILE = Path(__file__).with_name("pause_heartbeat.txt")

# Dummy user credentials
users = {
    "admin": "password123",
    "bob": "mypassword",
    "user": "12345"
}

failed_attempts = {
    "admin": 0,
    "bob": 0,
    "user": 0
}


def save_checkpoint():
    temp_file = CHECKPOINT_FILE.with_suffix(".tmp")

    with open(temp_file, "w") as file:
        json.dump(failed_attempts, file, indent=4)
        file.flush()
        os.fsync(file.fileno())

    os.replace(temp_file, CHECKPOINT_FILE)


def load_checkpoint():
    if not CHECKPOINT_FILE.exists():
        print("No checkpoint found. Starting fresh.")
        return

    try:
        with open(CHECKPOINT_FILE, "r") as file:
            saved_attempts = json.load(file)

        if not isinstance(saved_attempts, dict):
            raise ValueError("Invalid checkpoint format")

        for username in users:
            count = saved_attempts.get(username, 0)

            if type(count) is not int or count < 0:
                raise ValueError("Invalid failed attempt count")

            failed_attempts[username] = count

        print("Checkpoint loaded successfully.")

    except (OSError, ValueError, TypeError) as error:
        print("Error loading checkpoint:", error)
        raise


def authenticate(username, password):
    if username in users and users[username] == password:
        failed_attempts[username] = 0
        save_checkpoint()
        return "ACCESS GRANTED"

    if username in users:
        failed_attempts[username] += 1
        save_checkpoint()

    return "ACCESS DENIED"


def send_heartbeat():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            if not HEARTBEAT_CONTROL_FILE.exists():
                sock.sendto(
                    b"HEARTBEAT",
                    (MONITOR_IP, MONITOR_PORT)
                )

            time.sleep(HEARTBEAT_INTERVAL)


def simulate_crash():
    while True:
        time.sleep(3)

        if random.random() < CRASH_PROBABILITY:
            print("CRITICAL ERROR: Service crashed!", flush=True)
            os._exit(1)


def main():
    load_checkpoint()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((SERVER_IP, SERVER_PORT))
        server.listen(5)

        print("Authentication Service Started")
        print(f"Listening for clients on TCP port {SERVER_PORT}")

        heartbeat_thread = threading.Thread(
            target=send_heartbeat,
            daemon=True
        )
        heartbeat_thread.start()

        crash_thread = threading.Thread(
            target=simulate_crash,
            daemon=True
        )
        crash_thread.start()

        while True:
            client, address = server.accept()

            with client:
                print("Connection received from:", address)

                data = client.recv(1024).decode()

                if ":" not in data:
                    client.sendall(b"Invalid request")
                    continue

                username, password = data.split(":", 1)

                result = authenticate(username, password)

                if username in failed_attempts:
                    result += (
                        f"\nFailed attempts: "
                        f"{failed_attempts[username]}"
                    )

                client.sendall(result.encode())


if __name__ == "__main__":
    main()
