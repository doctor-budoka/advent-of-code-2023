from argparse import ArgumentParser
from pathlib import Path
import re

from utils.io_utils import read_file_by_line

parser = ArgumentParser(prog="trebuchet-1")

parser.add_argument("input_name")

DIGITS = {
    "one": "1", 
    "two": "2", 
    "three": "3", 
    "four": "4", 
    "five": "5", 
    "six": "6", 
    "seven": "7", 
    "eight": "8", 
    "nine": "9",
}

def trebuchet_1(input_name):
    path = Path(__file__).parent / input_name
    input_lines = read_file_by_line(path)

    answers = [
        int(get_first_and_last_digit(line))
        for line in input_lines
        if line
    ]
    return sum(answers)


def get_first_and_last_digit(line_str):
    forward_pattern_str = r"([1-9])|" + "|".join(
        ["(" + digit_name + ")" for digit_name in DIGITS.keys()]
    )
    first_digit_match = return_digit_char_for_pattern(forward_pattern_str, line_str)
    first_digit = convert_digit_to_char(first_digit_match)

    backward_pattern_str = r"([1-9])|" + "|".join(
        ["(" + digit_name[::-1] + ")" for digit_name in DIGITS.keys()]
    )
    last_digit_match = return_digit_char_for_pattern(backward_pattern_str, line_str[::-1])
    last_digit = convert_digit_to_char(last_digit_match[::-1])
    return first_digit + last_digit


def return_digit_char_for_pattern(pattern_str, line):
    pattern_re = re.compile(pattern_str)
    digit_str = pattern_re.search(line).group(0)
    return digit_str
    

def convert_digit_to_char(digit_str):
    if digit_str.isdigit():
        return digit_str
    else:
        return DIGITS[digit_str]


if __name__ == "__main__":
    args = parser.parse_args()
    answer = trebuchet_1(args.input_name)
    print(answer)