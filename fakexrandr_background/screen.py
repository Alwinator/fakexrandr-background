import os
from typing import List


class Screen:
    def __init__(self, line):
        self.width = int(line[7])
        self.height = int(line[9][:-1])
        self.displays = []

    def __repr__(self):
        return f"Screen(w={self.width}, h={self.height}, displays={self.displays})"


class Display:
    def __init__(self, line: List[str]):
        self.name = line[0]

        raw_dim = line[2]

        if raw_dim == "primary":
            raw_dim = line[3]

        dim = raw_dim.split("+")
        res = dim[0].split("x")

        self.width = int(res[0])
        self.height = int(res[1])
        self.left = int(dim[1])
        self.top = int(dim[2])

    def __repr__(self):
        return f"Display({self.name}, w={self.width}, h={self.height}, l={self.left}, t={self.top})"


def parse_randr(lines: List[str]) -> Screen:
    screen = None

    for line in lines:
        line = line.strip().split()

        if line[0] != " ":
            if line[0] == "Screen":
                screen = Screen(line)
            elif line[1] == "connected":
                screen.displays.append(Display(line))

    return screen


def get_screen() -> Screen:
    result = os.popen('xrandr')
    return parse_randr(result.readlines())
