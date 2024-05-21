from argparse import ArgumentParser
from pathlib import Path
from itertools import product
from dataclasses import dataclass

from utils.io_utils import read_file

parser = ArgumentParser(prog="gear-ratio-2")


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


def gear_ratio_2(input_name):
    path = Path(__file__).parent / input_name
    input_str = read_file(path)

    numbers, star_positions = parse_input(input_str)
    part_numbers = extract_gear_ratios(numbers, star_positions)

    return sum(part_numbers)


def parse_input(input_str):
    star_positions = set()
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
        elif char.isdigit():
            current_positions.add(Point(row, col))
            current_number += char
        elif char == "*":
            if current_number:
                numbers.append((int(current_number), current_positions))
                current_number = ""
                current_positions = set()
            star_positions.add(Point(row, col))
        elif current_number:
            numbers.append((int(current_number), current_positions))
            current_number = ""
            current_positions = set()
        col += 1

    return numbers, star_positions


def extract_gear_ratios(numbers, star_positions):
    star_numbers = {pos: [] for pos in star_positions}
    for number, positions in numbers:
        number_nbd = {
            nbd_pnt
            for pos in positions
            for nbd_pnt in pos.neighbours()
        }
        stars_for_num = number_nbd.intersection(star_positions)
        for star in stars_for_num:
            star_numbers[star].append(number)
    
    gear_ratios = [
        gear_nums[0] * gear_nums[1]
        for gear_nums in star_numbers.values()
        if len(gear_nums) == 2
    ]

    return gear_ratios


if __name__ == "__main__":
    args = parser.parse_args()
    answer = gear_ratio_2(args.input_name)
    print(answer)
