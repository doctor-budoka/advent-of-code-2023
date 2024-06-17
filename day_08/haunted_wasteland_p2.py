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
        for ind, item in enumerate(to_loop):
            yield ind, item



def haunted_wasteland_2(input_name):
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

    summarised_journeys = {
        start_node: summarise_journey(directions, graph, start_node)
        for start_node in start_nodes
    }
    
    return analyse_journeys(summarised_journeys)


def get_start_nodes(graph):
    return [
        name for name, node in graph.items()
        if node.ends_with == "A"
    ]


def summarise_journey(directions, graph, start_node):
    loop_start = find_loop_start(directions, graph, start_node)

    lead_in_length = 0
    lead_in_path = {}
    loop_length = 0
    loop_path = {}

    current_node_name = start_node
    current_node = graph[start_node]
    current_visit = (current_node_name, 0)
    in_loop = False
    for step, direction in looped_generator(directions):
        if not in_loop and current_visit == loop_start:
            in_loop = True
        
        lead_in_length += int(not in_loop)
        loop_length += int(in_loop)
        current_path_dict = loop_path if in_loop else lead_in_path

        next_node_name = current_node.go(direction)
        next_visit = (next_node_name, step + 1)
        
        current_path_dict[current_visit] = next_visit
        current_visit = next_visit
        current_node = graph[next_node_name]

        if in_loop and current_visit == loop_start:
            break

    lead_in_details = {"start": (start_node, 0), "length": lead_in_length, "path": lead_in_path}
    loop_details = {"start": loop_start, "length": loop_length, "path": loop_path}
    overall_details = {
        "lead_in": lead_in_details,
        "loop": loop_details,
    }
    return overall_details


def find_loop_start(directions, graph, start_node):
    steps = 0
    current_node = start_node
    visited = set()
    for step, direction in looped_generator(directions):
        this_visit = (current_node, step)
        if this_visit in visited:
            break
        visited.add(this_visit)
        current_node = graph[current_node].go(direction)
        steps += 1

    loop_start = this_visit or None
    if loop_start is None:
        raise ValueError("loop_start is None")
    return loop_start


def analyse_journeys(summarised_journeys):
    print(summarised_journeys)
    return 0


if __name__ == "__main__":
    args = parser.parse_args()
    answer = haunted_wasteland_2(args.input_name)
    print(answer)
