from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer

from cloudsoc.screens.splash import SplashScreen
from cloudsoc.widgets.system_stats import SystemStats
from cloudsoc.widgets.cloud_status import CloudStatus
from cloudsoc.widgets.log_panel import LogPanel

from cloudsoc.screens.welcome import WelcomeScreen
from cloudsoc.services.rclone import RcloneService
from cloudsoc.plugins.manager import PluginManager


class CloudSOC(App):
    TITLE = "CloudSOC"
    SUB_TITLE = "Cloud Security Operations Center"

    CSS_PATH = "cloudsoc.tcss"

    def on_mount(self) -> None:
        self.push_screen(SplashScreen())
        manager = PluginManager()
        
        if not manager.has_configured_plugins():
            self.push_screen(WelcomeScreen())

    def compose(self) -> ComposeResult:

        yield Header()

        with Vertical():

            with Horizontal():

                with Vertical(id="left"):
                    yield SystemStats()

                with Vertical(id="right"):
                    yield CloudStatus(id="cloud")

            yield LogPanel(id="logs")

        yield Footer()


if __name__ == "__main__":
    CloudSOC().run()