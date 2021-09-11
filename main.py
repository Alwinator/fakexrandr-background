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
        self.width = 0
        self.height = 0
        self.left = 0
        self.top = 0

    def __repr__(self):
        return f"Display({self.name}, w={self.width}, h={self.height}, l={self.left}, t={self.top})"


def parse_randr(lines: List[str]):
    screen = None

    for line in lines:
        line = line.strip().split()

        if line[0] != " ":
            if line[0] == "Screen":
                screen = Screen(line)
            elif line[1] == "connected":
                screen.displays.append(Display(line))

    return screen


def main():
    result = os.popen('xrandr')
    screen = parse_randr(result.readlines())
    print(screen)


if __name__ == '__main__':
    main()
