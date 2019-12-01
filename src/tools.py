def process(filename):
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()


def left_pad_process(filename):
    """
    In some cases we do not want to remove the white space on the 
    left side of the input
    """
    with open(filename, "r") as f:
        for line in f:
            yield line.rstrip()


def turn(current_direction, turn_direction):
    directions = {"left": 0, "up": 1, "right": 2, "down": 3}
    rdirections = {0: "left", 1: "up", 2: "right", 3: "down"}
    turns = {"left": -1, "right": 1, "straight": 0}
    new_direction = (directions[current_direction] + turns[turn_direction]) % 4
    return rdirections[new_direction]
