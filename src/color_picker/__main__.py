from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input, RadioSet, Label, Header, Footer
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.binding import Binding
from textual.events import Resize
from textual.validation import Number, Function
from textual.css.query import NoMatches

from color_picker.constants import (
    COLOR_SPACES,
    FORMATTED_INPUT_STR,
    FORMATTED_COLOR_PREVIEW,
)
from color_picker.conversions import ColorState
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

    state: reactive[ColorState] = reactive(ColorState(0, 0, 0, "RGB"))

    def compose(self) -> ComposeResult:
        yield Header(icon="☰")
        yield PyfigletText("Color  Picker", font="speed")

        yield SelectColorSpace(id="select-space-panel")
        yield Inputs(id="inputs-panel")
        yield ColorPreview(id="preview-panel")

        yield Footer()

    @on(RadioSet.Changed)
    def handle_radio_change(self, event: RadioSet.Changed) -> None:
        """Update selected color space"""
        for i in range(len(COLOR_SPACES[self.state.selected_space]["channels"])):
            self.query_one(f"#input-{i}", Input).value = ""
        self.state.selected_space = str(event.pressed.label)

        self.mutate_reactive(ColorPicker.state)

    @on(Input.Changed)
    def handle_input_change(self, event: Input.Changed) -> None:
        """Update channels according to input"""
        if not (value := event.value):
            return

        i = int(str(event.input.id)[-1])
        current_input = self.query_one(f"#input-{i}", Input)
        try:
            maximum = float(COLOR_SPACES[self.state.selected_space]["max"][i])
            current_input.validators = [Number(minimum=0, maximum=maximum)]
        except ValueError:

            def validate_hex_input(value_: str) -> bool:
                """Validate HEX input"""
                if not value_:
                    return True
                elif len(value_) != 6:
                    return False
                try:
                    converted = int(value_, 16)
                except ValueError:
                    return False

                max_ = int(COLOR_SPACES[self.state.selected_space]["max"][i], 16)
                return converted <= max_

            current_input.validators = [
                Function(validate_hex_input, "Invalid HEX input")
            ]

        if not current_input.is_valid:
            return

        new_channels = self.state.channels[:]

        try:
            if value.isdecimal():
                new_channels[i] = int(value)
            elif self.state.selected_space == "HEX":
                new_channels[i] = value
            else:
                new_channels[i] = float(value)
        except ValueError:
            pass

        self.state.channels = new_channels

        self.mutate_reactive(ColorPicker.state)

    def watch_state(self) -> None:
        """Update UI based on current ColorState"""
        if not self.is_mounted:
            return

        new_space = self.state.selected_space

        for space in COLOR_SPACES.keys():
            try:
                self.query_one(f"#label-{space}", Label).remove_class("highlight")
            except NoMatches:
                pass

        try:
            self.query_one(f"#label-{new_space}", Label).add_class("highlight")
        except NoMatches:
            pass

        formatted_string = format_string(COLOR_SPACES[new_space], FORMATTED_INPUT_STR)
        inputs_amount = len(COLOR_SPACES[new_space]["channels"])

        for i in range(inputs_amount):
            try:
                text_input = self.query_one(f"#input-{i}", Input)
                text_input.styles.display = "block"
                text_input.placeholder = str(next(formatted_string))
            except NoMatches:
                pass

        for i in range(inputs_amount, 4):
            try:
                text_input = self.query_one(f"#input-{i}", Input)
                text_input.styles.display = "none"
            except NoMatches:
                pass

        for color_space, specs in COLOR_SPACES.items():
            convert_method = getattr(self.state, color_space.lower())

            formatted_string = format_string(
                specs, FORMATTED_COLOR_PREVIEW, convert_method()
            )
            new_text = "".join(
                next(formatted_string) for _ in range(len(specs["channels"]))
            )

            try:
                label = self.query_one(f"#label-{color_space}", Label)
                label.update(new_text)
            except NoMatches:
                pass

        try:
            ascii_art = self.query_one("#hex-ascii", PyfigletText)
            ascii_art.text = self.state.hex()[0]
        except NoMatches:
            pass

        ascii_art = self.query_one("#hex-ascii", PyfigletText)
        ascii_art.text = self.state.hex()[0]

    def on_mount(self) -> None:
        self.title = "Color Picker"
        self.sub_title = "Support six different color spaces"

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
