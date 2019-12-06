import pytest
from tools.tools import process, timing


def criteria(number):
    n = list(str(number))
    if len(n) == len(set(n)):
        return False, False
    if n == sorted(n):
        return True, criteria2(n)
    return False, False


def count(l, x):
    return l.count(x)


def criteria2(n):
    # assumes we have checked critera first
    match2 = (count(n, x) == 2 for x in n)
    return any(match2)


def solve_part1_and_part2(low, high):
    part1_count = 0
    part2_count = 0
    for number in range(low, high):
        pass1, pass2 = criteria(number)
        if pass1:
            part1_count += 1
        if pass2:
            part2_count += 1
    return part1_count, part2_count


def run(input_file):
    for line in process(input_file):
        with timing("Day 4: Secure Container"):
            low, high = [int(n) for n in line.split("-")]
            part1, part2 = solve_part1_and_part2(low, high)
        print(part1)
        print(part2)


def test_part1_and_part2():
    part1, part2 = solve_part1_and_part2(109165, 576723)
    assert part1 == 2814
    assert part2 == 1991


@pytest.mark.parametrize(
    "number, expected",
    [
        pytest.param(111111, (True, False)),
        pytest.param(223450, (False, False)),
        pytest.param(123789, (False, False)),
        pytest.param(112233, (True, True)),
        pytest.param(123444, (True, False)),
        pytest.param(111122, (True, True)),
    ],
)
def test_criteria(number, expected):
    part1, part2 = criteria(number)
    assert (part1, part2) == expected
