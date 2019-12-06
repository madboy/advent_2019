import operator
from src.tools import process, get_digits


def get_value(mode, idx, intcodes):
    if mode == 0:
        return intcodes[idx]
    return idx


ops = {1: operator.add, 2: operator.mul}


def run_program(intcodes, input_value=1):
    i = 0
    while i < len(intcodes):
        opcode, _, mode1, mode2 = get_digits(intcodes[i])
        if opcode == 9:
            break
        elif opcode == 1:
            idx1 = intcodes[i + 1]
            idx2 = intcodes[i + 2]
            idx3 = intcodes[i + 3]
            intcodes[idx3] = get_value(mode1, idx1, intcodes) + get_value(
                mode2, idx2, intcodes
            )
            i += 4
        elif opcode == 2:
            idx1 = intcodes[i + 1]
            idx2 = intcodes[i + 2]
            idx3 = intcodes[i + 3]
            intcodes[idx3] = get_value(mode1, idx1, intcodes) * get_value(
                mode2, idx2, intcodes
            )
            i += 4
        elif opcode == 3:
            idx1 = intcodes[i + 1]
            intcodes[idx1] = input_value
            i += 2
        elif opcode == 4:
            print("output: ", get_value(mode1, intcodes[i + 1], intcodes))
            i += 2
        else:
            print("unknown opcode", intcodes[i])
            break


def run(input_file):
    for line in process(input_file):
        run_program([int(n) for n in line.split(",")])


def solve(input):
    pass
