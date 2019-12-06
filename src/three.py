from dataclasses import dataclass
import pytest
from src.tools import process


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def get_wires(input_file):
    wires = []
    for line in process(input_file):
        wires.append([m for m in line.split(",")])
    return wires


def run(input_file):
    part1, part2 = solve_part1_and_part2(get_wires(input_file))
    print(part1)
    print(part2)


def solve_part1_and_part2(wires):
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
    return (current_manhattan, current_steps)


@pytest.mark.parametrize(
    "wires,expected",
    [
        pytest.param(
            [
                ["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"],
                ["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"],
            ],
            (159, 610),
        ),
        pytest.param(
            [
                [
                    "R98",
                    "U47",
                    "R26",
                    "D63",
                    "R33",
                    "U87",
                    "L62",
                    "D20",
                    "R33",
                    "U53",
                    "R51",
                ],
                ["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"],
            ],
            (135, 410),
        ),
    ],
)
def test_part1_and_part2_examples(wires, expected):
    response = solve_part1_and_part2(wires)
    assert response == expected


def test_part1_and_part2():
    wires = get_wires("input/3")
    part1, part2 = solve_part1_and_part2(wires)
    assert part1 == 860
    assert part2 == 9238
