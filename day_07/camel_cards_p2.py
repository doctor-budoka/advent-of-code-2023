from argparse import ArgumentParser
from pathlib import Path
from collections import Counter

from utils.io_utils import read_file

parser = ArgumentParser(prog="camel-cards-2")

parser.add_argument("input_name")

type_ranks = {
    "high-card": 1,
    "pair": 2,
    "two-pair": 3,
    "three-of-a-kind": 4,
    "full-house": 5,
    "four-of-a-kind": 6,
    "five-of-a-kind": 7,
}

class CamelHand:
    def __init__(self, hand: str):
        self.hand = hand
        self.counts = Counter(hand)
        self._type = None
        self._value_tuple = None

    @property
    def type(self):
        if self._type is None:
            self._type = _get_type_from_counts(self.counts)
        return self._type
    
    @property
    def value_tuple(self):
        if self._value_tuple is None:
            self._value_tuple = _get_value_tuple(self.type, self.hand)
        return self._value_tuple

    def __str__(self):
        return f"{self.__class__.__name__}({self.hand})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.hand})"
    
    def __eq__(self, other):
        return self.value_tuple == other.value_tuple
    
    def __lt__(self, other):
        return self.value_tuple < other.value_tuple
    
    def __gt__(self, other):
        return self.value_tuple > other.value_tuple


def _get_type_from_counts(counter):
    ordered_counts = sorted([val for key, val in counter.items() if key != "J"], reverse=True) + [0, 0]
    joker_count = counter.get("J", 0)
    high_count = ordered_counts[0]
    second_high_count = ordered_counts[1]
    match high_count + joker_count, second_high_count:
        case (1, _):
            return "high-card"
        case (2, 2):
            return "two-pair"
        case (2, _):
            return "pair"
        case (3, 2):
            return "full-house"
        case (3, _):
            return "three-of-a-kind"
        case (4, _):
            return "four-of-a-kind"
        case (5, _):
            return "five-of-a-kind"
        case _:
            raise ValueError(f"Something is wrong here. Counts: {counter}")
        
def _get_value_tuple(hand_type, hand):
    type_rank = type_ranks[hand_type]
    card_ints = [_card_as_int(card) for card in hand]
    return (type_rank, *card_ints)


def _card_as_int(card):
    try:
        return int(card)
    except ValueError:
        match card:
            case "T":
                return 10
            case "J":
                return 1
            case "Q":
                return 12
            case "K":
                return 13
            case "A":
                return 14
            case _:
                raise ValueError(f"Shouldn't be here. Card: {card}")


def camel_cards_1(input_name):
    path = Path(__file__).parent / input_name
    input_str = read_file(path)

    hands = parse_input(input_str)
    winnings = sum(map(
        lambda x: x[1][1] * (x[0] + 1), 
        enumerate(sorted(hands, key=lambda x: x[0])),
    ))
    return winnings


def parse_input(input_str):
    hands = input_str.strip().split("\n")
    return list(map(_get_hand_couple, hands))


def _get_hand_couple(couple_str):
    hand_str, wager_str = couple_str.strip().split()
    return (CamelHand(hand_str), int(wager_str))


if __name__ == "__main__":
    args = parser.parse_args()
    answer = camel_cards_1(args.input_name)
    print(answer)
