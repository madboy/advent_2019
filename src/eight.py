from collections import Counter
from tools.tools import process, timing


def run(input_file):
    with timing("Day 8: Space Image Format"):
        for line in process(input_file):
            print(solve_part1(line, 25, 6))
            image = solve_part2(line, 25, 6)
            _print_image(image, 25, 6)


def solve_part1(line, width, height):
    layers = []
    for l in range(len(line) // (width * height)):
        layer = Counter(line[l * (width * height) : (l + 1) * (width * height)])
        layers.append(layer)

    layer_of_choice = None
    nbr_of_zeros = 10000
    for layer in layers:
        if layer.get("0", 100000) < nbr_of_zeros:
            nbr_of_zeros = layer.get("0")
            layer_of_choice = layer

    return layer_of_choice.get("1") * layer_of_choice.get("2")


def _print_image(image, width, height):
    for y in range(height):
        line = ""
        for x in range(width):
            line += "." if image[x + y * width] == "0" else "X"
        print(line)


def solve_part2(line, width, height):
    image = ""
    size = width * height
    layers = len(line) // (size)
    for px in range(size):
        for l in range(layers):
            value = line[px + l * (size)]
            if value == "0" or value == "1":
                image += value
                break
    return image


def test_part1():
    for line in process("input/8"):
        response = solve_part1(line, 25, 6)

    assert response == 1088


def test_part2():
    for line in process("input/8"):
        response = solve_part2(line, 25, 6)
    assert (
        response
        == "100000110010001100101110010000100101000110010100101000010000010101111011100100001011000100100101001010000100100010010010100101111001110001001001011100"
    )


def test_part1_example():
    line = "123456789012"
    response = solve_part1(line, 3, 2)
    assert response == 1


def test_part2_example():
    line = "0222112222120000"
    response = solve_part2(line, 2, 2)

    assert response == "0110"

