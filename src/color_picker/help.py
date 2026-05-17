from typing import Generator

from color_picker.constants import COLOR_SPACES


def circle_buffer() -> Generator[int]:
    """Circle buffer"""
    while True:
        yield 0
        yield 1
        yield 2


def input_formatted_string(color_space: str) -> Generator[str]:
    """Return formatted string for input's placeholder"""

    current_space = COLOR_SPACES[color_space]
    for i in range(len(current_space["channels"])):
        channel = current_space["channels"][i]
        max_value = current_space["max"][i]
        unit = current_space["unit"][i]

        yield f"{channel} (0 - {max_value}{unit})"
