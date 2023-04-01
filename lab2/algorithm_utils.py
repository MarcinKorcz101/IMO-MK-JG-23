import numpy as np

def make_random_solution(nodes):
    nodes = np.random.permutation(nodes)
    half = len(nodes) // 2
    return nodes[:half], nodes[half:]

def calc_cycle_length(distance_matrix, cycle):
    cyc_len = 0.0

    for i in range(len(cycle)):
        if i == len(cycle) - 1: cyc_len += distance_matrix[cycle[0]][cycle[-1]]
        else: cyc_len += distance_matrix[cycle[i]][cycle[i + 1]]

    return cyc_len

def get_node_pair(cycle, action):
    possibilities = []
    for node1 in range(len(cycle)):
        for node2 in range(node1 + 1, len(cycle)):
            possibilities.append(([cycle[node1], cycle[node2]], action))
    return possibilities

def get_between_cycles_node_pair(cycles, action):
    possibilities = []
    for node1 in range(len(cycles[0])):
        for node2 in range(len(cycles[1])):
            possibilities.append(([cycles[0][node1], cycles[1][node2]], action))
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
    before_first, after_first = find_neighbour(cycles[0], first)
    before_second, after_second = find_neighbour(cycles[1], second)
    print(before_first, first, after_first, "|||", before_second, second, after_second)

    first_delta = distance_matrix[before_second][first] + distance_matrix[first][after_second] - distance_matrix[before_first][first] - distance_matrix[first][after_first]
    second_delta = distance_matrix[before_first][second] + distance_matrix[second][after_first] - distance_matrix[before_second][second] - distance_matrix[second][after_second]
    return first_delta + second_delta
    
def delta_inside_cycle_edge_exchange(distance_matrix, cycle, nodes):
    first, second = nodes[0], nodes[1]
    _, after_first, _, after_second = find_neighbour(cycle, first, second)
    return distance_matrix[first][second] + distance_matrix[after_first][after_second] - distance_matrix[first][after_first] - distance_matrix[second][after_second]
    
def exchange_nodes_in_cycle(cycle, nodes):
    first, second = cycle.index(nodes[0]), cycle.index(nodes[1])
    cycle[first], cycle[second] = cycle[second], cycle[first]
    
    return cycle

def exchange_nodes_between_cycles(cycles, nodes):
    first, second = cycles[0].index(nodes[0]), cycles[1].index(nodes[1])
    cycles[0][first], cycles[1][second] = cycles[1][second], cycles[0][first]

    return cycles

def exchange_edge_in_cycle(cycle, edges):
    first, second = cycle.index(edges[0]), cycle.index(edges[1])

    if first == 0 and second == len(cycle) - 1:
        cycle[first], cycle[second] = cycle[second], cycle[first]

    cycle[first+1:second+1] = np.flip(cycle[first+1:second+1]).tolist()

    return cycle

def greedy_one_epoch(cycles, distance_matrix, method):
    for cycle_idx, cycle in enumerate(cycles):
        cycle_length = calc_cycle_length(distance_matrix, cycle)

        possibilities = get_node_pair(cycle, method)
        possibilities.extend(get_between_cycles_node_pair(cycles, delta_between_cycles_node_exchange))

        np.random.seed()
        np.random.shuffle(possibilities)

        for nodes, action in possibilities:
            if action == delta_inside_cycle_node_exchange:
                delta = delta_inside_cycle_node_exchange(distance_matrix, cycle, nodes)
            elif action == delta_between_cycles_node_exchange:
                delta = delta_between_cycles_node_exchange(distance_matrix, cycles, nodes)


            if delta < 0:
                if action == delta_inside_cycle_node_exchange:
                    new_cycle = exchange_nodes_in_cycle(cycle, nodes)
                elif action == delta_between_cycles_node_exchange:
                    new_cycle = exchange_nodes_between_cycles(cycles, nodes)
                else:
                    print("Fatal error")
                cycle_length = cycle_length + delta
                break

        cycles[cycle_idx] = new_cycle
    return cycles

def steepest_one_epoch(cycles, distance_matrix, method):
    for cycle_idx, cycle in enumerate(cycles):
        cycle_length = calc_cycle_length(distance_matrix, cycle)

        possibilities = get_node_pair(cycle, method)
        possibilities.extend(get_between_cycles_node_pair(cycle, delta_between_cycles_node_exchange))

        np.random.seed()
        np.random.shuffle(possibilities)
        
        best_delta = 0
        for nodes, action in possibilities:
            delta = action(distance_matrix, cycle, nodes)
            if delta < best_delta:
                best_delta = delta

                if isinstance(action, delta_inside_cycle_node_exchange):
                    new_cycle = exchange_nodes_in_cycle(cycle, nodes)
                elif isinstance(action, delta_between_cycles_node_exchange):
                    new_cycle = exchange_nodes_between_cycles(cycle, nodes)
                else:
                    print("Fatal error")

                cycle_length = cycle_length + delta

        cycles[cycle_idx] = new_cycle

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