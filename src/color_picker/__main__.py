from textual.app import App, ComposeResult
from textual.widgets import RadioButton, RadioSet, Static, Footer, Header, Input
from textual.containers import Horizontal, Container
from textual.binding import Binding
from textual.events import Resize

from color_picker.constants import COLOR_SPACES


class ColorPicker(App[None]):
    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="?", action="help", description="Show help screen", key_display="?")
    ]

    selected_space = "RGB"  # TODO: hardcoded RGB

    def compose(self) -> ComposeResult:
        yield Header(icon="☰")

        with Horizontal(id="choose-color-space"):
            with Container(id="container-static"):
                yield Static()
            
            with Container(id="container-radioset"):
                with RadioSet():
                    for color_space in COLOR_SPACES.keys():
                        yield RadioButton(color_space, value=True)

        with Container(id="set-numbers"):
            with Horizontal():
                current_space = COLOR_SPACES[self.selected_space]
                for i in range(len(current_space["channels"])):
                    channel = current_space["channels"][i]
                    max_value = current_space["max"][i]
                    unit = current_space["unit"][i]
                    yield Input(placeholder=f"{channel} (0 - {max_value}{unit})")

        yield Footer()
    
    def on_mount(self) -> None:
        self.title = "Header Application"
        self.sub_title = "Subtitle"

    def on_resize(self, event: Resize) -> None:
        square = self.query_one("Horizontal > #container-static")
        horizontal = self.query_one("Horizontal")

        term_base_width = int(event.size.width * 0.06)

        square.styles.width = term_base_width * 2
        horizontal.styles.height = term_base_width

        
if __name__ == "__main__":
    ColorPicker().run()