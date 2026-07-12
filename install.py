"""
CloudSOC Installer
"""

import platform
import shutil
import subprocess
import sys


def install_requirements():
    print("\nInstalling Python packages...\n")

    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            "requirements.txt",
        ]
    )


def check_rclone():

    print("\nChecking rclone...\n")

    if shutil.which("rclone"):

        print("[OK] rclone detected")

    else:

        print("[WARNING] rclone not found\n")

        system = platform.system()

        if system == "Windows":

            print("Download:")
            print("https://rclone.org/downloads/")

        elif system == "Linux":

            print("Install using:")
            print("curl https://rclone.org/install.sh | sudo bash")

        else:

            print("Visit:")
            print("https://rclone.org/downloads/")


def main():

    print("=" * 50)
    print("        CloudSOC Installer")
    print("=" * 50)

    print(f"Python : {platform.python_version()}")
    print(f"OS     : {platform.system()}")

    install_requirements()

    check_rclone()

    print("\nInstallation Complete.\n")
    print("Run:")
    print("python -m src.cloudsoc.app")


if __name__ == "__main__":
    main()