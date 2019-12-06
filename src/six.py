from src.tools import process


def find_path(start, end, graph):
    path = []
    while start != end:
        start = graph[start]
        path.append(start)
    return path


def run(input_file):
    graph = {"COM": None}
    for line in process(input_file):
        parent, orbiter = line.split(")")
        graph[orbiter] = parent

    solve_part1(graph)
    solve_part2(graph)


def solve_part1(graph):
    total = 0
    for so in graph:
        total += len(find_path(so, "COM", graph))
    print(total)


def solve_part2(graph):
    you = set(find_path("YOU", "COM", graph))
    san = set(find_path("SAN", "COM", graph))
    # if we remove common nodes we should have number of jumps between us
    print(len(you) + len(san) - 2 * len(you.intersection(san)))
