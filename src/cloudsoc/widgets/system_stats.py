from textual.widgets import Static
import psutil


class SystemStats(Static):

    def on_mount(self):
        self.set_interval(1, self.refresh_stats)
        self.refresh_stats()

    def refresh_stats(self):

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory()

        disk = psutil.disk_usage("/")

        self.update(f"""
🖥 SYSTEM

CPU
 {cpu:.1f} %

RAM
 {ram.percent:.1f} %

DISK
 {disk.percent:.1f} %
""")