from collections import abc, defaultdict
from dataclasses import dataclass
import operator
from tools.tools import process, timing


def get_program(line):
    intcodes = [int(n) for n in line.split(",")]
    return defaultdict(int, zip(range(len(intcodes)), intcodes))


@dataclass
class ICComputer:
    p: list
    in_data: int
    output: list
    base: int = 0
    pc: int = 0

    def get_value(self, opcode, pos):
        mode = opcode // (10 ** (pos + 1)) % 10
        idx = self.p[self.pc + pos]
        if mode == 0:
            return self.p[idx]
        elif mode == 1:
            return idx
        elif mode == 2:
            return self.p[idx + self.base]
        else:
            raise NotImplementedError("unknown mode")

    def get_index(self, inst, pos):
        mode = inst // (10 ** (pos + 1)) % 10
        idx = self.p[self.pc + pos]
        if mode == 0:
            return idx
        elif mode == 2:
            return idx + self.base
        else:
            raise NotImplementedError

    def run(self):
        ops = {
            1: operator.add,
            2: operator.mul,
            5: operator.ne,
            6: operator.eq,
            7: operator.lt,
            8: operator.eq,
        }

        while self.pc < len(self.p):
            inst = self.p[self.pc]
            opcode = inst % 100
            if opcode == 99:
                return self.output
            elif opcode == 1 or opcode == 2:  # addition or multiplication
                self.p[self.get_index(inst, 3)] = ops[opcode](
                    self.get_value(inst, 1), self.get_value(inst, 2),
                )
                self.pc += 4
            elif opcode == 3:  # read input
                self.p[self.get_index(inst, 1)] = self.in_data
                self.pc += 2
            elif opcode == 4:  # output
                data = self.get_value(inst, 1)
                self.output.append(data)
                self.pc += 2
            elif opcode == 5 or opcode == 6:  # not equal or equal to 0
                parameter1 = self.get_value(inst, 1)
                parameter2 = self.get_value(inst, 2)
                if ops[opcode](parameter1, 0):
                    self.pc = parameter2
                else:
                    self.pc += 3
            elif opcode == 7 or opcode == 8:  # less than or equal
                if ops[opcode](self.get_value(inst, 1), self.get_value(inst, 2)):
                    self.p[self.get_index(inst, 3)] = 1
                else:
                    self.p[self.get_index(inst, 3)] = 0
                self.pc += 4
            elif opcode == 9:
                self.base += self.get_value(inst, 1)
                self.pc += 2
            else:
                print("unknown opcode", self.p[self.pc])
                break
        return self.output


def run(input_file):
    line = next(process(input_file))
    with timing("Day 9: Sensor Boost"):
        part1 = ICComputer(get_program(line), 1, [])
        part2 = ICComputer(get_program(line), 2, [])
        part1.run()
        part2.run()
    print(part1.output[0])
    print(part2.output[0])


def test_part1():
    line = next(process("input/9"))
    part1 = ICComputer(get_program(line), 1, [])
    part1.run()
    assert part1.output[0] == 2775723069


def test_part2():
    line = next(process("input/9"))
    part2 = ICComputer(get_program(line), 2, [])
    part2.run()
    assert part2.output[0] == 49115


def test_part1_example1():
    line = "104,1125899906842624,99"
    c = ICComputer(get_program(line), 1, [])
    response = c.run()
    assert response[0] == 1125899906842624


def test_part1_example2():
    line = "1102,34915192,34915192,7,4,7,99,0"
    c = ICComputer(get_program(line), 1, [])
    response = c.run()
    assert response[0] == 1219070632396864


def test_part1_example_3():
    line = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    c = ICComputer(get_program(line), 1, [])
    result = c.run()
    assert result == [
        109,
        1,
        204,
        -1,
        1001,
        100,
        1,
        100,
        1008,
        100,
        16,
        101,
        1006,
        101,
        0,
        99,
    ]
