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
    current_steps = 10000
    csteps = {}
    for w, wire in enumerate(wires):
        start = Point(0, 0)
        wire_steps = 0
        for movement in wire:
            direction, steps = movement[0], int(movement[1:])
            for m in range(1, steps + 1):
                wire_steps += 1
                if direction == "R":
                    new = Point(start.x + m, start.y)
                elif direction == "L":
                    new = Point(start.x - m, start.y)
                elif direction == "U":
                    new = Point(start.x, start.y + m)
                elif direction == "D":
                    new = Point(start.x, start.y - m)
                # only count it as crossing if we are on the second wire
                if w == 1 and new in places:
                    if current_manhattan > (manhattan := abs(new.x) + abs(new.y)):
                        current_manhattan = manhattan
                    if (steps_to_here := csteps[new] + wire_steps) < current_steps:
                        current_steps = steps_to_here
                elif (
                    w == 0 and new not in csteps
                ):  # only add for the first wire and for first visit
                    places.add(new)
                    csteps[new] = wire_steps

            start = new
    print(current_manhattan, current_steps)
