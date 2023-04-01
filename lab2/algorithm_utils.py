import numpy as np
import copy

def make_random_solution(n):
    nodes = np.arange(n)
    print(len(nodes))
    nodes = np.random.permutation(nodes).tolist()
    half = len(nodes) // 2
    return [nodes[:half], nodes[half:]]

def calc_cycle_length(distance_matrix, cycle):
    cyc_len = 0.0

    for i in range(len(cycle)):
        if i == len(cycle) - 1: cyc_len += distance_matrix[cycle[0]][cycle[-1]]
        else: cyc_len += distance_matrix[cycle[i]][cycle[i + 1]]

    return cyc_len

def calc_cycles_length(distance_matrix, cycles):
    return calc_cycle_length(distance_matrix, cycles[0]) + calc_cycle_length(distance_matrix, cycles[1])

def get_node_pair(cycles, action):
    possibilities = []
    for cycle_idx, cycle in enumerate(cycles):
        # print(cycle_idx)
        for node1 in range(len(cycle)):
            for node2 in range(node1 + 1, len(cycle)):
                possibilities.append(([cycle[node1], cycle[node2]], action, cycle_idx))
    # print(possibilities)
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
    # print(cycle)
    first, second = nodes[0], nodes[1]
    before_first, after_first, before_second, after_second = find_neighbour(cycle, first, second)
    # print(before_first, first, after_first,'|||', before_second,second, after_second)

    if before_second == first:
        return distance_matrix[before_first][second] + distance_matrix[first][after_second] - distance_matrix[before_first][first] - distance_matrix[second][after_second]
    elif after_second == first:
        return distance_matrix[second][after_first] + distance_matrix[first][before_second] - distance_matrix[before_second][second] - distance_matrix[first][after_first]
    else:
        first_delta = distance_matrix[before_second][first] + distance_matrix[first][after_second] - distance_matrix[before_first][first] - distance_matrix[first][after_first]
        second_delta = distance_matrix[before_first][second] + distance_matrix[second][after_first] - distance_matrix[before_second][second] - distance_matrix[second][after_second]
        return first_delta + second_delta
    
def delta_between_cycles_node_exchange(distance_matrix, cycles, nodes):
    first, second = nodes[0], nodes[1]
    # print(first, second, ":::::",cycles)
    before_first, after_first = find_neighbour(cycles[0], first)
    before_second, after_second = find_neighbour(cycles[1], second)
    # print(before_first, first, after_first, "|||", before_second, second, after_second)

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

    return new_cycles

def exchange_edge_in_cycle(cycle, edges):
    new_cycle = copy.deepcopy(cycle)
    first, second = new_cycle.index(edges[0]), new_cycle.index(edges[1])

    if first == 0 and second == len(new_cycle) - 1:
        new_cycle[first], new_cycle[second] = new_cycle[second], new_cycle[first]

    new_cycle[first+1:second+1] = np.flip(new_cycle[first+1:second+1]).tolist()

    return new_cycle

def greedy_one_epoch(cycles, distance_matrix, method):

    possibilities = get_node_pair(cycles, method)
    possibilities.extend(get_between_cycles_node_pair(cycles, delta_between_cycles_node_exchange))

    np.random.seed()
    np.random.shuffle(possibilities)

    for nodes, action, cycle_idx in possibilities:
        if action == delta_inside_cycle_node_exchange:
            delta = delta_inside_cycle_node_exchange(distance_matrix, cycles[cycle_idx], nodes)
        elif action == delta_inside_cycle_edge_exchange:
            delta = delta_inside_cycle_edge_exchange(distance_matrix, cycles[cycle_idx], nodes)
        elif action == delta_between_cycles_node_exchange:
            delta = delta_between_cycles_node_exchange(distance_matrix, cycles, nodes)
        
        if delta < 0:
            if action == delta_inside_cycle_node_exchange or action == delta_inside_cycle_edge_exchange:
                new_cycle = exchange_nodes_in_cycle(cycles[cycle_idx], nodes)
                cycles[cycle_idx] = new_cycle
            elif action == delta_between_cycles_node_exchange:
                new_cycles = exchange_nodes_between_cycles(cycles, nodes)
                cycles = new_cycles
            else:
                ValueError("Fatal error")
            # cycle_length = cycle_length + delta
            break

    return cycles

def steepest_one_epoch(cycles, distance_matrix, method):
    # for cycle_idx1, cycle in enumerate(cycles):
    # cycle_length = calc_cycle_length(distance_matrix, cycle)

    possibilities = get_node_pair(cycles, method)
    possibilities.extend(get_between_cycles_node_pair(cycles, delta_between_cycles_node_exchange))
    
    # np.random.seed()
    # np.random.shuffle(possibilities)
    
    best_delta = 0
    best_cycle_idx = 0
    single_cycle = None
    
    # tmp_cycles = cycles.copy()
    for nodes, action, cycle_idx in possibilities:
        # print(nodes, action, cycle_idx)

        if action == delta_inside_cycle_node_exchange:
            delta = delta_inside_cycle_node_exchange(distance_matrix, cycles[cycle_idx], nodes)
        elif action == delta_inside_cycle_edge_exchange:
            delta = delta_inside_cycle_edge_exchange(distance_matrix, cycles[cycle_idx], nodes)
        elif action == delta_between_cycles_node_exchange:
            delta = delta_between_cycles_node_exchange(distance_matrix, cycles, nodes)
        
        if delta < best_delta:
            best_delta = delta
            
            if action == delta_inside_cycle_node_exchange or action == delta_inside_cycle_edge_exchange:
                new_cycle = exchange_nodes_in_cycle(cycles[cycle_idx], nodes)
                single_cycle = True
                best_cycle_idx = cycle_idx
            elif action == delta_between_cycles_node_exchange:
                new_cycles = exchange_nodes_between_cycles(cycles, nodes)
                single_cycle = False
            else:
                # print("Fatal error")
                ValueError("Fatal error")

            # cycle_length = cycle_length + delta
    # if single_cycle != None:
    #     print("niefajnie")
    if single_cycle == True:
        cycles[best_cycle_idx] = new_cycle
    elif single_cycle == False:
        cycles = new_cycles

    return cycles
    
# def inside_cycle_edge_exchange(cycles, distance_matrix):
#     for cycle_idx, cycle in enumerate(cycles):
#         new_cycle = cycle
#         cycle_length = calc_cycle_length(distance_matrix, cycle)
#         possibilities = get_node_pair(cycle)

#         np.random.seed()
#         np.random.shuffle(possibilities)
#         for nodes in possibilities:
#             delta = delta_inside_cycle_edge_exchange(distance_matrix, cycle, nodes)
#             if delta < 0:
#                 new_cycle = exchange_edge_in_cycle(cycle, nodes)
#                 # print("Exchange for nodes ", nodes)
#                 cycle_length = cycle_length + delta
#                 break

#         cycles[cycle_idx] = new_cycle
#     return cycles

# def between_cycle_node_exchange(cycles, distance_matrix):
#     new_cycles = cycles
#     cycles_length = calc_cycle_length(distance_matrix, cycles[0]) + calc_cycle_length(distance_matrix, cycles[1])
#     possibilities = get_between_cycles_node_pair(cycles)
#     np.random.seed()
#     np.random.shuffle(possibilities)
#     for nodes in possibilities:
#         delta = delta_between_cycles_node_exchange(distance_matrix, cycles, nodes)
#         if delta < 0:
#             new_cycles = exchange_nodes_between_cycles(cycles, nodes)
#             # print("Exchange for nodes ", nodes)
#             cycles_length = cycles_length + delta
#             break

#     return new_cycles