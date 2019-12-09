#!/usr/bin/env python
import asyncio
from dataclasses import dataclass
from itertools import permutations
import operator
import pytest
from tools.tools import process, timing


@dataclass
class Amplifier:
    name: str
    p: list
    in_data: asyncio.Queue
    out_data: asyncio.Queue
    pc: int = 0

    @classmethod
    def build(
        cls, name, intcodes, in_data=asyncio.Queue(), data=None,
    ):
        data = data if data else []
        amp = Amplifier(
            name=name, p=intcodes, in_data=in_data, out_data=asyncio.Queue(),
        )
        for d in data:
            amp.in_data.put_nowait(d)
        return amp

    def get_value(self, opcode, pos):
        mode = opcode // (10 ** (pos + 1)) % 10
        idx = self.p[self.pc + pos]
        if mode == 0:
            return self.p[idx]
        return idx

    async def run(self):
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
                return
            elif opcode == 1 or opcode == 2:  # addition or multiplication
                self.p[self.p[self.pc + 3]] = ops[opcode](
                    self.get_value(inst, 1), self.get_value(inst, 2),
                )
                self.pc += 4
            elif opcode == 3:  # read input
                try:
                    self.p[self.p[self.pc + 1]] = self.in_data.get_nowait()
                    self.in_data.task_done()
                    self.pc += 2
                except asyncio.QueueEmpty:
                    await asyncio.sleep(0)
            elif opcode == 4:  # output
                self.out_data.put_nowait(self.get_value(inst, 1))
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
                    self.p[self.p[self.pc + 3]] = 1
                else:
                    self.p[self.p[self.pc + 3]] = 0
                self.pc += 4
            else:
                print("unknown opcode", self.p[self.pc])
                break
        return None


async def run(input_file):
    with timing("Day 7: Amplification Circuit - async"):
        line = next(process(input_file))
        part1 = await solve_part1(line)
        part2 = await solve_part2(line)
    print(part1)
    print(part2)


async def solve_part1(line):
    thruster_signal = []
    intcodes = [int(n) for n in line.split(",")]
    for aph, bph, cph, dph, eph in permutations(range(5), 5):
        a = Amplifier.build("A", intcodes[:], data=[aph, 0])
        b = Amplifier.build("B", intcodes[:], a.out_data, [bph])
        c = Amplifier.build("C", intcodes[:], b.out_data, [cph])
        d = Amplifier.build("D", intcodes[:], c.out_data, [dph])
        e = Amplifier.build("E", intcodes[:], d.out_data, [eph])

        await a.run()
        await b.run()
        await c.run()
        await d.run()
        await e.run()
        thruster_signal.append(e.out_data.get_nowait())
    return max(thruster_signal)


async def solve_part2(line):
    intcode = [int(n) for n in line.split(",")]
    thruster_signal = []
    for aph, bph, cph, dph, eph in permutations(range(5, 10), 5):
        a = Amplifier.build("A", intcode[:])
        b = Amplifier.build("B", intcode[:], a.out_data, [bph])
        c = Amplifier.build("C", intcode[:], b.out_data, [cph])
        d = Amplifier.build("D", intcode[:], c.out_data, [dph])
        e = Amplifier.build("E", intcode[:], d.out_data, [eph])

        a.in_data = e.out_data
        a.in_data.put_nowait(aph)
        a.in_data.put_nowait(0)

        await asyncio.gather(a.run(), b.run(), c.run(), d.run(), e.run())
        thruster_signal.append(e.out_data.get_nowait())
    return max(thruster_signal)


@pytest.mark.asyncio
async def test_part1_example():
    line = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
    intcodes = [int(n) for n in line.split(",")]

    a = Amplifier.build("A", intcodes[:], data=[4, 0])
    b = Amplifier.build("B", intcodes[:], a.out_data, [3])
    c = Amplifier.build("C", intcodes[:], b.out_data, [2])
    d = Amplifier.build("D", intcodes[:], c.out_data, [1])
    e = Amplifier.build("E", intcodes[:], d.out_data, [0])

    await a.run()
    await b.run()
    await c.run()
    await d.run()
    await e.run()
    assert e.out_data.get_nowait() == 43210


@pytest.mark.asyncio
async def test_part2_example_1():
    line = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"

    intcode = [int(n) for n in line.split(",")]
    a = Amplifier.build("A", intcode[:])
    b = Amplifier.build("B", intcode[:], a.out_data, [8])
    c = Amplifier.build("C", intcode[:], b.out_data, [7])
    d = Amplifier.build("D", intcode[:], c.out_data, [6])
    e = Amplifier.build("E", intcode[:], d.out_data, [5])

    a.in_data = e.out_data
    a.in_data.put_nowait(9)
    a.in_data.put_nowait(0)

    await asyncio.gather(a.run(), b.run(), c.run(), d.run(), e.run())
    assert e.out_data.get_nowait() == 139629729


@pytest.mark.asyncio
async def test_part1():
    line = next(process("input/7"))
    part1 = await solve_part1(line)
    assert part1 == 116680


@pytest.mark.asyncio
async def test_part2():
    line = next(process("input/7"))
    part2 = await solve_part2(line)
    assert part2 == 89603079


asyncio.run(run("input/7"))
