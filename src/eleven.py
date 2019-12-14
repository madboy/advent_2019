from collections import defaultdict
from dataclasses import dataclass
import operator
from typing import Dict
from tools.tools import process, timing


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


# face = ["<", "^", ">", "v"]
FACES = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]


# @dataclass
class ICComputer:
    def __init__(
        self, p, position, base=0, pc=0, panels=None, paint=True, facing=1, start=None
    ):
        self.p = p
        self.position = position
        self.base = base
        self.pc = pc
        self.panels = panels if panels else defaultdict(int)
        self.paint = paint
        self.facing = facing
        self.start = start

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
                return self.panels
            elif opcode == 1 or opcode == 2:  # addition or multiplication
                self.p[self.get_index(inst, 3)] = ops[opcode](
                    self.get_value(inst, 1), self.get_value(inst, 2),
                )
                self.pc += 4
            elif opcode == 3:  # read input
                self.p[self.get_index(inst, 1)] = (
                    self.start if self.start else self.panels.get(self.position, 0)
                )
                if self.start:
                    self.start = None
                self.pc += 2
            elif opcode == 4:  # output
                data = self.get_value(inst, 1)
                if self.paint:
                    self.panels[self.position] = data
                    self.paint = not self.paint
                else:
                    self.facing = self.facing - 1 if data == 0 else self.facing + 1
                    self.facing %= 4
                    try:
                        self.position += FACES[self.facing]
                    except TypeError:
                        breakpoint()
                    self.paint = not self.paint
                # self.output.append(data)
                # update pos
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
        return None


def get_program(line):
    intcodes = [int(n) for n in line.split(",")]
    return defaultdict(int, zip(range(len(intcodes)), intcodes))


def run(input_file):
    with timing("Day 11: Space Police"):
        part1 = solve_part1(get_program(next(process(input_file))))
        part2 = solve_part2(get_program(next(process(input_file))))
    print(part1)
    print(part2)


def solve_part1(program):
    paint_computer = ICComputer(program, position=Point(0, 0))
    panels = paint_computer.run()
    return len(panels.keys())


def solve_part2(program):
    paint_computer = ICComputer(program, position=Point(0, 0), start=1)
    panels = paint_computer.run()
    minx = 0
    miny = 0
    maxy = 0
    maxx = 0
    for p in panels:
        if p.x < minx:
            minx = p.x
        if p.x > maxx:
            maxx = p.x

        if p.y < miny:
            miny = p.y
        if p.y > maxy:
            maxy = p.y

    response = ""
    for y in range(maxy, miny - 1, -1):
        line = ""
        for x in range(maxx, minx - 1, -1):
            line += "*" if str(panels[Point(x, y)]) == "1" else "."
        response += line[::-1] + "\n"
    return response


def test_part1():
    program = get_program(next(process("input/11")))
    paint_computer = ICComputer(program, position=Point(0, 0))
    panels = paint_computer.run()

    assert len(panels.keys()) == 2160


def test_part2():
    program = get_program(next(process("input/11")))
    paint_computer = ICComputer(program, position=Point(0, 0), start=1)
    response = solve_part2(program)

    response = response.split("\n")

    expected = [
        ".*....***..****.****..**...**..****.****...",
        ".*....*..*....*.*....*..*.*..*.*....*......",
        ".*....*..*...*..***..*....*....***..***....",
        ".*....***...*...*....*....*.**.*....*......",
        ".*....*.*..*....*....*..*.*..*.*....*......",
        ".****.*..*.****.****..**...***.*....****...",
    ]
    for i, line in enumerate(expected):
        assert line == response[i]
