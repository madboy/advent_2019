import math
import pytest
from tools.tools import process, timing
from typing import List


def run(input_file):
    with timing("Day 16: Flawed Frequency Transmission"):
        for line in process(input_file):
            part1 = solve_part1(line, 100)
            part2 = solve_part2(line, 1)
    print(part1)
    print(part2)


def repeating_pattern(pos: int, min_length=4):
    pattern = []
    first = True
    while len(pattern) < min_length:
        # first element in the first pattern should not be included
        if first:
            pattern.extend(get_pattern(pos)[1:])
            first = False
        else:
            pattern.extend(get_pattern(pos))
    return pattern


def get_pattern(pos: int) -> List[int]:
    base = [0, 1, 0, -1]
    pattern = []
    for n in base:
        for i in range(pos):
            pattern.append(n)
    return pattern


def generate_patterns(length):
    patterns = dict()
    for position in range(1, length + 1):
        patterns[position] = repeating_pattern(position, length)
    return patterns


def solve_part1(line, phases=1):
    line = [int(c) for c in line]
    min_length = len(line)
    patterns = generate_patterns(min_length)
    for _ in range(phases):
        output = []
        for position in range(1, len(line) + 1):
            pattern = patterns[position]
            total = 0
            for a, b in zip(line, pattern):
                total += a * b
            output.append(int(str(total)[-1]))
        line = output
    return "".join([str(n) for n in line[:8]])


def solve_part2(line, phases=1):
    line = [int(c) for c in line]
    line = line * 10000
    min_length = len(line)
    patterns = generate_patterns(min_length)
    for _ in range(phases):
        output = []
        for position in range(1, len(line) + 1):
            pattern = patterns[position]
            total = 0
            for a, b in zip(line, pattern):
                total += a * b
            output.append(int(str(total)[-1]))
        line = output
    return "".join([str(n) for n in line[:8]])


def test_part1():
    response = solve_part1(next(process("input/16")), 100)
    assert response == "73127523"


def test_get_pattern():
    assert get_pattern(1) == [0, 1, 0, -1]
    assert get_pattern(2) == [0, 0, 1, 1, 0, 0, -1, -1]
    assert get_pattern(3) == [0, 0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1]


def test_repeating_pattern():
    assert repeating_pattern(1, 4) == [1, 0, -1, 0, 1, 0, -1]
    assert repeating_pattern(1, 6) == [1, 0, -1, 0, 1, 0, -1]
    assert repeating_pattern(2, 6) == [0, 1, 1, 0, 0, -1, -1]
    assert repeating_pattern(2, 10) == [0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, -1, -1]


@pytest.mark.parametrize(
    "line, phases, expected",
    [
        pytest.param("12345678", 1, "48226158"),
        pytest.param("12345678", 2, "34040438"),
        pytest.param("12345678", 3, "03415518"),
        pytest.param("80871224585914546619083218645595", 100, "24176176"),
        pytest.param("19617804207202209144916044189917", 100, "73745418"),
        pytest.param("69317163492948606335995924319873", 100, "52432133"),
    ],
)
def test_part1_example(line, phases, expected):
    response = solve_part1(line, phases=phases)
    assert response[:8] == expected


def test_part2_example():
    line = ""
    response = solve_part2(line)
    assert response == ""
