from tools.tools import process, timing


def run(input_file):
    with timing("template"):
        for line in process(input_file):
            solve_part1(line)
            solve_part2(line)


def solve_part1(line):
    return "None"


def solve_part2(line):
    return "None"


def test_part1_example():
    line = ""
    response = solve_part1(line)
    assert response == "None"


def test_part2_example():
    line = ""
    response = solve_part2(line)
    assert response == "None"
