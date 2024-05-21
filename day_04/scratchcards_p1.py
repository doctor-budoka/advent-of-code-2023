from argparse import ArgumentParser
from pathlib import Path

from utils.io_utils import read_file_by_line

parser = ArgumentParser(prog="scratchcards-1")

parser.add_argument("input_name")

def scratchcards_1(input_name):
    path = Path(__file__).parent / input_name
    input_lines = read_file_by_line(path)

    cards = parse_input(input_lines)
    
    card_points = [get_points_for_card(card) for card in cards]
    return sum(card_points)


def parse_input(lines):
    return [
        parse_card(line)
        for line in lines
    ]


def parse_card(line):
    card_part, rest = line.split(": ")
    card_id = int(card_part.replace("Card ", ""))
    wants_str, haves_str = rest.split(" | ")
    wants, haves = _str_to_int_list(wants_str), _str_to_int_list(haves_str)
    return card_id, wants, haves


def _str_to_int_list(int_str):
    return [int(x) for x in int_str.split()]


def get_points_for_card(card):
    _, wants, haves = card
    wants_set = set(wants)
    matches = [num for num in haves if num in wants_set]
    num_matches = len(matches)
    return 2 ** (num_matches - 1) if num_matches else 0



if __name__ == "__main__":
    args = parser.parse_args()
    answer = scratchcards_1(args.input_name)
    print(answer)
