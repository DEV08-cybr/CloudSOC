from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    """Represents a CloudSOC event."""

    level: str
    source: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)

    def format(self) -> str:
        return (
            f"[{self.timestamp.strftime('%H:%M:%S')}] "
            f"{self.level:<8} "
            f"{self.source:<15} "
            f"{self.message}"
        )