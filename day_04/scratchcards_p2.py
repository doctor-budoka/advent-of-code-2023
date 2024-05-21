from argparse import ArgumentParser
from pathlib import Path
from collections import Counter

from utils.io_utils import read_file_by_line

parser = ArgumentParser(prog="scratchcards-1")

parser.add_argument("input_name")

def scratchcards_2(input_name):
    path = Path(__file__).parent / input_name
    input_lines = read_file_by_line(path)

    cards = parse_input(input_lines)
    card_counts = play_game(cards)

    return card_counts.total()


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


def play_game(cards):
    max_card = len(cards)
    card_counts = Counter([i + 1 for i in range(max_card)])
    for card in cards:
        card_id, wants, haves = card
        num_copies = card_counts[card_id]
        num_matches = get_matches_for_card(card)
        card_counts.update({card_id + i + 1: num_copies for i in range(num_matches)})
    return card_counts


def get_matches_for_card(card):
    _, wants, haves = card
    wants_set = set(wants)
    matches = [num for num in haves if num in wants_set]
    return len(matches)


if __name__ == "__main__":
    args = parser.parse_args()
    answer = scratchcards_2(args.input_name)
    print(answer)
