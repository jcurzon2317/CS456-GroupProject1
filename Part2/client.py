
import socket
import time

# Configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000


def send_login(username, password):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)
            sock.connect((SERVER_IP, SERVER_PORT))

            message = f"{username}:{password}"
            sock.sendall(message.encode())

            response = sock.recv(1024).decode()
            return response

    except (ConnectionRefusedError, socket.timeout, OSError):
        return "Service unavailable. Please try again."


def main():
    print("Authentication Client Started")

    while True:
        username = input("\nUsername (or exit): ")

        if username.lower() == "exit":
            break

        password = input("Password: ")

        response = send_login(username, password)
        print(response)

        time.sleep(0.5)


if __name__ == "__main__":
    main()
