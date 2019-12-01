from src.tools import process


def fuel_requirement_part1(mass):
    return (mass // 3) - 2


def fuel_requirement_part2(mass):
    if (fr := fuel_requirement_part1(mass)) <= 0:
        return 0
    return fr + fuel_requirement_part2(fr)


def run(input_file):
    fuel_needed1 = 0
    fuel_needed2 = 0
    for mass in process(input_file):
        fuel_needed1 += fuel_requirement_part1(int(mass))
        fuel_needed2 += fuel_requirement_part2(int(mass))
    print(fuel_needed1, fuel_needed2)

