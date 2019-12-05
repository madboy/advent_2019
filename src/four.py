from src.tools import process


def criteria(number):
    n = list(str(number))
    if len(n) == len(set(n)):
        return False
    if n == sorted(n):
        return True
    return False


def count(l, x):
    return l.count(x)


def criteria2(number):
    # assumes we have checked critera first
    n = list(str(number))
    match2 = (count(n, x) == 2 for x in n)
    return any(match2)


def run(input_file):
    part1_count = 0
    part2_count = 0
    for line in process(input_file):
        low, high = [int(n) for n in line.split("-")]
        for number in range(low, high):
            if criteria(number):
                part1_count += 1
                # second criteria is subset of first
                if criteria2(number):
                    part2_count += 1

    print(part1_count, part2_count)
