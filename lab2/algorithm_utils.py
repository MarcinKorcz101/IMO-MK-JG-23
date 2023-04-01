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

def get_node_pair(cycle):
    possibilities = []
    for node1 in range(len(cycle)):
        for node2 in range(node1 + 1, len(cycle)):
            possibilities.append([node1, node2])
    return possibilities

def get_between_cycles_node_pair(cycles):
    possibilities = []
    for node1 in range(len(cycles[0])):
        for node2 in range(len(cycles[1])):
            possibilities.append([node1, node2])
    return possibilities

def find_neighbour(cycle, first, second):
    for i in range(1, cycle):
        if cycle[i + 1] == first:
            before_first_neighbour = cycle[i]
        elif cycle[i - 1] == cycle[0]:
            after_first_neighbour = cycle[i]
        
        if cycle[i + 1] == second:
            before_second_neighbour = cycle[i]
        elif cycle[i - 1] == cycle[1]:
            after_second_neighbour = cycle[i]

    return before_first_neighbour, after_first_neighbour, before_second_neighbour, after_second_neighbour

def delta_inside_cycle_node_exchange(distance_matrix, cycle, nodes):
    first, second = nodes[0], nodes[1]
    before_first, after_first, before_second, after_second = find_neighbour(cycle, first, second)

    if before_second == first:
        return distance_matrix[before_first, second] + distance_matrix[first, after_second] - distance_matrix[before_first, first] - distance_matrix[second, after_second]
    elif after_second == first:
        return distance_matrix[second][after_first] + distance_matrix[first][before_second] - distance_matrix[before_second][second] - distance_matrix[first][after_first]
    else:
        first_delta = distance_matrix[before_second][first] + distance_matrix[first][after_second] - distance_matrix[before_first][first] - distance_matrix[first][after_first]
        second_delta = distance_matrix[before_first][second] + distance_matrix[second][after_first] - distance_matrix[before_second][second] - distance_matrix[second][after_second]
        return first_delta + second_delta
    
def delta_between_cycle_node_exchange(distance_matrix, cycle, nodes):
    first, second = nodes[0], nodes[1]
    before_first, after_first, before_second, after_second = find_neighbour(cycle, first, second)

    first_delta = distance_matrix[before_second][first] + distance_matrix[first][after_second] - distance_matrix[before_first][first] - distance_matrix[first][after_first]
    second_delta = distance_matrix[before_first][second] + distance_matrix[second][after_first] - distance_matrix[before_second][second] - distance_matrix[second][after_second]
    return first_delta + second_delta
    
def delta_inside_cycle_edge_exchange(distance_matrix, cycle, nodes):
    first, second = nodes[0], nodes[1]
    _, after_first, _, after_second = find_neighbour(cycle, first, second)
    return distance_matrix[first, second] + distance_matrix[after_first, after_second] - distance_matrix[first, after_first] - distance_matrix[second, after_second]
    
def exchange_nodes_in_cycle(cycle, nodes):
    first, second = nodes[0], nodes[1]
    tmp = first
    first = second
    second = tmp
    return cycle

def exchange_nodes_between_cycles(cycles, nodes):
    first, second = nodes[0], nodes[1]
    temp = cycles[0][first]
    cycles[0][first] = cycles[1][second]
    cycles[1][second] = temp
    return cycles

def exchange_edge_in_cycle(cycle, edges):
    first, second = edges[0], edges[1]

    if first == 0 and second == len(cycle) - 1:
        temp = cycle[first]
        cycle[first] = cycle[second]
        cycle[second] = temp

    cycle[first:second + 1] = reversed(cycle[first:second + 1]) # np.flip()
    return cycle

def inside_cycle_node_exchange(cycles, distance_matrix):
    for cycle in cycles:
        cycle_length = calc_cycle_length(distance_matrix, cycle)
        possibilities = get_node_pair(cycle)
        np.random.seed()
        np.random.shuffle(possibilities)
        for nodes in possibilities:
            delta = delta_inside_cycle_node_exchange(distance_matrix, cycle, nodes)
            if delta < 0:
                new_cycle = exchange_nodes_in_cycle(cycle, nodes)
                cycle_length = cycle_length + delta
                break

        cycles[cycle] = new_cycle
    return cycles
        
def inside_cycle_edge_exchange(cycles, distance_matrix):
    for cycle in cycles:
        new_cycle = cycle
        cycle_length = calc_cycle_length(distance_matrix, cycle)
        possibilities = get_node_pair(cycle)
        np.random.seed()
        np.random.shuffle(possibilities)
        for nodes in possibilities:
            delta = delta_inside_cycle_edge_exchange(distance_matrix, cycle, nodes)
            if delta < 0:
                new_cycle = exchange_edge_in_cycle(cycle, nodes)
                cycle_length = cycle_length + delta
                break

        cycles[cycle] = new_cycle
    return cycles

def between_cycle_node_exchange(cycles, distance_matrix):
    new_cycles = cycles
    cycles_length = calc_cycle_length(distance_matrix, cycles[0]) + calc_cycle_length(distance_matrix, cycles[1])
    possibilities = get_node_pair(cycles)
    np.random.seed()
    np.random.shuffle(possibilities)
    for nodes in possibilities:
        delta = delta_inside_cycle_edge_exchange(distance_matrix, cycles, nodes)
        if delta < 0:
            new_cycles = exchange_nodes_between_cycles(cycles, nodes)
            cycles_length = cycles_length + delta
            break

    return new_cycles