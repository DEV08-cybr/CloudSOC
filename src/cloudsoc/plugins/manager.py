"""
CloudSOC Plugin Manager

Automatically discovers and loads all plugins.
"""

from importlib import import_module
from pathlib import Path
import inspect

from .base import BasePlugin


class PluginManager:
    """Automatically loads every CloudSOC plugin."""

    def __init__(self) -> None:
        self.plugins: list[BasePlugin] = []
        self.load_plugins()

    def load_plugins(self) -> None:

        plugin_dir = Path(__file__).parent

        for file in plugin_dir.glob("*.py"):

            if file.stem in (
                "__init__",
                "base",
                "manager",
            ):
                continue

            module = import_module(f"cloudsoc.plugins.{file.stem}")

            for _, obj in inspect.getmembers(module, inspect.isclass):

                if (
                    issubclass(obj, BasePlugin)
                    and obj is not BasePlugin
                ):
                    self.plugins.append(obj())

    def initialize_all(self):
        for plugin in self.plugins:
            plugin.initialize()

    def connect_all(self):
        for plugin in self.plugins:
            plugin.connect()

    def disconnect_all(self):
        for plugin in self.plugins:
            plugin.disconnect()

    def shutdown_all(self):
        for plugin in self.plugins:
            plugin.shutdown()

    def collect_all(self):
        return [plugin.collect() for plugin in self.plugins]