from collections import deque
from dataclasses import dataclass
from itertools import permutations
import operator
import pytest
from tools.tools import process, get_digits, timing
from typing import Generator


@dataclass
class Amplifier:
    intcodes: list
    i: int
    inputs: iter


def input_gen(input_value, phase):
    yield phase
    while True:
        yield input_value


def get_value(mode, idx, intcodes):
    if mode == 0:
        return intcodes[idx]
    return idx


def get_intcodes(input_file):
    for line in process(input_file):
        return [int(n) for n in line.split(",")]


def run_program(amp):
    ops = {
        1: operator.add,
        2: operator.mul,
        5: operator.ne,
        6: operator.eq,
        7: operator.lt,
        8: operator.eq,
    }

    output = []
    while amp.i < len(amp.intcodes):
        opcode, _, mode1, mode2 = get_digits(amp.intcodes[amp.i])
        if opcode == 9:
            return output, "halt"
        elif opcode == 1 or opcode == 2:  # addition or multiplication

            idx1 = amp.intcodes[amp.i + 1]
            idx2 = amp.intcodes[amp.i + 2]
            idx3 = amp.intcodes[amp.i + 3]
            amp.intcodes[idx3] = ops[opcode](
                get_value(mode1, idx1, amp.intcodes),
                get_value(mode2, idx2, amp.intcodes),
            )
            amp.i += 4
        elif opcode == 3:  # read input
            idx1 = amp.intcodes[amp.i + 1]
            if isinstance(amp.inputs, Generator):
                amp.intcodes[idx1] = amp.inputs.send(None)
            elif len(amp.inputs) > 0:
                amp.intcodes[idx1] = amp.inputs.popleft()
            else:
                return output, None
            amp.i += 2
        elif opcode == 4:  # output
            idx1 = amp.intcodes[amp.i + 1]
            output.append(get_value(mode1, idx1, amp.intcodes))
            amp.i += 2
        elif opcode == 5 or opcode == 6:  # not equal or equal to 0
            parameter1 = get_value(mode1, amp.intcodes[amp.i + 1], amp.intcodes)
            parameter2 = get_value(mode2, amp.intcodes[amp.i + 2], amp.intcodes)
            if ops[opcode](parameter1, 0):
                amp.i = parameter2
            else:
                amp.i += 3
        elif opcode == 7 or opcode == 8:  # less than or equal
            parameter1 = get_value(mode1, amp.intcodes[amp.i + 1], amp.intcodes)
            parameter2 = get_value(mode2, amp.intcodes[amp.i + 2], amp.intcodes)
            idx3 = amp.intcodes[amp.i + 3]
            if ops[opcode](parameter1, parameter2):
                amp.intcodes[idx3] = 1
            else:
                amp.intcodes[idx3] = 0
            amp.i += 4
        else:
            print("unknown opcode", amp.intcodes[amp.i])
            break
    return output, None


def solve_part1(line):
    thruster_signal = []
    for aph, bph, cph, dph, eph in permutations(range(5), 5):
        a = Amplifier(
            intcodes=[int(n) for n in line.split(",")], i=0, inputs=input_gen(0, aph),
        )
        a_output = run_program(a)

        b = Amplifier(
            intcodes=[int(n) for n in line.split(",")],
            i=0,
            inputs=input_gen(a_output[0][0], bph),
        )
        b_output = run_program(b)

        c = Amplifier(
            intcodes=[int(n) for n in line.split(",")],
            i=0,
            inputs=input_gen(b_output[0][0], cph),
        )
        c_output = run_program(c)

        d = Amplifier(
            intcodes=[int(n) for n in line.split(",")],
            i=0,
            inputs=input_gen(c_output[0][0], dph),
        )
        d_output = run_program(d)

        e = Amplifier(
            intcodes=[int(n) for n in line.split(",")],
            i=0,
            inputs=input_gen(d_output[0][0], eph),
        )
        e_output = run_program(e)

        thruster_signal.append(e_output[0][0])
    return max(thruster_signal)


def solve_part2(line):
    thruster_signal = []

    for aph, bph, cph, dph, eph in permutations(range(5, 10), 5):
        e_output = deque([0])

        a = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([aph]))
        b = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([bph]))
        c = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([cph]))
        d = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([dph]))
        e = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([eph]))

        eh = ""
        while eh != "halt":
            a.inputs.extend(e_output)
            a_output, _ = run_program(a)

            b.inputs.extend(a_output)
            b_output, _ = run_program(b)

            c.inputs.extend(b_output)
            c_output, _ = run_program(c)

            d.inputs.extend(c_output)
            d_output, _ = run_program(d)

            e.inputs.extend(d_output)
            e_output, eh = run_program(e)
        thruster_signal.extend(e_output)
    return max(thruster_signal)


def run(input_file):
    with timing("Day 7: Amplification Circuit"):
        for line in process(input_file):
            part1 = solve_part1(line)
            part2 = solve_part2(line)
    print(part1)
    print(part2)


def test_part1_example():
    line = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
    a = Amplifier(
        intcodes=[int(n) for n in line.split(",")], i=0, inputs=input_gen(phase=4, input_value=0)
    )
    a_output = run_program(a)

    b = Amplifier(
        intcodes=[int(n) for n in line.split(",")], i=0, inputs=input_gen(phase=3, input_value=a_output[0][0])
    )
    b_output = run_program(b)

    c = Amplifier(
        intcodes=[int(n) for n in line.split(",")], i=0, inputs=input_gen(phase=2, input_value=b_output[0][0])
    )
    c_output = run_program(c)

    d = Amplifier(
        intcodes=[int(n) for n in line.split(",")], i=0, inputs=input_gen(phase=1, input_value=c_output[0][0])
    )
    d_output = run_program(d)

    e = Amplifier(
        intcodes=[int(n) for n in line.split(",")], i=0, inputs=input_gen(phase=0, input_value=d_output[0][0])
    )
    e_output = run_program(e)

    assert e_output[0][0] == 43210


def test_part1_example_2():
    line = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
    a = Amplifier(
        intcodes=[int(n) for n in line.split(",")], i=0, inputs=input_gen(phase=0, input_value=0)
    )
    a_output = run_program(a)

    b = Amplifier(
        intcodes=[int(n) for n in line.split(",")], i=0, inputs=input_gen(phase=1, input_value=a_output[0][0])
    )
    b_output = run_program(b)

    c = Amplifier(
        intcodes=[int(n) for n in line.split(",")], i=0, inputs=input_gen(phase=2, input_value=b_output[0][0])
    )
    c_output = run_program(c)

    d = Amplifier(
        intcodes=[int(n) for n in line.split(",")], i=0, inputs=input_gen(phase=3, input_value=c_output[0][0])
    )
    d_output = run_program(d)

    e = Amplifier(
        intcodes=[int(n) for n in line.split(",")], i=0, inputs=input_gen(phase=4, input_value=d_output[0][0])
    )
    e_output = run_program(e)

    assert e_output[0][0] == 54321


def test_part1_example_3():
    line = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
    a = Amplifier(
        intcodes=[int(n) for n in line.split(",")], i=0, inputs=input_gen(0, 1),
    )
    a_output = run_program(a)

    b = Amplifier(
        intcodes=[int(n) for n in line.split(",")],
        i=0,
        inputs=input_gen(a_output[0][0], 0),
    )
    b_output = run_program(b)

    c = Amplifier(
        intcodes=[int(n) for n in line.split(",")],
        i=0,
        inputs=input_gen(b_output[0][0], 4),
    )
    c_output = run_program(c)

    d = Amplifier(
        intcodes=[int(n) for n in line.split(",")],
        i=0,
        inputs=input_gen(c_output[0][0], 3),
    )
    d_output = run_program(d)

    e = Amplifier(
        intcodes=[int(n) for n in line.split(",")],
        i=0,
        inputs=input_gen(d_output[0][0], 2),
    )
    e_output = run_program(e)

    assert e_output[0][0] == 65210


def test_part2_example_1():
    line = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"

    e_output = deque([0])

    a = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([9]))
    b = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([8]))
    c = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([7]))
    d = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([6]))
    e = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([5]))

    thruster_signal = []
    eh = ""
    while eh != "halt":
        a.inputs.extend(e_output)
        a_output, _ = run_program(a)

        b.inputs.extend(a_output)
        b_output, _ = run_program(b)

        c.inputs.extend(b_output)
        c_output, _ = run_program(c)

        d.inputs.extend(c_output)
        d_output, _ = run_program(d)

        e.inputs.extend(d_output)
        e_output, eh = run_program(e)
        thruster_signal.extend(e_output)

    assert e_output[0] == 139629729

def test_part2_example_2():
    line = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"

    e_output = deque([0])

    a = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([9]))
    b = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([7]))
    c = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([8]))
    d = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([5]))
    e = Amplifier(intcodes=[int(n) for n in line.split(",")], i=0, inputs=deque([6]))

    eh = ""
    while eh != "halt":
        a.inputs.extend(e_output)
        a_output, _ = run_program(a)

        b.inputs.extend(a_output)
        b_output, _ = run_program(b)

        c.inputs.extend(b_output)
        c_output, _ = run_program(c)

        d.inputs.extend(c_output)
        d_output, _ = run_program(d)

        e.inputs.extend(d_output)
        e_output, eh = run_program(e)

    assert e_output[0] == 18216


def test_part1():
    for line in process("input/7"):
        part1 = solve_part1(line)
    assert part1 == 116680

def test_part2():
    for line in process("input/7"):
        part1 = solve_part2(line)
    assert part1 == 89603079
