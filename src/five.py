import operator
import pytest
from tools.tools import process, get_digits, timing


def get_value(mode, idx, intcodes):
    if mode == 0:
        return intcodes[idx]
    return idx


def get_intcodes(input_file):
    line = next(process(input_file))
    return [int(n) for n in line.split(",")]


def run_program(intcodes, input_value=1):
    ops = {
        1: operator.add,
        2: operator.mul,
        5: operator.ne,
        6: operator.eq,
        7: operator.lt,
        8: operator.eq,
    }

    i = 0
    output = []
    while i < len(intcodes):
        opcode, _, mode1, mode2 = get_digits(intcodes[i])
        if opcode == 9:
            break
        elif opcode == 1 or opcode == 2:
            idx1 = intcodes[i + 1]
            idx2 = intcodes[i + 2]
            idx3 = intcodes[i + 3]
            intcodes[idx3] = ops[opcode](
                get_value(mode1, idx1, intcodes), get_value(mode2, idx2, intcodes),
            )
            i += 4
        elif opcode == 3:
            idx1 = intcodes[i + 1]
            intcodes[idx1] = input_value
            i += 2
        elif opcode == 4:
            idx1 = intcodes[i + 1]
            output.append(get_value(mode1, idx1, intcodes))
            i += 2
        elif opcode == 5 or opcode == 6:
            parameter1 = get_value(mode1, intcodes[i + 1], intcodes)
            parameter2 = get_value(mode2, intcodes[i + 2], intcodes)
            if ops[opcode](parameter1, 0):
                i = parameter2
            else:
                i += 3
        elif opcode == 7 or opcode == 8:
            parameter1 = get_value(mode1, intcodes[i + 1], intcodes)
            parameter2 = get_value(mode2, intcodes[i + 2], intcodes)
            idx3 = intcodes[i + 3]
            if ops[opcode](parameter1, parameter2):
                intcodes[idx3] = 1
            else:
                intcodes[idx3] = 0
            i += 4
        else:
            print("unknown opcode", intcodes[i])
            break
    return output[-1] if output else None


def run(input_file):
    with timing("Day 5: Sunny with a Chance of Asteroids"):
        part1 = run_program(get_intcodes(input_file), 1)
        part2 = run_program(get_intcodes(input_file), 5)
    print(part1)
    print(part2)


def test_part1():
    response = run_program(get_intcodes("input/5"), 1)
    assert response == 7286649


def test_part2():
    response = run_program(get_intcodes("input/5"), 5)
    assert response == 15724522


@pytest.mark.parametrize(
    "line, input_value, expected",
    [
        pytest.param("3, 0, 4, 0, 99", 1, 1),
        pytest.param("1002, 4, 3, 4, 33", 1, None),
        pytest.param("1101, 100, -1, 4, 0", 1, None),
        pytest.param("3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9", 0, 0),
        pytest.param("3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9", 5, 1),
        pytest.param("3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1", 0, 0),
        pytest.param("3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1", 5, 1),
    ],
)
def test_examples(line, input_value, expected):
    intcodes = [int(n) for n in line.split(",")]
    response = run_program(intcodes, input_value)
    assert response == expected


@pytest.mark.parametrize(
    "line, input_value, expected",
    [
        pytest.param(
            "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99",
            7,
            999,
        ),
        pytest.param(
            "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99",
            8,
            1000,
        ),
        pytest.param(
            "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99",
            9,
            1001,
        ),
    ],
)
def test_larger_example(line, input_value, expected):
    intcodes = [int(n) for n in line.split(",")]
    response = run_program(intcodes, input_value)
    assert response == expected
