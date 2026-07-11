"""
CloudSOC Plugin Base Class

Every CloudSOC plugin must inherit from this class.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class BasePlugin(ABC):
    """Base class for every CloudSOC plugin."""

    def __init__(
        self,
        name: str,
        version: str,
        author: str,
        description: str,
        provider: str = "Unknown",
    ) -> None:

        self.name = name
        self.version = version
        self.author = author
        self.description = description
        self.provider = provider

        self.connected = False
        self.health = "Unknown"
        self.last_check = None

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def health_check(self) -> bool:
        pass

    @abstractmethod
    def collect(self) -> dict:
        pass

    @abstractmethod
    def shutdown(self) -> None:
        pass

    # ----------------------------
    # Common helper methods
    # ----------------------------

    def update_health(self, healthy: bool) -> None:
        self.health = "Healthy" if healthy else "Unhealthy"
        self.last_check = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def metadata(self) -> dict:
        return {
            "service": self.name,
            "provider": self.provider,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "connected": self.connected,
            "health": self.health,
            "last_check": self.last_check,
        }