"""
CloudSOC Google Drive Plugin
"""


from .base import BasePlugin
from cloudsoc.services.rclone import RcloneService


class GoogleDrivePlugin(BasePlugin):
    """Plugin for monitoring Google Drive."""

    def __init__(self) -> None:

        super().__init__(
    name="Google Drive",
    version="1.0.0",
    author="DEEE",
    description="Monitors Google Drive",
    provider="Google",
    )
        

        self.rclone = RcloneService()
        self.remote = self.rclone.find_remote("drive")

    def initialize(self) -> None:
        pass

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