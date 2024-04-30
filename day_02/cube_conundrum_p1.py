from argparse import ArgumentParser
from pathlib import Path

from utils.io_utils import read_file_by_line

parser = ArgumentParser(prog="cube-conundrum-1")

parser.add_argument("input_name")
parser.add_argument("--rule", "-r", default="r12,g13,b14")

def cube_conundrum_1(input_name, rule_str="r12,g13,b14"):
    rule = {
        colour_rule[0]: int(colour_rule[1:])
        for colour_rule in rule_str.split(",") 
    }

    path = Path(__file__).parent / input_name
    input_lines = read_file_by_line(path)

    possible_ids = [
        return_id_if_possible(line, rule)
        for line in input_lines
    ]
    return sum(possible_ids)


def return_id_if_possible(line_str, rule):
    gid, results = parse_game(line_str)
    all_keys = set().union(*[result.keys() for result in results])

    max_values = {
        key: max([result.get(key, 0) for result in results])
        for key in all_keys
    }
    ok = [
        1 - int(key in rule.keys() and max_values[key] <= rule[key])
        for key in all_keys
    ]
    return gid if sum(ok) == 0 else 0

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
    answer = cube_conundrum_1(args.input_name, rule_str=args.rule)
    print(answer)