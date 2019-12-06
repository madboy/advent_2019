from src.tools import process, timing


def find_path(start, end, graph):
    path = []
    while start != end:
        start = graph[start]
        path.append(start)
    return path


def create_graph(input_file):
    graph = {"COM": None}
    for line in process(input_file):
        parent, orbiter = line.split(")")
        graph[orbiter] = parent
    return graph


def run(input_file):
    with timing("Day 6: Universal Orbit Map"):
        graph = create_graph(input_file)
        part1 = solve_part1(graph)
        part2 = solve_part2(graph)
    print(part1)
    print(part2)


def solve_part1(graph):
    total = 0
    for so in graph:
        total += len(find_path(so, "COM", graph))
    return total


def solve_part2(graph):
    you = set(find_path("YOU", "COM", graph))
    san = set(find_path("SAN", "COM", graph))
    # if we remove common nodes we should have number of jumps between us
    return len(you) + len(san) - 2 * len(you.intersection(san))


def test_part1_example():
    graph = create_graph("input/6.test")
    assert solve_part1(graph) == 42


def test_part1():
    graph = create_graph("input/6")
    assert solve_part1(graph) == 270768


def test_part2_example():
    graph = create_graph("input/6.test.2")
    assert solve_part2(graph) == 4


def test_part2():
    graph = create_graph("input/6")
    assert solve_part2(graph) == 451
