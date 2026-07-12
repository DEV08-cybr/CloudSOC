from textual.app import ComposeResult
from textual.containers import Center, Middle
from textual.screen import Screen
from textual.widgets import Static
from textual.timer import Timer


class SplashScreen(Screen):
    """CloudSOC startup splash."""

    STEPS = [
        "Loading Core Engine...",
        "Loading Plugin Manager...",
        "Loading Logger...",
        "Loading Detectors...",
        "Loading Services...",
        "Detecting Cloud Providers...",
        "Preparing Dashboard...",
    ]

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                yield Static(
                    """
   ██████╗██╗      ██████╗ ██╗   ██╗██████╗ ███████╗ ██████╗  ██████╗
  ██╔════╝██║     ██╔═══██╗██║   ██║██╔══██╗██╔════╝██╔═══██╗██╔════╝
  ██║     ██║     ██║   ██║██║   ██║██║  ██║███████╗██║   ██║██║
  ██║     ██║     ██║   ██║██║   ██║██║  ██║╚════██║██║   ██║██║
  ╚██████╗███████╗╚██████╔╝╚██████╔╝██████╔╝███████║╚██████╔╝╚██████╗
   ╚═════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝ ╚═════╝  ╚══════╝

              Cloud Security Operations Center
                        Version 2.0
""",
                    id="splash_logo",
                )
                yield Static("", id="loading_text")

    def on_mount(self) -> None:
        self.step = 0
        self.lines = []
        self.timer = self.set_interval(0.45, self.animate)

    def animate(self) -> None:
        if self.step < len(self.STEPS):
            self.lines.append(f"✓ {self.STEPS[self.step]}")
            self.query_one("#loading_text", Static).update(
                "\n".join(self.lines)
            )
            self.step += 1
        else:
            self.timer.stop()
            self.dismiss()
