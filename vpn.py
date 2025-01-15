import subprocess
import os
import time


def start_hotspot_shield():
    try:
        # Path to Hotspot Shield executable
        # Primary path
        hotspot_path = r"C:\Program Files\Hotspot Shield\hsselite.exe"
        backup_path = r"C:\Program Files\Hotspot Shield\hsselite.exe"  # Backup path

        # Try primary path first
        if os.path.exists(hotspot_path):
            subprocess.Popen([hotspot_path])
        # Try backup path if primary doesn't exist
        elif os.path.exists(backup_path):
            hotspot_path = backup_path
            subprocess.Popen([hotspot_path])
        else:
            print("Hotspot Shield executable not found!")
            return False

        print("Hotspot Shield launched successfully.")
        return True

    except Exception as e:
        print(f"Failed to start Hotspot Shield: {e}")
        return False


def stop_hotspot_shield():
    try:
        # Kill the Hotspot Shield process
        subprocess.run('taskkill /f /im hsselite.exe', shell=True)
        print("Hotspot Shield has been stopped.")
        return True
    except Exception as e:
        print(f"Failed to stop Hotspot Shield: {e}")
        return False


def main():
    while True:
        print("\n1. Start Hotspot Shield")
        print("2. Stop Hotspot Shield")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == '1':
            start_hotspot_shield()
        elif choice == '2':
            stop_hotspot_shield()
        elif choice == '3':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
