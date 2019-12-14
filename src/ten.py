from collections import defaultdict
from fractions import Fraction
import pytest
from tools.tools import process, timing


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        if self.y == other.y:
            if self.x == other.x:
                return 0
            return self.x < other.x
        # this is specific to how we want to consume asteroids
        return self.y > other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Quadrant:
    def __init__(self, u=False, r=False, x=False):
        self.u = u
        self.r = r
        self.x = x

    def __str__(self):
        return f"u: {self.u} r: {self.r}, x: {self.x}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.u == other.u and self.r == other.r and self.x == other.x

    def __hash__(self):
        return hash((self.u, self.r, self.x))


class AFraction:
    def __init__(self, f, q):
        self.f = f
        self.q = q

    def __str__(self):
        return f"({self.f}, q: ({self.q}))"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def __gt__(self, other):
        return self.f > other.f

    def __eq__(self, other):
        return self.f == other.f and self.q == other.q

    def __hash__(self):
        return hash((self.f, self.q))


def gradient(a1, a2):
    try:
        g = str(Fraction((a1.y - a2.y), (a1.x - a2.x)))
    except ZeroDivisionError:
        g = "0" if a2.x > a1.x else "-0"
    g = f"{g}u" if a2.y < a1.y else f"{g}"
    g = f"{g}r" if a2.x > a1.x else f"{g}"
    return g


def gradient2(a1, a2):
    # This is much slower to use for part 1 so we have two versions
    try:
        g = Fraction((a1.y - a2.y), (a1.x - a2.x))
    except ZeroDivisionError:
        g = Fraction(0)
    return AFraction(g, Quadrant(u=a2.y < a1.y, r=a2.x > a1.x, x=a1.x == a2.x))


def get_visible(asteroid, asteroids):
    visible = set()
    for a in asteroids:
        g = gradient(asteroid, a)
        visible.add(g)
    return visible


def get_asteroids(input_file):
    asteroids = set()
    y = 0
    for line in process(input_file):
        for x, c in enumerate(line):
            if c == "#":
                asteroids.add(Point(x, y))
        y += 1
    return asteroids


def run(input_file):
    with timing("Day 10: Monitoring Station"):
        asteroids = get_asteroids(input_file)
        msl, part1 = solve_part1(asteroids)
        part2 = solve_part2(msl, asteroids)
    print(part1)
    print(part2)


def solve_part1(asteroids):
    max_count = 0
    msl = None
    for asteroid in asteroids:
        visible = get_visible(asteroid, asteroids - {asteroid})
        if len(visible) > max_count:
            max_count = len(visible)
            msl = asteroid
    return msl, max_count


def solve_part2(msl, asteroids):
    asteroids.remove(msl)
    asteroids = list(asteroids)

    gradients = set()
    directions = defaultdict(list)
    for asteroid in asteroids:
        af = gradient2(msl, asteroid)
        gradients.add(af)
        directions[af].append(asteroid)
        directions[af] = sorted(directions[af], reverse=True)

    # The zero gradients are not aligned with quadrants so adding
    # a separate list to iterate over
    zeros = [
        Quadrant(u=True, r=False, x=True),
        Quadrant(u=False, r=True, x=False),
        Quadrant(u=False, r=False, x=True),
        Quadrant(u=False, r=False, x=False),
    ]
    quadrants = [
        Quadrant(u=True, r=True, x=False),
        Quadrant(u=False, r=True, x=False),
        Quadrant(u=False, r=False, x=False),
        Quadrant(u=True, r=False, x=False),
    ]
    q = 0  # index for quadrants and zeros is the same
    p = None  # start with no previous asteroid so that we start by looking straight up
    i = 0
    gradients = sorted(gradients)
    zero = zeros[q]
    quadrant = quadrants[q]
    count = 0
    while len(directions.values()) > 0:
        grad = gradients[i]
        # we deal with zero gradients from the zeros list instead of destroying
        # based on the gradient, so here we just skip them
        if grad.f == 0:
            i += 1
            continue
        # if we are in the same quadrant we should have no sign change between previous and current
        if p and p.f // abs(p.f) == grad.f // abs(grad.f):
            if grad.q == quadrant and directions.get(grad):
                count += 1
                asteroid = directions[grad].pop()
                if count == 200:
                    return asteroid.x * 100 + asteroid.y
                if not directions.get(grad):
                    del directions[grad]
            i += 1
            i %= len(gradients)
        # when we change sign we should look for the next zero gradient
        else:
            zero = zeros[q]
            quadrant = quadrants[q]
            if directions.get(AFraction(0, zero)):
                count += 1
                asteroid = directions[AFraction(0, zero)].pop()
                if count == 200:
                    return asteroid.x * 100 + asteroid.y
                if not directions[AFraction(0, zero)]:
                    del directions[AFraction(0, zero)]
            q += 1
            q %= len(zeros)
        p = grad

    return directions


def test_part1():
    asteroids = get_asteroids("input/10")
    assert solve_part1(asteroids) == (Point(11, 11), 221)


def test_part2():
    asteroids = get_asteroids("input/10")
    assert solve_part2(Point(11, 11), asteroids) == 806


def test_point_sorting():
    points = [Point(14, 3), Point(13, 3), Point(12, 3)]

    assert points == sorted(points, reverse=True)

    points = [Point(8, 0), Point(8, 1)]
    assert points == sorted(points, reverse=True)
