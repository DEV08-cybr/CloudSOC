from textual.widgets import Static
import psutil


class SystemStats(Static):

    def on_mount(self) -> None:
        self.set_interval(1, self.refresh_stats)
        self.refresh_stats()

    def bar(self, value: float, width: int = 20) -> str:
        filled = int((value / 100) * width)
        return "█" * filled + "░" * (width - filled)

    def refresh_stats(self) -> None:

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        disk = psutil.disk_usage("/").percent

        net = psutil.net_io_counters()

        up = net.bytes_sent / (1024 * 1024)

        down = net.bytes_recv / (1024 * 1024)

        self.update(
f"""🖥 SYSTEM

CPU
{self.bar(cpu)} {cpu:.1f}%

RAM
{self.bar(ram)} {ram:.1f}%

DISK
{self.bar(disk)} {disk:.1f}%

NET ↑ {up:.2f} MB

NET ↓ {down:.2f} MB
"""
        )