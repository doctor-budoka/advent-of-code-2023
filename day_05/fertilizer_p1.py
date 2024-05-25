from argparse import ArgumentParser
from pathlib import Path
from dataclasses import dataclass
from collections import namedtuple
from typing import List
from operator import itemgetter

from utils.io_utils import read_file

parser = ArgumentParser(prog="fertilizer-1")

parser.add_argument("input_name")


RangeTuple = namedtuple("RangeTuple", ["dest_start", "src_start", "range_len"])
PathNode = namedtuple("PathNode", ["type", "num"])


@dataclass(frozen=True)
class RangeMapping:
    from_str: str
    to_str: str
    ranges: List[RangeTuple]

    def __call__(self, val: int):
        for range_tuple in self.ranges:
            if 0 <= val - range_tuple.src_start <= range_tuple.range_len:
                return val + range_tuple.dest_start - range_tuple.src_start
        return val


def fertilizer_1(input_name):
    path = Path(__file__).parent / input_name
    input_str = read_file(path)

    seeds, maps = parse_input(input_str)
    map_froms = [map_.from_str for map_ in maps]
    if len(map_froms) != len(set(map_froms)):
        raise ValueError("There are non-unique from strings!")
    map_dict = {map_.from_str: map_ for map_ in maps}
    
    paths, start_end = find_paths(seeds, map_dict)
    locations = list(map(itemgetter(1), start_end.values()))
    print(seeds)
    print(locations)
    return min(locations)


def parse_input(input_str):
    sections = input_str.split("\n\n")
    seed_section, map_sections = sections[0], sections[1:]
    seeds = list(map(int, seed_section.replace("seeds: ", "").strip().split()))
    return seeds, list(map(parse_section, map_sections))


def parse_section(section):
    section_lines = section.split("\n")
    title, map_lines = section_lines[0], section_lines[1:]
    from_str, to_str = title.replace(" map:", "").split("-to-")
    return RangeMapping(
        from_str=from_str, 
        to_str=to_str, 
        ranges = [
            RangeTuple(*map(int, map_line.split()))
            for map_line in map_lines
        ]
    )


def find_paths(seeds, map_dict):
    paths = {}
    start_end = {}
    end_type = "location"
    for seed in seeds:
        start_node = PathNode("seed", seed)
        current_node = start_node
        while current_node.type != end_type:
            edge_map = map_dict[current_node.type]
            next_node = PathNode(edge_map.to_str, edge_map(current_node.num))
            paths[current_node] = next_node
            current_node = next_node
        start_end[start_node] = next_node
    return paths, start_end


def show_path(start, paths):
    node = start
    print(start)
    while node in paths:
        node = paths[node]
        print(node)


if __name__ == "__main__":
    args = parser.parse_args()
    answer = fertilizer_1(args.input_name)
    print(answer)
