from collections import defaultdict
from dataclasses import dataclass
import operator
from tools.tools import process, timing


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

    def __lt__(self, other):
        return self.x < other.x

    def __gt__(self, other):
        return self.x > other.x


def get_program(line):
    intcodes = [int(n) for n in line.split(",")]
    return defaultdict(int, zip(range(len(intcodes)), intcodes))


def draw_screen(tiles):
    # does not include the score
    tile_face = {0: ".", 1: "#", 2: "=", 3: "-", 4: "*"}

    for y in range(20):
        line = ""
        for x in range(38):
            line += tile_face[tiles.get(Point(x, y), 0)]
        print(line)


class ICComputer:
    def __init__(self, p, in_data=0, quarters=None):
        self.p = p
        if quarters:
            self.p[0] = quarters
        self.in_data = in_data
        self.output = []
        self.base = 0
        self.pc = 0
        self.tiles = {}
        self.ball = None
        self.paddle = None

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
            # move our paddle towards the ball on every tick
            if self.ball and self.paddle:
                if self.ball.x > self.paddle.x:
                    self.in_data = 1
                elif self.ball.x < self.paddle.x:
                    self.in_data = -1
                else:
                    self.in_data = 0
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
            # 0 is an empty tile. No game object appears in this tile.
            # 1 is a wall tile. Walls are indestructible barriers.
            # 2 is a block tile. Blocks can be broken by the ball.
            # 3 is a horizontal paddle tile. The paddle is indestructible.
            # 4 is a ball tile. The ball moves diagonally and bounces off objects.
            elif opcode == 4:  # output
                data = self.get_value(inst, 1)
                self.output.append(data)
                if len(self.output) == 3:
                    # update tiles
                    x, y, _id = self.output
                    self.tiles[Point(x, y)] = _id
                    self.output = []
                    if _id == 3:
                        self.paddle = Point(x, y)
                    elif _id == 4:
                        self.ball = Point(x, y)
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
    with timing("Day 13: Care Package"):
        part1 = solve_part1(line)
        part2 = solve_part2(line)
    print(part1)
    print(part2)


def solve_part1(line):
    part1 = ICComputer(get_program(line))
    part1.run()
    count = 0
    for v in part1.tiles.values():
        if v == 2:
            count += 1
    return count


def solve_part2(line):
    part2 = ICComputer(get_program(line), quarters=2)
    part2.run()
    return part2.tiles[Point(-1, 0)]


def test_part1():
    line = next(process("input/13"))
    assert solve_part1(line) == 205


def test_part2():
    line = next(process("input/13"))
    assert solve_part2(line) == 10292
