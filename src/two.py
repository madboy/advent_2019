from src.tools import process


def run(input_file):
    for line in process(input_file):
        solve_part1([int(n) for n in line.split(",")])
        solve_part2([int(n) for n in line.split(",")])


def run_program(intcodes):
    i = 0
    while i < len(intcodes):
        if intcodes[i] == 99:
            break
        else:
            idx1 = intcodes[i + 1]
            idx2 = intcodes[i + 2]
            idx3 = intcodes[i + 3]
            if intcodes[i] == 1:
                intcodes[idx3] = intcodes[idx1] + intcodes[idx2]
            elif intcodes[i] == 2:
                intcodes[idx3] = intcodes[idx1] * intcodes[idx2]
            i += 4
    return intcodes[0]


def solve_part1(intcodes):
    intcodes[1] = 12
    intcodes[2] = 2

    print(run_program(intcodes))


def solve_part2(intcodes):
    for one in range(100):
        for two in range(100):
            intcodes_c = intcodes[:]  # resetting the memory banks
            intcodes_c[1] = one
            intcodes_c[2] = two
            if run_program(intcodes_c) == 19690720:
                print(f"{100*one+two}")
                return
