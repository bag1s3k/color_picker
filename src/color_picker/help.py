from string import Template
from typing import Generator

from color_picker.constants import AllowedKeys


def format_string(
    color_space: dict, template: Template, channel_values: list[int | float] = None
) -> Generator[str]:
    """Return formatted string according to template"""

    def render_template(allowed: AllowedKeys):
        """Render string template"""
        return template.substitute(allowed)

    for i in range(len(color_space["channels"])):
        template_map: AllowedKeys = {
            "channel_title": color_space["channels"][i],
            "channel_value": channel_values[i] if channel_values else 0,
            "max_value": color_space["max"][i],
            "unit": color_space["unit"][i],
        }

        yield render_template(template_map)
