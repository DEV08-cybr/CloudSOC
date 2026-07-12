from textual.widgets import Static

from cloudsoc.core.logger import logger


class LogPanel(Static):
    """Displays recent CloudSOC events."""

    def on_mount(self):
        self.set_interval(1, self.refresh_logs)
        self.refresh_logs()

    def refresh_logs(self):

        events = logger.latest(15)

        if not events:
            self.update("CloudSOC Started...")
            return

        output = ""

        for event in events:
            output += (
                f"[{event.timestamp}] "
                f"{event.level:<8} "
                f"{event.source:<15} "
                f"{event.message}\n"
            )

        self.update(output)