"""
CloudSOC Plugin Base Class

Every CloudSOC plugin must inherit from this class.
It defines the standard interface that all plugins
must implement.
"""

from abc import ABC, abstractmethod


class BasePlugin(ABC):
    """Abstract base class for all CloudSOC plugins."""

    def __init__(
        self,
        name: str,
        version: str,
        author: str,
        description: str,
    ) -> None:
        self.name = name
        self.version = version
        self.author = author
        self.description = description

        self.connected = False

    @abstractmethod
    def initialize(self) -> None:
        """Prepare the plugin before use."""
        pass

    @abstractmethod
    def connect(self) -> bool:
        """Connect to the target service."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the target service."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check whether the plugin is healthy."""
        pass

    @abstractmethod
    def collect(self) -> dict:
        """Collect data from the service."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the plugin gracefully."""
        pass