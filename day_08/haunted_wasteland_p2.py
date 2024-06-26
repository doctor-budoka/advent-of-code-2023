from argparse import ArgumentParser
from pathlib import Path
from dataclasses import dataclass
import math

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
    loop_ind = 0
    lead_in_ind = 0
    loop_endpoints = {}
    lead_in_endpoints = {}

    current_node_name = start_node
    current_node = graph[start_node]
    current_visit = (current_node_name, 0)
    in_loop = False
    for step, direction in looped_generator(directions):
        if not in_loop and current_visit == loop_start:
            in_loop = True
        
        current_path_dict = loop_path if in_loop else lead_in_path
        current_ind_counter = loop_length if in_loop else lead_in_ind
        current_endpoint_tracker = loop_endpoints if in_loop else lead_in_endpoints

        if current_node.ends_with == "Z":
            current_endpoint_tracker[current_ind_counter] = current_visit

        current_ind_counter += 1

        next_node_name = current_node.go(direction)
        next_visit = (next_node_name, step + 1)

        current_path_dict[current_visit] = next_visit
        current_visit = next_visit
        current_node = graph[next_node_name]
        current_node_name = current_node.name

        lead_in_length += int(not in_loop)
        loop_length += int(in_loop)
        if in_loop and current_visit == loop_start:
            break

    lead_in_details = {
        "start": (start_node, 0), 
        "length": lead_in_length, 
        "path": lead_in_path, 
        "endpoints": lead_in_endpoints,
    }
    loop_details = {
        "start": loop_start, 
        "length": loop_length, 
        "path": loop_path,
        "endpoints": loop_endpoints,
    }
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
    shared_lead_in_length = max([
        journey_sum["lead_in"]["length"] for journey_sum in summarised_journeys.values()
    ])
    if y := analyse_shared_lead_in(summarised_journeys, shared_lead_in_length):
        return min(y)
    return 0


def analyse_shared_lead_in(summarised_journeys, shared_lead_in_length):
    shared_lead_in_endpoints = [
        _get_shared_lead_in_endpoints(summarised_journey, shared_lead_in_length)
        for summarised_journey in summarised_journeys.values()
    ]
    return shared_lead_in_endpoints[0].intersection(*shared_lead_in_endpoints)


def _get_shared_lead_in_endpoints(summarised_journey, shared_lead_in_length):
    lead_in_length = summarised_journey["lead_in"]["length"]
    lead_in_endpoints = summarised_journey["lead_in"]["endpoints"]
    endpoint_set = set(lead_in_endpoints.keys())

    loop_length = summarised_journey["loop"]["length"]
    loop_steps_to_do = shared_lead_in_length - lead_in_length
    number_of_loops_to_check = math.ceil(float(loop_steps_to_do) / loop_length)
    loop_endpoints = summarised_journey["loop"]["endpoints"]
    for loop_num in range(number_of_loops_to_check):
        index_offset = lead_in_length + loop_length * loop_num
        endpoints_from_loop = {
            index_offset + loop_ind
            for loop_ind in loop_endpoints.keys()
        }
        endpoint_set.update(endpoints_from_loop)

    return endpoint_set


if __name__ == "__main__":
    args = parser.parse_args()
    answer = haunted_wasteland_2(args.input_name)
    print(answer)
