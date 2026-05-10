from textual.app import App, ComposeResult
from textual.widgets import Label
from textual.containers import Horizontal


COLORS = ("primary", "secondary", "foreground", "background", "surface", "panel", "boost",
          "warning", "error", "success", "accent")


"""
Utility to visualize the current Textual theme's colors.
"""
class ColoredText(App[None]):
    _text = [f".text-{color} {{ color: ${color}; }}" for color in COLORS]
    _bg = [f".bg-{color} {{ background: ${color}; }}" for color in COLORS]

    CSS = "\n".join(_text + _bg)

    def compose(self) -> ComposeResult:
        for color in COLORS:
            with Horizontal():
                yield Label(f"$text-{color} ", classes=f"text-{color}")
                yield Label(f"$bg-{color}", classes=f"bg-{color}")
