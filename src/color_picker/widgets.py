import pyfiglet
from textual.widgets import Static


class PyfigletText(Static):
    """Widget, which automatically generate Pyfiglet text without '\n' in the end"""

    def __init__(self, text: str, font: str = "standard", **kwargs):
        rendered_text = pyfiglet.figlet_format(text, font=font).rstrip("\n")
        super().__init__(rendered_text, **kwargs)