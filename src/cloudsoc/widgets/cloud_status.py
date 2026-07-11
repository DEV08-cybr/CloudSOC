from textual.widgets import Static

from cloudsoc.plugins.manager import PluginManager


class CloudStatus(Static):
    """Displays cloud status using PluginManager."""

    def on_mount(self) -> None:
        self.manager = PluginManager()
        self.set_interval(2, self.update_status)
        self.update_status()

    def make_bar(self, percent: float, width: int = 20) -> str:
        filled = int((percent / 100) * width)
        return "█" * filled + "░" * (width - filled)

    def usage_percent(self, used: str, total: str) -> float:
        try:
            used_value = float(used.split()[0])
            used_unit = used.split()[1]

            total_value = float(total.split()[0])
            total_unit = total.split()[1]

            units = {
                "B": 1,
                "KiB": 1024,
                "MiB": 1024**2,
                "GiB": 1024**3,
                "TiB": 1024**4,
            }

            used_bytes = used_value * units[used_unit]
            total_bytes = total_value * units[total_unit]

            return (used_bytes / total_bytes) * 100

        except Exception:
            return 0.0

    def update_status(self) -> None:

        self.manager.initialize_all()
        self.manager.connect_all()

        clouds = self.manager.collect_all()

        output = ""

        for cloud in clouds:
            status = "🟢" if cloud["connected"] else "🔴"

            percent = self.usage_percent(
                cloud["used"],
                cloud["total"],
            )

            bar = self.make_bar(percent)

            output += (
                f"{status} {cloud['service']}\n"
                f"Provider : {cloud.get('provider', '-')}\n"
                f"Health   : {cloud.get('health', '-')}\n"
                f"Last Scan: {cloud.get('last_check', '-')}\n"
                f"Remote   : {cloud['remote']}\n"
                f"Usage    : {bar} {percent:.1f}%\n"
                f"Used     : {cloud['used']}\n"
                f"Free     : {cloud['free']}\n"
                f"Total    : {cloud['total']}\n\n"
            )

        output += (
            "🟡 Telegram      [Plugin Available]\n"
            "🔵 Dropbox       [Plugin Available]\n"
            "🟠 AWS S3        [Plugin Available]\n"
            "🔷 Azure Blob    [Plugin Available]\n"
            "🟢 Nextcloud     [Plugin Available]\n"
            "⚫ Mega          [Plugin Available]\n"
            "🟣 Box           [Plugin Available]\n"
        )

        self.update(output)