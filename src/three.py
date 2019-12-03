from dataclasses import dataclass
from src.tools import process


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def run(input_file):
    wires = []
    for line in process(input_file):
        wires.append([m for m in line.split(",")])

    places = set()
    current_manhattan = 10000
    for wire in wires:
        start = Point(0, 0)
        for movement in wire:
            direction, steps = movement[0], int(movement[1:])
            for m in range(1, steps + 1):
                if direction == "R":
                    new = Point(start.x + m, start.y)
                if direction == "L":
                    new = Point(start.x - m, start.y)
                if direction == "U":
                    new = Point(start.x, start.y + m)
                if direction == "D":
                    new = Point(start.x, start.y - m)
                if new in places:
                    manhattan = abs(new.x) + abs(new.y)
                    if current_manhattan > manhattan:
                        current_manhattan = manhattan
                else:
                    places.add(new)

            start = new
    print(current_manhattan)


def solve(input):
    pass
