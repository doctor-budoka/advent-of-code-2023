from argparse import ArgumentParser
from pathlib import Path
from itertools import product
from dataclasses import dataclass

from utils.io_utils import read_file

parser = ArgumentParser(prog="gear-ratio-1")


parser.add_argument("input_name")

@dataclass(frozen=True)
class Point:
    row: int
    col: int

    def __add__(self, other):
        return Point(self.row + other.row, self.col + other.col)
    
    def neighbours(self):
        return {
            self + Point(row_add, col_add)
            for row_add, col_add in product([1, 0, -1], [1, 0, -1])
        }


def gear_ratio_1(input_name):
    path = Path(__file__).parent / input_name
    input_str = read_file(path)

    numbers, symbol_positions = parse_input(input_str)
    part_numbers = extract_part_numbers(numbers, symbol_positions)

    return sum(part_numbers)


def parse_input(input_str):
    symbol_positions = set()
    numbers = []
    if input_str[-1]:
        input_str += "\n"

    row = 0
    col = 0
    current_number = ""
    current_positions = set()
    for char in input_str:
        if char.isspace():
            row += 1
            col = 0
            if current_number:
                numbers.append((int(current_number), current_positions))
                current_number = ""
                current_positions = set()
            continue
        elif char == "." and current_number:
            numbers.append((int(current_number), current_positions))
            current_number = ""
            current_positions = set()
        elif char == ".":
            pass
        elif char.isdigit():
            current_positions.add(Point(row, col))
            current_number += char
        else:
            if current_number:
                numbers.append((int(current_number), current_positions))
                current_number = ""
                current_positions = set()
            symbol_positions.add(Point(row, col))
        col += 1

    return numbers, symbol_positions


def extract_part_numbers(numbers, symbol_positions):
    part_numbers = []
    for number, positions in numbers:
        number_nbd = {
            nbd_pnt
            for pos in positions
            for nbd_pnt in pos.neighbours()
        }
        if number_nbd.intersection(symbol_positions):
            part_numbers.append(number)
    return part_numbers


if __name__ == "__main__":
    args = parser.parse_args()
    answer = gear_ratio_1(args.input_name)
    print(answer)
