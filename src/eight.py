from collections import Counter
from tools.tools import process, timing


class LayerCounter(Counter):
    # we only care about ordering layers on the number of zeros
    def __lt__(self, other):
        return self.get("0", 0) <= other.get("0", 0) and self != other


def run(input_file):
    width, height = 25, 6
    with timing("Day 8: Space Image Format"):
        line = next(process(input_file))
        part1 = solve_part1(line, width, height)
        part2 = solve_part2(line, width, height)
    print(part1)
    _print_image(part2, width, height)


def solve_part1(line, width, height):
    layers = []
    for l in range(len(line) // (width * height)):
        layers.append(
            LayerCounter(line[l * (width * height) : (l + 1) * (width * height)])
        )

    layers = sorted(layers)
    # as the layers are sorted on ascending number of zeros
    # we want the first layer
    layer_of_choice = layers[0]

    return layer_of_choice.get("1") * layer_of_choice.get("2")


def _print_image(image, width, height):
    for y in range(height):
        line = ""
        for x in range(width):
            line += "." if image[x + y * width] == "0" else "*"
        print(line)


def solve_part2(line, width, height):
    image = ""
    size = width * height
    layers = len(line) // size
    for px in range(size):
        for l in range(layers):
            if (value := line[px + l * size]) in ["0", "1"]:
                image += value
                break
    return image


def test_part1():
    line = next(process("input/8"))
    response = solve_part1(line, 25, 6)

    assert response == 1088


def test_part2():
    line = next(process("input/8"))
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
