import copy
from dataclasses import dataclass
from math import gcd
from itertools import permutations, combinations
from tools.tools import process, timing


@dataclass(eq=True)
class Vector:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __next__(self):
        yield self.x
        yield self.y
        yield self.z

    def __iter__(self):
        return next(self)

    def __abs__(self):
        return Vector(abs(self.x), abs(self.y), abs(self.z))

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def state(self):
        return f"{self.x},{self.y},{self.z}"


@dataclass
class Moon:
    pos: Vector
    vel: Vector

    def potential(self):
        return sum(abs(self.pos))

    def kinetic(self):
        return sum(abs(self.vel))

    def __eq__(self, other):
        return self.pos == other.pos and self.vel == self.pos

    def __hash__(self):
        return hash((self.pos, self.vel))


def tick(moons):
    for m1, m2 in combinations(moons, 2):
        if m1.pos.x < m2.pos.x:
            m1.vel.x += 1
            m2.vel.x -= 1
        elif m1.pos.x > m2.pos.x:
            m1.vel.x -= 1
            m2.vel.x += 1

        if m1.pos.y < m2.pos.y:
            m1.vel.y += 1
            m2.vel.y -= 1
        elif m1.pos.y > m2.pos.y:
            m1.vel.y -= 1
            m2.vel.y += 1

        if m1.pos.z < m2.pos.z:
            m1.vel.z += 1
            m2.vel.z -= 1
        elif m1.pos.z > m2.pos.z:
            m1.vel.z -= 1
            m2.vel.z += 1

    for m in moons:
        m.pos += m.vel


def run(input_file):
    with timing("Day 12: The N-Body Problem"):
        part1 = solve_part1(
            [
                Moon(Vector(x=-16, y=-1, z=-12), Vector(0, 0, 0)),
                Moon(Vector(x=0, y=-4, z=-17), Vector(0, 0, 0)),
                Moon(Vector(x=-11, y=11, z=0), Vector(0, 0, 0)),
                Moon(Vector(x=2, y=2, z=-6), Vector(0, 0, 0)),
            ]
        )

        part2 = solve_part2(
            [
                Moon(Vector(x=-16, y=-1, z=-12), Vector(0, 0, 0)),
                Moon(Vector(x=0, y=-4, z=-17), Vector(0, 0, 0)),
                Moon(Vector(x=-11, y=11, z=0), Vector(0, 0, 0)),
                Moon(Vector(x=2, y=2, z=-6), Vector(0, 0, 0)),
            ]
        )

    print(part1)
    print(part2)


def solve_part1(moons, ticks=1000):
    for t in range(0, ticks):
        tick(moons)
    return sum(m.potential() * m.kinetic() for m in moons)


def lcm(a, b):
    return (a * b) // gcd(a, b)


def lcm3(a, b, c):
    # https://stackoverflow.com/questions/42517365/lcm-and-gcd-3-number-python
    return a * lcm(b, c) // gcd(a, lcm(b, c))


def solve_part2(moons):
    start = copy.deepcopy(moons)
    count = 0
    x, y, z = ([], [], [])
    while not x or not y or not z:
        tick(moons)
        count += 1
        if not x and all(
            m.pos.x == start[i].pos.x and m.vel.x == 0 for i, m in enumerate(moons)
        ):
            x.append(count)

        if not y and all(
            m.pos.y == start[i].pos.y and m.vel.y == 0 for i, m in enumerate(moons)
        ):
            y.append(count)

        if not z and all(
            m.pos.z == start[i].pos.z and m.vel.z == 0 for i, m in enumerate(moons)
        ):
            z.append(count)

    return lcm3(x[0], y[0], z[0])


def test_part1():
    io = Moon(Vector(x=-16, y=-1, z=-12), Vector(0, 0, 0))
    europa = Moon(Vector(x=0, y=-4, z=-17), Vector(0, 0, 0))
    ganymede = Moon(Vector(x=-11, y=11, z=0), Vector(0, 0, 0))
    callisto = Moon(Vector(x=2, y=2, z=-6), Vector(0, 0, 0))

    moons = [io, europa, ganymede, callisto]

    assert solve_part1(moons) == 5517


def test_part2():
    part2 = solve_part2(
        [
            Moon(Vector(x=-16, y=-1, z=-12), Vector(0, 0, 0)),
            Moon(Vector(x=0, y=-4, z=-17), Vector(0, 0, 0)),
            Moon(Vector(x=-11, y=11, z=0), Vector(0, 0, 0)),
            Moon(Vector(x=2, y=2, z=-6), Vector(0, 0, 0)),
        ]
    )

    assert part2 == 303070460651184


def test_part2_example():
    io = Moon(Vector(-1, 0, 2), Vector(0, 0, 0))
    europa = Moon(Vector(2, -10, -7), Vector(0, 0, 0))
    ganymede = Moon(Vector(4, -8, 8), Vector(0, 0, 0))
    callisto = Moon(Vector(3, 5, -1), Vector(0, 0, 0))

    moons = [io, europa, ganymede, callisto]

    assert solve_part2(moons) == 2772
