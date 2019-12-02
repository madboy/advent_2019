#!/usr/bin/env python
import argparse
from dataclasses import dataclass
from src import one, two
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
