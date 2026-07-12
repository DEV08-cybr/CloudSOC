"""CloudSOC installer."""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

ROOT = Path(__file__).parent.resolve()
MIN_VERSION = (3, 10)
REQUIRED = [
    "requirements.txt",
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "src",
]


def parse_args() -> argparse.Namespace:
    """Parse installer command-line flags."""
    parser = argparse.ArgumentParser(description="Install CloudSOC")
    parser.add_argument(
        "--yes",
        "--non-interactive",
        action="store_true",
        help="Skip confirmation prompts and proceed automatically.",
    )
    parser.add_argument(
        "--skip-launch",
        action="store_true",
        help="Install dependencies and exit without launching the app.",
    )
    return parser.parse_args()


def line() -> None:
    """Print a visual separator."""
    print("=" * 60)


def banner() -> None:
    """Display the installer banner."""
    line()
    print("           CloudSOC Secure Installer")
    line()
    print(f"Python : {platform.python_version()}")
    print(f"OS     : {platform.system()}")
    print()


def check_python() -> None:
    """Ensure the installed Python version is supported."""
    print("[0/5] Checking Python...\n")

    if sys.version_info[:2] < MIN_VERSION:
        print("ERROR")
        print()
        print("Python 3.10 or newer is required.")
        print()
        print("Detected:")
        print(platform.python_version())
        print()
        print("Installation aborted.")
        raise SystemExit(1)

    print(f"✓ Python {platform.python_version()} supported\n")


def verify_project() -> None:
    """Verify required project files and directories exist."""
    print("[1/5] Verifying project...\n")

    missing: list[str] = []

    for item in REQUIRED:
        path = ROOT / item
        if path.exists():
            print(f"✓ {item}")
        else:
            print(f"✗ {item}")
            missing.append(item)

    if missing:
        print()
        print("Project verification failed.")
        print()
        print("Missing:")
        for item in missing:
            print(f"- {item}")
        print()
        print("Installation aborted.")
        raise SystemExit(1)

    print()


def permission(assume_yes: bool = False) -> None:
    """Show the installation summary and request user confirmation."""
    if assume_yes:
        return

    print("CloudSOC will perform the following actions:\n")
    print("✓ Verify project integrity")
    print("✓ Verify Python version")
    print("✓ Verify pip")
    print("✓ Install dependencies")
    print("✓ Install CloudSOC")
    print("✓ Check rclone")
    print("✓ Optionally launch CloudSOC")
    print()
    print("Security:")
    print("• No personal files will be modified")
    print("• No telemetry is collected")
    print("• No administrator privileges are required")
    print()
    answer = input("Continue? [Y/n] ").strip().lower()

    if answer not in ("", "y", "yes"):
        print("\nInstallation cancelled.")
        raise SystemExit(0)


def verify_pip() -> None:
    """Ensure pip is available or bootstrap it when possible."""
    print("[2/5] Verifying pip...\n")

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Attempting:")
        print(f"{sys.executable} -m ensurepip --upgrade")
        try:
            subprocess.run(
                [sys.executable, "-m", "ensurepip", "--upgrade"],
                cwd=ROOT,
                check=True,
            )
        except subprocess.CalledProcessError:
            print()
            print("ERROR")
            print()
            print("pip is not installed.")
            print()
            print("Installation aborted.")
            raise SystemExit(1)

    print("✓ pip is available\n")


def check_internet() -> None:
    """Ensure outbound internet access is available for package installs."""
    print("[3/5] Checking internet connectivity...\n")

    try:
        with urlopen("https://pypi.org/simple/", timeout=10):
            pass
    except (HTTPError, URLError, TimeoutError):
        print("ERROR")
        print()
        print("Internet connection required.")
        print()
        print("Installation aborted.")
        raise SystemExit(1)

    print("✓ Internet connection detected\n")


def detect_git() -> None:
    """Report whether Git is available on the system."""
    if shutil.which("git"):
        print("✓ Git detected\n")
    else:
        print("WARNING")
        print()
        print("Git not detected.")
        print()
        print("CloudSOC can still work if downloaded as ZIP.")
        print()


def detect_virtualenv() -> None:
    """Report whether the installer is running inside a virtual environment."""
    if getattr(sys, "real_prefix", None) is not None or sys.prefix != sys.base_prefix:
        print("✓ Virtual environment detected\n")
    else:
        print("INFO")
        print()
        print("No virtual environment detected.")
        print()
        print("Continuing...")
        print()


def install_dependencies() -> None:
    """Install Python dependencies and the project in editable mode."""
    print("[4/5] Installing dependencies and CloudSOC...\n")

    env = os.environ.copy()
    env.setdefault("PIP_DISABLE_PIP_VERSION_CHECK", "1")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--requirement",
            str(ROOT / "requirements.txt"),
        ],
        cwd=ROOT,
        env=env,
        check=True,
        timeout=1800,
    )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--editable",
            str(ROOT),
        ],
        cwd=ROOT,
        env=env,
        check=True,
        timeout=1800,
    )


def check_rclone() -> None:
    """Check for the optional rclone dependency."""
    print("[5/5] Checking rclone...\n")

    if shutil.which("rclone"):
        print("✓ rclone detected\n")
        return

    print("WARNING")
    print()
    print("CloudSOC will still work.")
    print()
    print("Cloud providers depending on rclone cannot be configured until rclone is installed.")
    print()
    print("Download:")
    print("https://rclone.org/downloads/")
    print()


def launch(assume_yes: bool = False, skip_launch: bool = False) -> None:
    """Optionally launch CloudSOC after a successful installation."""
    if skip_launch:
        print("Launch skipped by request.\n")
        return

    print("Launch CloudSOC now? [Y/n]")
    if not assume_yes:
        answer = input().strip().lower()
        if answer not in ("", "y", "yes"):
            return

    subprocess.run(
        [sys.executable, "-m", "cloudsoc.app"],
        cwd=ROOT,
        check=True,
    )


def done() -> None:
    """Display the completion screen."""
    line()
    print("CloudSOC installed successfully.")
    print()
    print("Launch later using")
    print()
    print("python -m cloudsoc.app")
    print()
    print("Documentation")
    print("https://github.com/DEV08-cybr/CloudSOC")
    line()


def main() -> None:
    """Run the installer workflow."""
    args = parse_args()

    try:
        banner()
        check_python()
        verify_project()
        permission(args.yes)
        verify_pip()
        check_internet()
        detect_git()
        detect_virtualenv()
        install_dependencies()
        check_rclone()
        launch(args.yes, args.skip_launch)
        done()
    except subprocess.CalledProcessError as exc:
        print("Installation failed.")
        print(f"Exit Code: {exc.returncode}")
        print()
        print("Please check:")
        print("- Internet connection")
        print("- Python installation")
        print("- pip installation")
        raise SystemExit(exc.returncode or 1) from None


if __name__ == "__main__":
    main()