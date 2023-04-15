# Ocena ruchów z poprzednich iteracji
from algorithm_utils import get_node_pair, get_between_cycles_node_pair, delta_between_cycles_node_exchange, delta_inside_cycle_edge_exchange, exchange_edge_in_cycle, exchange_nodes_between_cycles

def get_node_pair_delta(cycles, distance_matrix):
    possibilities = []
    for cycle_idx, cycle in enumerate(cycles):
        for node1 in range(len(cycle)):
            for node2 in range(node1 + 1, len(cycle)):
                delta = delta_inside_cycle_edge_exchange(distance_matrix, cycles[cycle_idx], [cycle[node1], cycle[node2]])
                if delta > 0: possibilities.append(([cycle[node1], cycle[node2]], delta_inside_cycle_edge_exchange, cycle_idx, delta))
    return possibilities

def get_between_cycles_node_pair_delta(cycles, distance_matrix):
    possibilities = []
    for node1 in range(len(cycles[0])):
        for node2 in range(len(cycles[1])):
            delta = delta_between_cycles_node_exchange(distance_matrix, cycles, [cycles[0][node1], cycles[1][node2]])
            if delta > 0: possibilities.append(([cycles[0][node1], cycles[1][node2]], delta_between_cycles_node_exchange, None, delta))
    return possibilities

def moves_rate_one_epoch(cycles, distance_matrix):
    while True:
        single_cycle = None
        best_cycle_idx = 0
        possibilities = get_node_pair_delta(cycles, distance_matrix)
        possibilities.extend(get_between_cycles_node_pair_delta(cycles, distance_matrix))
        if len(possibilities) == 0: break
        min_possibility = min(possibilities, key = lambda x: x[3])
        nodes, action, cycle_idx, _ = min_possibility
        if action == delta_inside_cycle_edge_exchange:
            if nodes[0] not in cycles[cycle_idx] and nodes[1] not in cycles[cycle_idx]:
                possibilities.remove(possibilities.index(min_possibility))
            elif nodes[0] in cycles[cycle_idx] and nodes[1] in cycles[cycle_idx]:
                new_cycle = exchange_edge_in_cycle(cycles[cycle_idx], nodes)
                single_cycle = True
                best_cycle_idx = cycle_idx
                possibilities.remove(possibilities.index(min_possibility))
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