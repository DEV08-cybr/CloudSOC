"""
CloudSOC Logger
"""

from collections import deque

from cloudsoc.core.event import Event


class EventLogger:
    """Stores CloudSOC events."""

    def __init__(self, limit: int = 100) -> None:
        self.events = deque(maxlen=limit)

    def log(self, level: str, source: str, message: str) -> Event:
        event = Event(
            level=level,
            source=source,
            message=message,
        )

        self.events.append(event)

        print(
            f"[{event.timestamp}] "
            f"{event.level:<8} "
            f"{event.source:<15} "
            f"{event.message}"
        )

        return event

    def info(self, source: str, message: str):
        return self.log("INFO", source, message)

    def success(self, source: str, message: str):
        return self.log("SUCCESS", source, message)

    def warning(self, source: str, message: str):
        return self.log("WARNING", source, message)

    def error(self, source: str, message: str):
        return self.log("ERROR", source, message)

    def critical(self, source: str, message: str):
        return self.log("CRITICAL", source, message)

    def get_events(self):
        return list(self.events)

    def latest(self, count: int = 20):
        return self.get_events()[-count:]

    def clear(self):
        self.events.clear()


# Global logger
logger = EventLogger()