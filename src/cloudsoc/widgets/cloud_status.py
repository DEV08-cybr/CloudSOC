from textual.widgets import Static

from cloudsoc.services.rclone import RcloneService


class CloudStatus(Static):
    """Displays connected cloud services."""

    def on_mount(self) -> None:
        self.update_status()

    def update_status(self) -> None:
        service = RcloneService()

        if not service.is_installed():
            self.update("❌ Rclone not installed")
            return

        remotes = service.list_remotes()

        if not remotes:
            self.update("⚠ No cloud remotes found")
            return

        output = ""

        for remote in remotes:
            output += f"🟢 {remote}\n"

        self.update(output)