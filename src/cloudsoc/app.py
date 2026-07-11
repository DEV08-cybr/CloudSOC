from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static

from cloudsoc.widgets.system_stats import SystemStats
from cloudsoc.widgets.cloud_status import CloudStatus


class CloudSOC(App):
    TITLE = "CloudSOC"
    SUB_TITLE = "Cloud Security Operations Center"

    CSS_PATH = "cloudsoc.tcss"

    def compose(self) -> ComposeResult:

        yield Header()

        with Vertical():

            with Horizontal():

                with Vertical(id="left"):
                    yield SystemStats()

                with Vertical(id="right"):
                    yield CloudStatus(id="cloud")

            yield Static(
                "CloudSOC Started...",
                id="logs"
            )

        yield Footer()


if __name__ == "__main__":
    CloudSOC().run()