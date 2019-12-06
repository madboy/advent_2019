from src.tools import process


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
        while so != None:
            so = graph[so]
            # we only want to count real nodes
            # and not the end node None
            total += 1 if so else 0
    print(total)


def solve_part2(graph):
    paths = []
    for so in ["YOU", "SAN"]:
        path = set()
        while so != None:
            so = graph[so]
            path.add(so)
        paths.append(path)
    you = paths[0]
    san = paths[1]
    print(len(you) + len(san) - 2 * len(you.intersection(san)))
