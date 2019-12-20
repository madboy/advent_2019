from collections import Counter, deque
from dataclasses import dataclass
import math
from tools.tools import process, timing


@dataclass
class C:
    n: str
    a: int


@dataclass
class P:
    i: list
    a: int


@dataclass
class Produced:
    name: str
    got: int
    want: int


def set_reaction(line, d):
    f, t = line.split(" => ")
    tc, tn = t.split()
    ingredients = []
    for c in f.split(", "):
        cc, cn = c.split()
        ingredients.append(C(cn, int(cc)))
    d[tn] = P(ingredients, int(tc))


def get_reactions(input_file):
    reactions = {}
    for line in process(input_file):
        set_reaction(line, reactions)
    return reactions


def run(input_file):
    with timing("Day 14: Space Stoichiometry"):
        part1 = solve_part1(get_reactions(input_file))
        part2 = solve_part2(get_reactions(input_file))
    print(part1)
    print(part2)


def solve_part1(reactions):
    return _produce(C("FUEL", 1), reactions)


def solve_part2(reactions):

    count = 2509100
    while _produce(C("FUEL", count), reactions) < 1000000000000:
        count += 1
    return count - 1


def _produce(start, reactions):
    to_produce = deque()
    production = Counter()
    to_produce.append(start)

    while to_produce:
        target = to_produce.popleft()
        amount = target.a
        if not production[target.n]:
            production[target.n] = Produced(target.n, 0, amount)
        else:
            production[target.n].want += amount
            amount = production[target.n].want - production[target.n].got
            if amount < 0:
                continue

        p = reactions.get(target.n)
        if p:
            for c in p.i:
                to_produce.append(C(c.n, math.ceil(amount / p.a) * c.a))
            production[target.n].got += p.a * math.ceil(amount / p.a)

    total = 0
    for k, v in production.items():
        try:
            if "ORE" in reactions[k].i[0].n:
                total += math.ceil(v.want / reactions[k].a) * reactions[k].i[0].a
        except (IndexError, KeyError):
            pass
    return total


def test_part1():
    reactions = get_reactions("input/14")
    assert solve_part1(reactions) == 612880


def test_part2():
    reactions = get_reactions("input/14")
    assert solve_part2(reactions) == 2509120


def test_part1_example():
    in_data = [
        "171 ORE => 8 CNZTR",
        "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
        "114 ORE => 4 BHXH",
        "14 VRPVC => 6 BMBT",
        "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
        "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
        "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
        "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
        "5 BMBT => 4 WPTQ",
        "189 ORE => 9 KTJDG",
        "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
        "12 VRPVC, 27 CNZTR => 2 XDBXC",
        "15 KTJDG, 12 BHXH => 5 XCVML",
        "3 BHXH, 2 VRPVC => 7 MZWV",
        "121 ORE => 7 VRPVC",
        "7 XCVML => 6 RJRHP",
        "5 BHXH, 4 VRPVC => 5 LTCX",
    ]
    reactions = {}
    for line in in_data:
        set_reaction(line, reactions)

    assert solve_part1(reactions) == 2210736
