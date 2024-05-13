from argparse import ArgumentParser
from math import prod
from pathlib import Path



from utils.io_utils import read_file_by_line

parser = ArgumentParser(prog="cube-conundrum-1")

parser.add_argument("input_name")

def cube_conundrum_2(input_name):
    path = Path(__file__).parent / input_name
    input_lines = read_file_by_line(path)

    possible_ids = [
        calculate_game_power(line)
        for line in input_lines
    ]
    return sum(possible_ids)


def calculate_game_power(line_str):
    gid, results = parse_game(line_str)
    all_keys = set().union(*[result.keys() for result in results])

    max_values = {
        key: max([result.get(key, 0) for result in results])
        for key in all_keys
    }
    return prod(max_values.values())

def parse_game(line):
    game_str, results_str = line.split(": ")
    gid = int(game_str[5:])
    rounds = [
        parse_round_result(result_str)
        for result_str in results_str.split("; ")
    ]
    return gid, rounds
 

def parse_round_result(result_str):
    return {
        colour_result.split(" ")[1][0]: int(colour_result.split(" ")[0]) 
        for colour_result in result_str.split(", ")
    }


if __name__ == "__main__":
    args = parser.parse_args()
    answer = cube_conundrum_2(args.input_name)
    print(answer)
