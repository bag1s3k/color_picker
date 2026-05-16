from textual.app import App, ComposeResult
from textual.widgets import RadioButton, RadioSet, Static, Footer, Header, Input, Label
from textual.containers import Horizontal, Grid, Container
from textual.binding import Binding
from textual.events import Resize

from color_picker.constants import COLOR_SPACES
from color_picker.widgets import PyfigletText
from color_picker.help import circle_buffer


class ColorPicker(App[None]):
    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="?", action="help", description="Show help screen", key_display="?"
        ),
    ]

    selected_space = "RGB"  # TODO: hardcoded RGB

    def compose(self) -> ComposeResult:
        yield Header(icon="☰")

        yield PyfigletText("C o l o r  P i c k e r")

        with Horizontal(id="choose-color-space"):
            with Container(id="container-static"):
                yield Static()

            radio_set = RadioSet()
            radio_set.border_subtitle = "Color Spaces"
            with radio_set:
                for color_space in COLOR_SPACES.keys():
                    yield RadioButton(color_space, value=True)

        with Horizontal(id="set-numbers"):
            current_space = COLOR_SPACES[self.selected_space]
            for i in range(len(current_space["channels"])):
                channel = current_space["channels"][i]
                max_value = current_space["max"][i]
                unit = current_space["unit"][i]

                yield Input(placeholder=f"{channel} (0 - {max_value}{unit})")

        with Horizontal(id="color-spaces"):
            with Grid():
                for color_space, specs in COLOR_SPACES.items():
                    i = circle_buffer()
                    unit = specs["unit"]

                    label = Label(f"0{unit[next(i)]} 0{unit[next(i)]} 0{unit[next(i)]}")
                    label.border_title = color_space
                    yield label

            yield PyfigletText("#ffffff")

        yield Footer()

    def on_mount(self) -> None:
        self.title = "Color Picker"
        self.sub_title = "Support five different color spaces"

    def on_resize(self, event: Resize) -> None:
        square = self.query_one("Horizontal > #container-static")
        horizontal = self.query_one("Horizontal")

        term_base_width = int(event.size.width * 0.06)

        square.styles.width = term_base_width * 2
        horizontal.styles.height = term_base_width


if __name__ == "__main__":
    ColorPicker().run()
