from textual.app import App, ComposeResult
from textual.widgets import RadioButton, RadioSet, Static, Footer, Header
from textual.containers import Horizontal, Container
from textual.binding import Binding
from textual.events import Resize


class ColorPicker(App[None]):
    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="?", action="help", description="Show help screen", key_display="?")
    ]

    def compose(self) -> ComposeResult:
        yield Header(icon="☰")

        with Horizontal():
            with Container(id="container-static"):
                yield Static()
            
            with Container(id="container-radioset"):
                with RadioSet():
                    yield RadioButton("RGB", value=True)
                    yield RadioButton("HSV")
                    yield RadioButton("HSL")
                    yield RadioButton("HWB")
                    yield RadioButton("OKLCH")

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