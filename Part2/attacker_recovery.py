
import json
from pathlib import Path

CHECKPOINT_FILE = Path(__file__).with_name("checkpoint.json")

HEARTBEAT_CONTROL_FILE = Path(__file__).with_name("pause_heartbeat.txt")


def tamper_checkpoint():
    if not CHECKPOINT_FILE.exists():
        print("Checkpoint file not found.")
        return

    with open(CHECKPOINT_FILE, "r") as file:
        data = json.load(file)

    print("Original checkpoint:", data)

    # Change admin's failed login attempts
    data["admin"] = 0

    with open(CHECKPOINT_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print("Modified checkpoint:", data)
    print("Checkpoint tampering complete.")

def stop_heartbeats():
    HEARTBEAT_CONTROL_FILE.touch()
    print("Primary heartbeats stopped.")
    print("Primary authentication service is still running.")


def resume_heartbeats():
    if HEARTBEAT_CONTROL_FILE.exists():
        HEARTBEAT_CONTROL_FILE.unlink()

    print("Primary heartbeats resumed.")



def main():
    while True:
        print("\nRecovery Attack Simulation")
        print("1. Tamper with checkpoint")
        print("2. Stop primary heartbeats")
        print("3. Resume primary heartbeats")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            tamper_checkpoint()

        elif choice == "2":
            stop_heartbeats()

        elif choice == "3":
            resume_heartbeats()

        elif choice == "4":
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
