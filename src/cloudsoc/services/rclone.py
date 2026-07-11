"""
CloudSOC Rclone Service

Provides a clean interface for interacting
with rclone across all plugins.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class RcloneService:
    """Service class for interacting with rclone."""

    def __init__(self, executable: str = "rclone") -> None:
        self.executable = executable

    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [self.executable, *args],
            capture_output=True,
            text=True,
        )

    def is_installed(self) -> bool:
        result = self._run("version")
        return result.returncode == 0

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
            if line.startswith("Configuration file is stored at:"):
                continue

            if line.strip():
                return str(Path(line.strip()))

        return None

    # -----------------------------
    # NEW
    # -----------------------------

    def about(self, remote: str) -> dict:
        """
        Returns storage information for a remote.

        Example:
        {
            "total": "100 GiB",
            "used": "204 MiB",
            "free": "99.8 GiB",
            "trashed": "0 B"
        }
        """

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