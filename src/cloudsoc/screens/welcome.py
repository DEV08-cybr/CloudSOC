from textual.screen import Screen
from textual.containers import Vertical
from textual.widgets import Static, Button


class WelcomeScreen(Screen):

    def compose(self):

        with Vertical(id="welcome"):

            yield Static(
"""
☁ CloudSOC

Cloud Security Operations Center

────────────────────────────────────

Welcome to CloudSOC

No cloud configured.

Configure your cloud providers.

""",
                id="title",
            )

            yield Button("Configure OneDrive", id="onedrive")
            yield Button("Configure Google Drive", id="gdrive")
            yield Button("Skip", id="skip")

    def on_button_pressed(self, event):

        self.dismiss(event.button.id)