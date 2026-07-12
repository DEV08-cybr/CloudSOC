"""
CloudSOC Installer
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys


REQUIREMENTS = "requirements.txt"


def banner() -> None:
    print("=" * 60)
    print("                CloudSOC Installer")
    print("=" * 60)
    print(f"Python : {platform.python_version()}")
    print(f"OS     : {platform.system()}")
    print()


def install_requirements() -> bool:
    print("[1/3] Installing Python packages...\n")

    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                REQUIREMENTS,
            ]
        )

        print("\n[OK] Dependencies installed.\n")
        return True

    except subprocess.CalledProcessError:
        print("\n[ERROR] Failed to install requirements.")
        return False


def check_rclone() -> None:
    print("[2/3] Checking rclone...\n")

    if shutil.which("rclone"):
        print("[OK] rclone detected.\n")
        return

    print("[WARNING] rclone is not installed.\n")

    system = platform.system()

    if system == "Windows":
        print("Download rclone:")
        print("https://rclone.org/downloads/\n")

    elif system == "Linux":
        print("Install using:")
        print("curl https://rclone.org/install.sh | sudo bash\n")

    else:
        print("Visit:")
        print("https://rclone.org/downloads/\n")


def launch_app() -> None:

    answer = input("Launch CloudSOC now? [Y/n]: ").strip().lower()

    if answer not in ("", "y", "yes"):
        print("\nYou can start later with:\n")
        print("python -m cloudsoc.app")
        return

    print("\nStarting CloudSOC...\n")

    env = os.environ.copy()

    project_root = os.path.dirname(os.path.abspath(__file__))

    env["PYTHONPATH"] = os.path.join(project_root, "src")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "cloudsoc.app",
        ],
        env=env,
    )


def main() -> None:

    banner()

    if not install_requirements():
        sys.exit(1)

    check_rclone()

    print("[3/3] Installation Complete.\n")

    launch_app()


if __name__ == "__main__":
    main() 