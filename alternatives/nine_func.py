from collections import defaultdict
import operator
from tools.tools import process, timing


def icc(line, in_data, base=0, pc=0):
    def load_program(line):
        intcodes = [int(n) for n in line.split(",")]
        return defaultdict(int, zip(range(len(intcodes)), intcodes))

    def get_value(opcode, pos):
        mode = opcode // (10 ** (pos + 1)) % 10
        idx = p[pc + pos]
        if mode == 0:
            return p[idx]
        elif mode == 1:
            return idx
        elif mode == 2:
            return p[idx + base]
        else:
            raise NotImplementedError("unknown mode")

    def get_index(inst, pos):
        mode = inst // (10 ** (pos + 1)) % 10
        idx = p[pc + pos]
        if mode == 0:
            return idx
        elif mode == 2:
            return idx + base
        else:
            raise NotImplementedError

    ops = {
        1: operator.add,
        2: operator.mul,
        5: operator.ne,
        6: operator.eq,
        7: operator.lt,
        8: operator.eq,
    }

    output = []
    p = load_program(line)
    while pc < len(p):
        inst = p[pc]
        opcode = inst % 100
        if opcode == 99:
            return output
        elif opcode == 1 or opcode == 2:  # addition or multiplication
            p[get_index(inst, 3)] = ops[opcode](get_value(inst, 1), get_value(inst, 2),)
            pc += 4
        elif opcode == 3:  # read input
            p[get_index(inst, 1)] = in_data
            pc += 2
        elif opcode == 4:  # output
            data = get_value(inst, 1)
            output.append(data)
            pc += 2
        elif opcode == 5 or opcode == 6:  # not equal or equal to 0
            parameter1 = get_value(inst, 1)
            parameter2 = get_value(inst, 2)
            if ops[opcode](parameter1, 0):
                pc = parameter2
            else:
                pc += 3
        elif opcode == 7 or opcode == 8:  # less than or equal
            if ops[opcode](get_value(inst, 1), get_value(inst, 2)):
                p[get_index(inst, 3)] = 1
            else:
                p[get_index(inst, 3)] = 0
            pc += 4
        elif opcode == 9:
            base += get_value(inst, 1)
            pc += 2
        else:
            print("unknown opcode", p[pc])
            break
    return output


line = next(process("input/9"))
with timing("Day 9: Sensor Boost"):
    part1 = icc(line, 1)
    part2 = icc(line, 2)
print(part1[0])
print(part2[0])
