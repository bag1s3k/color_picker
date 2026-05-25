from string import Template
from typing import TypedDict, Literal


COLOR_SPACES = {
    "RGB": {"channels": ["R", "G", "B"], "max": [255, 255, 255], "unit": ["", "", ""]},
    "HSL": {
        "channels": ["H", "S", "L"],
        "max": [360, 100, 100],
        "unit": ["°", "%", "%"],
    },
    "HSV": {
        "channels": ["H", "S", "V"],
        "max": [360, 360, 360],
        "unit": ["°", "%", "%"],
    },
    "HWB": {
        "channels": ["H", "W", "B"],
        "max": [360, 100, 100],
        "unit": ["°", "%", "%"],
    },
    "OKLCH": {"channels": ["L", "C", "H"], "max": [1, 0.4, 360], "unit": ["", "", "°"]},
    "HEX": {"channels": ["HEX"], "max": ["FFFFFF"], "unit": [""]},
}

ColorSpaceType = Literal[*COLOR_SPACES.keys()]


class AllowedKeys(TypedDict):
    """Class which contains allowed arguments for string template"""

    channel_title: str
    channel_value: float | int
    max_value: float | int
    unit: str


FORMATTED_INPUT_STR = Template("$channel_title (0 - ${max_value}${unit})")
FORMATTED_COLOR_PREVIEW = Template("${channel_value}${unit} ")
