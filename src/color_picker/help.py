from typing import Generator


def circle_buffer() -> Generator[int]:
    """Circle buffer"""
    while True:
        yield 0
        yield 1
        yield 2
