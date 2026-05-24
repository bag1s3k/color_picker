import pyfiglet
from textual.widgets import Static, Input, RadioSet, RadioButton, Label
from textual.containers import Horizontal, Container, Grid
from textual.app import ComposeResult
from textual.validation import Number
from textual.reactive import reactive

from color_picker.constants import COLOR_SPACES


class PyfigletText(Static):
    """Widget, which automatically generate Pyfiglet text without empty line in the end"""

    text = reactive("#000000")

    def __init__(self, text: str, font: str = "standard", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font = font

    def render(self):
        raw_text = pyfiglet.figlet_format(self.text, font=self.font)

        lines = raw_text.splitlines()
        return "\n".join(lines[:-1])



class Inputs(Horizontal):
    """Represents Horizontal widget with Inputs"""

    def compose(self) -> ComposeResult:
        for i in range(3):
            yield Input(id=f"input-{i}", validators=[Number()], valid_empty=True)


class SelectColorSpace(Horizontal):
    """Represents Horizontal widget with RadioSet + square with color"""

    def compose(self) -> ComposeResult:
        with Container(id="color-container"):
            yield Static()

        radio_set = RadioSet()
        radio_set.border_subtitle = "Color Spaces"
        with radio_set:
            for color_space in COLOR_SPACES.keys():
                yield RadioButton(color_space, value=True)


class ColorPreview(Horizontal):
    """Represents Horizontal widget with color preview + aesthetic RGB ASCII image"""

    def compose(self) -> ComposeResult:
        with Grid():
            for color_space in COLOR_SPACES.keys():
                label = Label("", id=f"label-{color_space}")
                label.border_title = color_space
                yield label

        yield PyfigletText("#ffffff", id="hex-ascii")
