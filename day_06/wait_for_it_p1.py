from argparse import ArgumentParser
from pathlib import Path
from collections import namedtuple
from operator import mul
from functools import reduce
import math

from utils.io_utils import read_file

parser = ArgumentParser(prog="wait-for-it-1")

parser.add_argument("input_name")

Race = namedtuple("Race", "time,distance")
SolutionRange = namedtuple("SolutionTuple", "lower,upper")


def wait_for_it_1(input_name):
    path = Path(__file__).parent / input_name
    input_str = read_file(path)

    races = parse_input(input_str)
    solution_ranges = list(map(get_upper_and_lower_bounds, races))
    output = reduce(mul, map(lambda x: x.upper - x.lower + 1, solution_ranges))
    return output


def parse_input(input_str):
    times_str, distances_str = input_str.strip().split("\n")
    
    times = list(map(int, times_str.replace("Time: ", "").strip().split()))
    distances = list(map(int, distances_str.replace("Distance: ", "").strip().split()))

    return list(map(lambda x: Race(*x), zip(times, distances)))


def get_upper_and_lower_bounds(race):
    time, best = race
    discriminant = math.sqrt(time * time - 4 * best)
    lower_root = (time - discriminant)/2
    upper_root = (time + discriminant)/2

    lower_sol = (
        math.ceil(lower_root) if int(lower_root) != lower_root 
        else int(lower_root + 1)
    )
    upper_sol = (
        math.floor(upper_root) if int(upper_root) != upper_root 
        else int(upper_root - 1)
    )

    return SolutionRange(lower_sol, upper_sol)



if __name__ == "__main__":
    args = parser.parse_args()
    answer = wait_for_it_1(args.input_name)
    print(answer)
