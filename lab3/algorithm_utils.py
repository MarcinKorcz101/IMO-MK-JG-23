import numpy as np
import copy

def make_random_solution(n):
    nodes = np.arange(n)
    # print(len(nodes))
    nodes = np.random.permutation(nodes).tolist()
    half = len(nodes) // 2
    return [nodes[:half], nodes[half:]]

def calc_cycle_length(distance_matrix, cycle):
    cyc_len = 0.0

    for i in range(len(cycle)):
        if i == len(cycle) - 1: 
            cyc_len += distance_matrix[cycle[0]][cycle[-1]]
        else: 
            cyc_len += distance_matrix[cycle[i]][cycle[i + 1]]

    return cyc_len

def calc_cycles_length(distance_matrix, cycles):
    return calc_cycle_length(distance_matrix, cycles[0]) + calc_cycle_length(distance_matrix, cycles[1])

def get_node_pair(cycles, action):
    possibilities = []
    for cycle_idx, cycle in enumerate(cycles):
        for node1 in range(len(cycle)):
            for node2 in range(node1 + 1, len(cycle)):
                possibilities.append(([cycle[node1], cycle[node2]], action, cycle_idx))
    
    return possibilities

def get_between_cycles_node_pair(cycles, action):
    possibilities = []
    for node1 in range(len(cycles[0])):
        for node2 in range(len(cycles[1])):
            possibilities.append(([cycles[0][node1], cycles[1][node2]], action, None))
    return possibilities

def find_neighbour(cycle, first, second=None):
    first_idx = cycle.index(first)
    before_first_neighbour = cycle[first_idx - 1]
    after_first_neighbour = cycle[(first_idx + 1) % len(cycle)]

    if second != None:
        second_idx = cycle.index(second)
        before_second_neighbour = cycle[second_idx - 1]
        after_second_neighbour = cycle[(second_idx + 1) % len(cycle)]
        return before_first_neighbour, after_first_neighbour, before_second_neighbour, after_second_neighbour
    return before_first_neighbour, after_first_neighbour

def delta_inside_cycle_node_exchange(distance_matrix, cycle, nodes):
    first, second = nodes[0], nodes[1]
    before_first, after_first, before_second, after_second = find_neighbour(cycle, first, second)

    if before_second == first:
        return distance_matrix[before_first][second] + distance_matrix[first][after_second] - distance_matrix[before_first][first] - distance_matrix[second][after_second]
    elif after_second == first:
        return distance_matrix[second][after_first] + distance_matrix[first][before_second] - distance_matrix[before_second][second] - distance_matrix[first][after_first]
    else:
        first_delta = distance_matrix[before_second][first] + distance_matrix[first][after_second] - distance_matrix[before_first][first] - distance_matrix[first][after_first]
        second_delta = distance_matrix[before_first][second] + distance_matrix[second][after_first] - distance_matrix[before_second][second] - distance_matrix[second][after_second]
        return first_delta + second_delta


def find_cycle_idx(cycles, node):
    for i in range(len(cycles)):
        if node in cycles[i]:
            return i
    return None

def delta_between_cycles_node_exchange(distance_matrix, cycles, nodes):
    first, second = nodes[0], nodes[1]
    first_cycle_idx = find_cycle_idx(cycles, first)
    second_cycle_idx = find_cycle_idx(cycles, second)
    

    before_first, after_first = find_neighbour(cycles[first_cycle_idx], first)
    before_second, after_second = find_neighbour(cycles[second_cycle_idx], second)

    first_delta = distance_matrix[before_second][first] + distance_matrix[first][after_second] - distance_matrix[before_first][first] - distance_matrix[first][after_first]
    second_delta = distance_matrix[before_first][second] + distance_matrix[second][after_first] - distance_matrix[before_second][second] - distance_matrix[second][after_second]
    return first_delta + second_delta
    
def delta_inside_cycle_edge_exchange(distance_matrix, cycle, nodes):
    first, second = nodes[0], nodes[1]
    _, after_first, _, after_second = find_neighbour(cycle, first, second)
    return distance_matrix[first][second] + distance_matrix[after_first][after_second] - distance_matrix[first][after_first] - distance_matrix[second][after_second]
    
def exchange_nodes_in_cycle(cycle, nodes):
    new_cycles = copy.deepcopy(cycle)
    first, second = new_cycles.index(nodes[0]), new_cycles.index(nodes[1])
    new_cycles[first], new_cycles[second] = new_cycles[second], new_cycles[first]
    
    return new_cycles

def exchange_nodes_between_cycles(cycles, nodes):
    new_cycles = copy.deepcopy(cycles)
    
    first, second = new_cycles[0].index(nodes[0]), new_cycles[1].index(nodes[1])
    new_cycles[0][first], new_cycles[1][second] = new_cycles[1][second], new_cycles[0][first]
    # print("done ")

    return new_cycles

def exchange_edge_in_cycle(cycle, edges):
    new_cycle = copy.deepcopy(cycle)
    first, second = new_cycle.index(edges[0]), new_cycle.index(edges[1])

    if first > second:
        first, second = second, first

    if first == 0 and second == len(new_cycle) - 1:
        new_cycle[first], new_cycle[second] = new_cycle[second], new_cycle[first]

    new_cycle[first+1:second+1] = np.flip(new_cycle[first+1:second+1]).tolist()

    return new_cycle


def steepest_one_epoch(cycles, distance_matrix, method):
    possibilities = get_node_pair(cycles, method)
    possibilities.extend(get_between_cycles_node_pair(cycles, delta_between_cycles_node_exchange))
    
    best_delta = 0
    best_cycle_idx = 0
    single_cycle = None
    
    for nodes, action, cycle_idx in possibilities:
        if action == delta_inside_cycle_node_exchange:
            delta = delta_inside_cycle_node_exchange(distance_matrix, cycles[cycle_idx], nodes)
        elif action == delta_inside_cycle_edge_exchange:
            delta = delta_inside_cycle_edge_exchange(distance_matrix, cycles[cycle_idx], nodes)
        elif action == delta_between_cycles_node_exchange:
            delta = delta_between_cycles_node_exchange(distance_matrix, cycles, nodes)
        
        if delta < best_delta:
            best_delta = delta
            if action == delta_inside_cycle_node_exchange:
                new_cycle = exchange_nodes_in_cycle(cycles[cycle_idx], nodes)
                single_cycle = True
                best_cycle_idx = cycle_idx
            elif action == delta_inside_cycle_edge_exchange:
                new_cycle = exchange_edge_in_cycle(cycles[cycle_idx], nodes)
                single_cycle = True
                best_cycle_idx = cycle_idx
            elif action == delta_between_cycles_node_exchange:
                new_cycles = exchange_nodes_between_cycles(cycles, nodes)
                single_cycle = False
            else:
                ValueError("Fatal error")

    if single_cycle == True:
        cycles[best_cycle_idx] = new_cycle
    elif single_cycle == False:
        cycles = new_cycles

    return cycles

