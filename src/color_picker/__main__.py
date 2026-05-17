from textual import on
from textual.app import App, ComposeResult
from textual.widgets import RadioButton, RadioSet, Static, Footer, Header, Input, Label
from textual.containers import Horizontal, Grid, Container
from textual.binding import Binding
from textual.events import Resize
from textual.reactive import reactive

from color_picker.constants import COLOR_SPACES
from color_picker.widgets import PyfigletText
from color_picker.help import circle_buffer, input_formatted_string


class ColorPicker(App[None]):
    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="?", action="help", description="Show help screen", key_display="?"
        ),
    ]

    selected_space = reactive("RGB")

    def compose(self) -> ComposeResult:
        yield Header(icon="☰")

        yield PyfigletText("C o l o r  P i c k e r")

        # Static widget with color + buttons to choose color space
        with Horizontal(id="top-part"):
            with Container(id="color-container"):
                yield Static()

            radio_set = RadioSet()
            radio_set.border_subtitle = "Color Spaces"
            with radio_set:
                for color_space in COLOR_SPACES.keys():
                    yield RadioButton(color_space, value=True)

        # Inputs
        with Horizontal(id="inputs"):
            formatted_string = input_formatted_string(self.selected_space)

            for i in range(len(COLOR_SPACES[self.selected_space]["channels"])):
                yield Input(placeholder=next(formatted_string), id=f"input-{i}")

        # Displaying colors in other spaces + aesthetic RGB ASCII image
        with Horizontal(id="bottom-part"):
            with Grid():
                for color_space, specs in COLOR_SPACES.items():
                    i = circle_buffer()
                    unit = specs["unit"]

                    label = Label(
                        f"0{unit[next(i)]} 0{unit[next(i)]} 0{unit[next(i)]}",
                        id=f"label-{color_space}",
                    )
                    label.border_title = color_space
                    yield label

            yield PyfigletText("#ffffff")

        yield Footer()

    @on(RadioSet.Changed)
    def radioset_changed(self, event: RadioSet.Changed) -> None:
        self.selected_space = str(event.pressed.label)

    def watch_selected_space(self, old_space: str, new_space: str) -> None:
        try:
            self.query_one(f"#label-{old_space}", Label).remove_class("highlight")
            self.query_one(f"#label-{new_space}", Label).add_class("highlight")
        except Exception:
            pass

        formatted_string = input_formatted_string(self.selected_space)
        for i in range(len(COLOR_SPACES[self.selected_space]["channels"])):
            try:
                text_input = self.query_one(f"#input-{i}", Input)
                text_input.placeholder = str(next(formatted_string))
            except Exception:
                pass

    def on_mount(self) -> None:
        self.title = "Color Picker"
        self.sub_title = "Support five different color spaces"
        self.query_one(f"#label-{self.selected_space}", Label).add_class("highlight")

    def on_resize(self, event: Resize) -> None:
        square = self.query_one("Horizontal > #color-container", Container)
        horizontal = self.query_one("Horizontal", Horizontal)

        term_base_width = int(event.size.width * 0.06)

        square.styles.width = term_base_width * 2
        horizontal.styles.height = term_base_width


if __name__ == "__main__":
    ColorPicker().run()
