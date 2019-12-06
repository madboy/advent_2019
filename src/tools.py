import contextlib
import pytest
import time


def process(filename):
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()


def left_pad_process(filename):
    """
    In some cases we do not want to remove the white space on the 
    left side of the input
    """
    with open(filename, "r") as f:
        for line in f:
            yield line.rstrip()


def turn(current_direction, turn_direction):
    directions = {"left": 0, "up": 1, "right": 2, "down": 3}
    rdirections = {0: "left", 1: "up", 2: "right", 3: "down"}
    turns = {"left": -1, "right": 1, "straight": 0}
    new_direction = (directions[current_direction] + turns[turn_direction]) % 4
    return rdirections[new_direction]


@contextlib.contextmanager
def timing(name=""):
    """
    Variation of:
    https://github.com/anthonywritescode/aoc2019/blob/master/support/support.py
    """
    before = time.time_ns()
    try:
        yield
    finally:
        after = time.time_ns()

        unit = "μs"
        if (t := (after - before) // 1000) > 10000:
            t //= 1000
            unit = "ms"
        print(f"{name} -> {int(t)} {unit}")


def get_digits(number):
    ones = number % 10
    tens = (number // 10) % 10
    hundreds = (number // 100) % 10
    thousands = (number // 1000) % 10
    return ones, tens, hundreds, thousands


@pytest.mark.parametrize(
    "numbers,expected",
    [
        pytest.param(1, (1, 0, 0, 0)),
        pytest.param(21, (1, 2, 0, 0)),
        pytest.param(340, (0, 4, 3, 0)),
        pytest.param(1234, (4, 3, 2, 1)),
        pytest.param(19002, (2, 0, 0, 9)),
    ],
)
def test_get_digits_all(numbers, expected):
    response = get_digits(numbers)
    assert response == expected
