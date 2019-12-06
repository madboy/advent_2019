import pytest
from src.tools import process, timing


def get_intcodes(input_file):
    for line in process(input_file):
        return [int(n) for n in line.split(",")]


def run(input_file):
    with timing("Day 2: 1202 Program Alarm"):
        part1 = solve_part1(get_intcodes(input_file))
        part2 = solve_part2(get_intcodes(input_file))
    print(part1)
    print(part2)


def run_program(intcodes):
    i = 0
    while i < len(intcodes):
        if intcodes[i] == 99:
            break
        else:
            idx1 = intcodes[i + 1]
            idx2 = intcodes[i + 2]
            idx3 = intcodes[i + 3]
            if intcodes[i] == 1:
                intcodes[idx3] = intcodes[idx1] + intcodes[idx2]
            elif intcodes[i] == 2:
                intcodes[idx3] = intcodes[idx1] * intcodes[idx2]
            i += 4
    return intcodes[0]


def solve_part1(intcodes):
    intcodes[1] = 12
    intcodes[2] = 2

    return run_program(intcodes)


def solve_part2(intcodes):
    for one in range(100):
        for two in range(100):
            intcodes_c = intcodes[:]  # resetting the memory banks
            intcodes_c[1] = one
            intcodes_c[2] = two
            r = run_program(intcodes_c)
            if r // 10000 == 1969:
                if r == 19690720:
                    return 100 * one + two
            else:
                # leading values increase with each one, and then incrementally with each two,
                # so we don't need to check for all leading values
                break


@pytest.mark.parametrize(
    "intcodes,response,expected",
    [
        pytest.param([1, 0, 0, 0, 99], 2, [2, 0, 0, 0, 99]),
        pytest.param([2, 3, 0, 3, 99], 2, [2, 3, 0, 6, 99]),
        pytest.param([2, 4, 4, 5, 99, 0], 2, [2, 4, 4, 5, 99, 9801]),
        pytest.param([1, 1, 1, 4, 99, 5, 6, 0, 99], 30, [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ],
)
def test_part1_example(intcodes, response, expected):
    assert run_program(intcodes) == response
    assert intcodes == expected


def test_part1():
    assert solve_part1(get_intcodes("input/2")) == 4462686


def test_part2():
    assert solve_part2(get_intcodes("input/2")) == 5936
