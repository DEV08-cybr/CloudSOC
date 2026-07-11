"""
CloudSOC OneDrive Plugin
"""

from .base import BasePlugin
from cloudsoc.services.rclone import RcloneService


class OneDrivePlugin(BasePlugin):
    """Plugin for monitoring OneDrive."""

    def __init__(self) -> None:

        super().__init__(
            name="OneDrive",
            version="1.0",
            author="DEEE",
            description="Monitors OneDrive using rclone."
        )

        self.remote = "1-DRIVE"
        self.rclone = RcloneService()

    def initialize(self) -> None:
        print("[OneDrive] Initializing plugin...")

    def connect(self) -> bool:

        remotes = self.rclone.list_remotes()

        self.connected = self.remote in remotes

        return self.connected

    def disconnect(self) -> None:
        self.connected = False

    def health_check(self) -> bool:
        return self.connected

    def collect(self) -> dict:

        storage = self.rclone.about(self.remote)

        return {
            "service": self.name,
            "connected": self.connected,
            "status": "Mounted" if self.connected else "Disconnected",
            "remote": self.remote,
            "used": storage.get("used", "Unknown"),
            "free": storage.get("free", "Unknown"),
            "total": storage.get("total", "Unknown"),
            "trashed": storage.get("trashed", "Unknown"),
        }

    def shutdown(self) -> None:
        self.connected = False