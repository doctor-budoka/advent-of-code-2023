from argparse import ArgumentParser
from pathlib import Path

from utils.io_utils import read_file_by_line

parser = ArgumentParser(prog="trebuchet-1")

parser.add_argument("input_name")

def trebuchet_1(input_name):
    path = Path(__file__).parent / input_name
    input_lines = read_file_by_line(path)

    answers = [
        int(get_first_and_last_digit(line))
        for line in input_lines
    ]
    return sum(answers)


def get_first_and_last_digit(line_str):
    digits = [char for char in line_str if char.isdigit()]
    return digits[0] + digits[-1]



if __name__ == "__main__":
    args = parser.parse_args()
    answer = trebuchet_1(args.input_name)
    print(answer)