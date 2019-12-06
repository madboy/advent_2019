from tools.tools import process, timing


def fuel_requirement_part1(mass):
    return (mass // 3) - 2


def fuel_requirement_part2(mass):
    if (fr := fuel_requirement_part1(mass)) <= 0:
        return 0
    return fr + fuel_requirement_part2(fr)


def solve_part1_and_2(input_file):
    fuel_needed1 = 0
    fuel_needed2 = 0
    for mass in process(input_file):
        fuel_needed1 += fuel_requirement_part1(int(mass))
        fuel_needed2 += fuel_requirement_part2(int(mass))
    return (fuel_needed1, fuel_needed2)


def run(input_file):
    with timing("Day 1: The Tyranny of the Rocket Equation"):
        part1, part2 = solve_part1_and_2(input_file)
    print(part1)
    print(part2)


def test_part1_part2():
    assert solve_part1_and_2("input/1") == (3317970, 4974073)
