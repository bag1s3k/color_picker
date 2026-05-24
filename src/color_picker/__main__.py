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
        try:
            maximum = float(COLOR_SPACES[self.selected_space]["max"][i])
            current_input.validators = [Number(minimum=0, maximum=maximum)]
        except ValueError:

            def validate_hex_input(value_: str) -> bool:
                """Validate HEX input"""
                if not value_:
                    return True
                try:
                    converted = int(value_, 16)
                except ValueError:
                    return False

                max_ = int(COLOR_SPACES[self.selected_space]["max"][i], 16)
                return converted <= max_

            current_input.validators = [
                Function(validate_hex_input, "Invalid HEX input")
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
        inputs_amount = len(COLOR_SPACES[new_space]["channels"])
        for i in range(inputs_amount):
            text_input = self.query_one(f"#input-{i}", Input)
            text_input.styles.display = "block"
            text_input.placeholder = str(next(formatted_string))

        try:
            if (
                remaining_inputs_amount := len(COLOR_SPACES[old_space]["channels"])
                - inputs_amount
            ) > 0:
                for i in range(remaining_inputs_amount):
                    text_input = self.query_one(f"#input-{i + inputs_amount}", Input)
                    text_input.styles.display = "none"
        except KeyError:  # old_space doesn't exist on start
            pass

    def watch_channels(self, new_channels: list) -> None:
        """Update preview Labels + aesthetic HEX ASCII art according to input"""
        if not self.is_mounted:
            return

        rgb = RGB(*new_channels) #TODO: REACTIVE???

        for color_space, specs in COLOR_SPACES.items():
            print(color_space)
            convert_method = getattr(rgb, color_space.lower())

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

        ascii_art = self.query_one("#hex-ascii", PyfigletText)
        ascii_art.text = rgb.hex()[0]

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
