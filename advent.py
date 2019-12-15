#!/usr/bin/env python
import argparse
from dataclasses import dataclass
from src import (
    one,
    two,
    three,
    four,
    five,
    six,
    seven,
    eight,
    nine,
    ten,
    eleven,
    twelve,
)
import sys
from typing import Callable


@dataclass
class Day:
    program: Callable
    input_file: str

    def __call__(self):
        self.program(self.input_file)


days = [
    (),
    Day(one.run, "input/1"),
    Day(two.run, "input/2"),
    Day(three.run, "input/3"),
    Day(four.run, "input/4"),
    Day(five.run, "input/5"),
    Day(six.run, "input/6"),
    Day(seven.run, "input/7"),
    Day(eight.run, "input/8"),
    Day(nine.run, "input/9"),
    Day(ten.run, "input/10"),
    Day(eleven.run, "input/11"),
    Day(twelve.run, "input/12"),
]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run an advent of code entry.")
    parser.add_argument(
        "day", metavar="day", type=int, help="the day of advent",
    )
    args = parser.parse_args()

    if args.day >= len(days) or args.day <= 0:
        print(f"I don't know that day yet. Try one between 1-{len(days)-1}.")
        sys.exit(1)

    days[args.day]()
