from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input, RadioSet, Label, Header, Footer
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.binding import Binding
from textual.events import Resize
from textual.validation import Number
from textual.css.query import NoMatches

from color_picker.constants import (
    COLOR_SPACES,
    FORMATTED_INPUT_STR,
    FORMATTED_COLOR_PREVIEW,
)
from color_picker.conversions import RGB
from color_picker.help import format_string
from color_picker.widgets import PyfigletText, Inputs, SelectColorSpace, ColorPreview


class ColorPicker(App[None]):
    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="?", action="help", description="Show help screen", key_display="?"
        ),
    ]

    selected_space = reactive("RGB")
    channels: reactive[list[int | float]] = reactive([0, 0, 0])

    def compose(self) -> ComposeResult:
        yield Header(icon="☰")
        yield PyfigletText("C o l o r  P i c k e r")

        yield SelectColorSpace(id="select-space-panel")
        yield Inputs(id="inputs-panel")
        yield ColorPreview(id="preview-panel")

        yield Footer()

    @on(RadioSet.Changed)
    def handle_radio_change(self, event: RadioSet.Changed) -> None:
        """Update selected color space"""
        for i in range(len(COLOR_SPACES[self.selected_space]["channels"])):
            self.query_one(f"#input-{i}", Input).value = ""
        self.selected_space = str(event.pressed.label)

    @on(Input.Changed)
    def handle_input_change(self, event: Input.Changed) -> None:
        """Update channels according to input"""
        if not (value := event.value):
            return

        i = int(str(event.input.id)[-1])
        current_input = self.query_one(f"#input-{i}", Input)
        current_input.validators = [
            Number(minimum=0, maximum=COLOR_SPACES[self.selected_space]["max"][i])
        ]

        if not current_input.is_valid:
            return

        try:
            if value.isdecimal():
                self.channels[i] = int(value)
            else:
                self.channels[i] = float(value)
        except ValueError:
            pass

        self.mutate_reactive(ColorPicker.channels)

    def watch_selected_space(self, old_space: str, new_space: str) -> None:
        """Update Input's placeholder and highlight of preview according to selected space"""
        if not self.is_mounted:
            return

        try:
            self.query_one(f"#label-{old_space}", Label).remove_class("highlight")
        except NoMatches:
            pass
        self.query_one(f"#label-{new_space}", Label).add_class("highlight")

        formatted_string = format_string(COLOR_SPACES[new_space], FORMATTED_INPUT_STR)
        for i in range(len(COLOR_SPACES[new_space]["channels"])):
            text_input = self.query_one(f"#input-{i}", Input)
            text_input.placeholder = str(next(formatted_string))

    def watch_channels(self, new_channels: list) -> None:
        """Update preview Labels according to input"""
        if not self.is_mounted:
            return

        tmp2 = RGB(*new_channels)

        for color_space, specs in COLOR_SPACES.items():
            convert_method = getattr(tmp2, color_space.lower())

            tmp = format_string(specs, FORMATTED_COLOR_PREVIEW, convert_method())
            new_text = "".join(next(tmp) for _ in range(len(self.channels)))

            try:
                label = self.query_one(f"#label-{color_space}", Label)
                label.update(new_text)
            except NoMatches:
                pass

    def on_mount(self) -> None:
        self.title = "Color Picker"
        self.sub_title = "Support five different color spaces"

        self.watch_selected_space("", self.selected_space)
        self.watch_channels(self.channels)

    def on_resize(self, event: Resize) -> None:
        try:
            square = self.query_one("#color-container", Container)
            horizontal = self.query_one("#select-space-panel", Horizontal)

            term_base_width = int(event.size.width * 0.06)
            square.styles.width = term_base_width * 2
            horizontal.styles.height = term_base_width
        except NoMatches:
            pass


if __name__ == "__main__":
    ColorPicker().run()
