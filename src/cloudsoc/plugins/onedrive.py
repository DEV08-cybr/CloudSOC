"""CloudSOC OneDrive Plugin

Provides a plugin for monitoring Microsoft OneDrive via rclone.
"""

from .base import BasePlugin
from cloudsoc.services.rclone import RcloneService


class OneDrivePlugin(BasePlugin):
    """Plugin for monitoring OneDrive."""

    def __init__(self) -> None:
        super().__init__(
            name="OneDrive",
            version="1.0.0",
            author="DEEE",
            description="Monitors Microsoft OneDrive",
            provider="Microsoft",
        )

        self.rclone = RcloneService()
        self.remote = self.rclone.find_remote("onedrive")

    def initialize(self) -> None:
        print("[OneDrive] Initializing plugin...")

    def connect(self) -> bool:
        if not self.remote:
            self.connected = False
            return False

        remotes = self.rclone.list_remotes()
        self.connected = self.remote in remotes
        self.update_health(self.connected)

        return self.connected

    def disconnect(self) -> None:
        self.connected = False

    def health_check(self) -> bool:
        return self.connected

    def collect(self) -> dict:

        storage = self.rclone.about(self.remote)

        data = self.metadata()

        data.update(
        {
            "status": "Mounted" if self.connected else "Disconnected",
            "remote": self.remote,
            "used": storage.get("used", "Unknown"),
            "free": storage.get("free", "Unknown"),
            "total": storage.get("total", "Unknown"),
            "trashed": storage.get("trashed", "Unknown"),
        }
    )

        return data

    def shutdown(self) -> None:
        self.connected = False