"""
CloudSOC Plugin Manager

Responsible for loading, managing, and controlling
all CloudSOC plugins.
"""

from typing import List

from .base import BasePlugin


class PluginManager:
    """Manages all CloudSOC plugins."""

    def __init__(self) -> None:
        self.plugins: List[BasePlugin] = []

    def register(self, plugin: BasePlugin) -> None:
        """Register a new plugin."""
        self.plugins.append(plugin)

    def initialize_all(self) -> None:
        """Initialize every plugin."""
        for plugin in self.plugins:
            plugin.initialize()

    def connect_all(self) -> None:
        """Connect every plugin."""
        for plugin in self.plugins:
            plugin.connect()

    def disconnect_all(self) -> None:
        """Disconnect every plugin."""
        for plugin in self.plugins:
            plugin.disconnect()

    def shutdown_all(self) -> None:
        """Shutdown every plugin."""
        for plugin in self.plugins:
            plugin.shutdown()

    def collect_all(self) -> list[dict]:
        """Collect data from every plugin."""
        data = []

        for plugin in self.plugins:
            data.append(plugin.collect())

        return data