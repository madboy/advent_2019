from collections import Counter, defaultdict
from fractions import Fraction
import pytest
from tools.tools import process, timing


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def gradient(a1, a2):
    try:
        g = str(Fraction((a1.y - a2.y), (a1.x - a2.x)))
    except ZeroDivisionError:
        g = "0" if a2.x > a1.x else "-0"
    g = f"{g}u" if a2.y > a1.y else f"{g}"
    g = f"{g}r" if a2.x > a1.x else f"{g}"
    return g


def get_visible(asteroid, asteroids):
    visible = set()
    for a in asteroids:
        g = gradient(asteroid, a)
        visible.add(g)

    return visible


def run(input_file):
    asteroids = set()
    y = 0

    with timing("Day 10: Monitoring Station"):
        for line in process(input_file):
            for x, c in enumerate(line):
                if c == "#":
                    asteroids.add(Point(x, y))
            y += 1
        print(solve_part1(asteroids))


def solve_part1(asteroids):
    count = Counter()
    for asteroid in asteroids:
        visible = get_visible(asteroid, asteroids - {asteroid})
        count[asteroid] = len(visible)
    return count


@pytest.mark.parametrize(
    "p0,p1,grad",
    [
        (Point(1, 1), Point(2, 2), "1ur"),
        (Point(1, 1), Point(0, 2), "-1u"),
        (Point(1, 1), Point(0, 0), "1"),
        (Point(1, 1), Point(2, 0), "-1r"),
        (Point(1, 1), Point(1, 2), "-0u"),
        (Point(1, 1), Point(0, 1), "0"),
        (Point(1, 1), Point(1, 0), "-0"),
        (Point(1, 1), Point(2, 1), "0r"),
    ],
)
def test_simple(p0, p1, grad):
    assert gradient(p0, p1) == grad
