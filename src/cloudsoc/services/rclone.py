"""
CloudSOC Rclone Service
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


class RcloneService:

    def __init__(self, executable: str = "rclone") -> None:
        self.executable = executable

    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [self.executable, *args],
            capture_output=True,
            text=True,
        )

    def is_installed(self) -> bool:
        return self._run("version").returncode == 0

    def list_remotes(self) -> list[str]:

        result = self._run("listremotes")

        if result.returncode != 0:
            return []

        return [
            line.strip().rstrip(":")
            for line in result.stdout.splitlines()
            if line.strip()
        ]

    def config_path(self) -> str | None:

        result = self._run("config", "file")

        if result.returncode != 0:
            return None

        for line in result.stdout.splitlines():

            if line.startswith("Configuration file"):
                continue

            if line.strip():
                return str(Path(line.strip()))

        return None

    def about(self, remote: str) -> dict:

        result = self._run("about", f"{remote}:")

        if result.returncode != 0:
            return {}

        info = {}

        for line in result.stdout.splitlines():

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            info[key.strip().lower()] = value.strip()

        return info

    # -----------------------------
    # Helpers
    # -----------------------------

    def _to_bytes(self, value: str) -> float:

        if not value:
            return 0

        match = re.match(r"([\d.]+)\s*([A-Za-z]+)", value)

        if not match:
            return 0

        number = float(match.group(1))
        unit = match.group(2).upper()

        units = {
            "B": 1,
            "KIB": 1024,
            "MIB": 1024**2,
            "GIB": 1024**3,
            "TIB": 1024**4,
        }

        return number * units.get(unit, 1)

    def usage_percent(self, remote: str) -> float:

        info = self.about(remote)

        used = self._to_bytes(info.get("used", "0 B"))
        total = self._to_bytes(info.get("total", "0 B"))

        if total == 0:
            return 0.0

        return (used / total) * 100

    def progress_bar(self, remote: str, width: int = 24) -> str:

        percent = self.usage_percent(remote)

        filled = int((percent / 100) * width)

        return "█" * filled + "░" * (width - filled)
    def find_remote(self, remote_type: str) -> str | None:
        """
        Find the first configured remote of a given type.

        Example:
            find_remote("onedrive") -> "1-DRIVE"
            find_remote("drive") -> "G-DRIVE"
        """

        config = self.config_path()

        if not config:
            return None

        current_remote = None

        with open(config, "r", encoding="utf-8") as file:

            for line in file:

                line = line.strip()

                if line.startswith("[") and line.endswith("]"):
                    current_remote = line[1:-1]

                elif line.startswith("type") and current_remote:

                    _, value = line.split("=", 1)

                    if value.strip() == remote_type:
                        return current_remote

        return None