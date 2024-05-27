from argparse import ArgumentParser
from pathlib import Path
from dataclasses import dataclass
from collections import namedtuple
from typing import List, Iterable
from operator import itemgetter
from itertools import chain

from utils.io_utils import read_file

parser = ArgumentParser(prog="fertilizer-2")

parser.add_argument("input_name")


RangeTuple = namedtuple("RangeTuple", ["dest_start", "src_start", "range_len"])
PathNode = namedtuple("PathNode", ["type", "num"])


@dataclass(frozen=True)
class ItemRange:
    start_range: int
    end_range: int

    @property
    def is_null(self):
        return self.start_range > self.end_range

    @property
    def not_null(self):
        return not self.is_null
    
    def intersection(self, start, end):
        new_start = max(self.start_range, start)
        new_end = min(self.end_range, end)
        if new_start > new_end:
            return ItemRange(-1, -2)
        return ItemRange(new_start, new_end)
    
    def diff(self, start, end):
        diff = set()
        if self.start_range < start:
            diff.add(ItemRange(self.start_range, min(self.end_range, start -1)))
        if self.end_range > end:
            diff.add(ItemRange(max(end + 1, self.end_range), self.end_range))
        return diff
    
    def __add__(self, val: int):
        if not isinstance(val, int):
            raise ValueError(f"Can't add range and {type(val)}")
        return ItemRange(self.start_range + val, self.end_range + val)

@dataclass(frozen=True)
class RangeMapping:
    from_str: str
    to_str: str
    ranges: List[RangeTuple]

    def apply_to_ranges(self, ranges: Iterable[ItemRange]) -> Iterable[ItemRange]:
        output = set()
        for item_range in ranges:
            this_result = self.apply_to_range(item_range)
            output.update(this_result)
        return output


    def apply_to_range(self, val: ItemRange) -> Iterable[ItemRange]:
        output = set()
        remaining = {val}
        for range_tuple in self.ranges:
            end = range_tuple.src_start + range_tuple.range_len - 1
            new_remaining = set()
            for thing in remaining:
                intersection = thing.intersection(range_tuple.src_start, end)
                diff = thing.diff(range_tuple.src_start, end)
                if intersection.not_null:
                    offset = range_tuple.dest_start - range_tuple.src_start
                    output.add(intersection + offset)
                if diff:
                    new_remaining.update(diff)
            remaining = new_remaining
        if remaining:
            output.update(remaining)

        return output


def fertilizer_2(input_name):
    path = Path(__file__).parent / input_name
    input_str = read_file(path)

    seed_ranges, maps = parse_input(input_str)
    map_froms = [map_.from_str for map_ in maps]
    if len(map_froms) != len(set(map_froms)):
        raise ValueError("There are non-unique from strings!")
    map_dict = {map_.from_str: map_ for map_ in maps}

    current_type = "seed"
    current_item_ranges = seed_ranges
    while current_type != "location":
        print(current_type)
        print(len(current_item_ranges))
        print(current_item_ranges)
        edge_map = map_dict[current_type]
        new_item_range = edge_map.apply_to_ranges(current_item_ranges)
        current_item_ranges = new_item_range
        current_type = edge_map.to_str
        print(current_item_ranges)
        print(len(current_item_ranges))
        print(current_type)

    min_loc = min([item_range.start_range for item_range in current_item_ranges])    

    return min_loc


def parse_input(input_str):
    sections = input_str.split("\n\n")
    seed_section, map_sections = sections[0], sections[1:]
    seeds = parse_seed_section(seed_section)
    return seeds, list(map(parse_section, map_sections))


def parse_seed_section(seed_section):
    numbers = list(map(int, seed_section.replace("seeds: ", "").strip().split()))
    starts = numbers[::2]
    lengths = numbers[1::2]
    return {ItemRange(start, start + length - 1) for start, length in zip(starts, lengths)}


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


def find_end_for_seed(start_node, map_dict):
    end_type = "location"
    current_node = start_node
    while current_node.type != end_type:
        edge_map = map_dict[current_node.type]
        next_node = PathNode(edge_map.to_str, edge_map(current_node.num))
        current_node = next_node
    return next_node


if __name__ == "__main__":
    args = parser.parse_args()
    answer = fertilizer_2(args.input_name)
    print(answer)
