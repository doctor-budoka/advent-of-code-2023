from argparse import ArgumentParser
from pathlib import Path
from dataclasses import dataclass

from utils.io_utils import read_file

parser = ArgumentParser(prog="haunted-wasteland-1")

parser.add_argument("input_name")


@dataclass
class WastelandNode:
    name: str
    left: str
    right: str

    @property
    def ends_with(self):
        return self.name[-1]

    def go(self, direction: str):
        if direction == "L":
            return self.left
        elif direction == "R":
            return self.right
        else:
            raise ValueError(f"Direction must be 'L' or 'R' not '{direction}'")


def looped_generator(to_loop):
    while True:
        for item in to_loop:
            yield item



def haunted_wasteland_1(input_name):
    path = Path(__file__).parent / input_name
    input_str = read_file(path)

    directions, graph = parse_input(input_str)
    steps = follow_directions(directions, graph)

    return steps


def parse_input(input_str):
    instructions_str, graph_str = input_str.strip().split("\n\n")
    instructions = _parse_instructions(instructions_str)
    graph = _parse_graph(graph_str)
    return instructions, graph


def _parse_instructions(instructions_str):
    return list(instructions_str)


def _parse_graph(graph_str):
    neighbours_str_list = graph_str.split("\n")
    graph = dict(
        _parse_line_in_adjacency_graph(neighbours_str)
        for neighbours_str in neighbours_str_list
    )
    return graph


def _parse_line_in_adjacency_graph(neighbours_str):
    node_name_unclean, neighbours_tuple_str = neighbours_str.split(" = ")
    left_unclean, right_unclean = neighbours_tuple_str.split(", ")

    node_name = node_name_unclean.strip()
    node = WastelandNode(
        name=node_name, 
        left=left_unclean.strip()[1:], 
        right=right_unclean.strip()[:-1],
    )
    return node_name, node


def follow_directions(directions, graph):
    start_nodes = get_start_nodes(graph)

    steps = 0
    current_nodes = start_nodes.copy()
    for direction in looped_generator(directions):
        if all(graph[node].ends_with == "Z" for node in current_nodes):
            break
        steps += 1
        current_nodes = [graph[this_node].go(direction) for this_node in current_nodes]
    return steps


def get_start_nodes(graph):
    return [
        name for name, node in graph.items()
        if node.ends_with == "A"
    ]


if __name__ == "__main__":
    args = parser.parse_args()
    answer = haunted_wasteland_1(args.input_name)
    print(answer)
