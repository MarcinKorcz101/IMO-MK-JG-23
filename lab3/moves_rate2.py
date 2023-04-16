from algorithm_utils import *

def get_edge_possibility(cycles, distance_matrix):
    possibilities = []
    for cycle_idx, cycle in enumerate(cycles):
        for node1 in range(len(cycle)):
            for node2 in range(node1 + 1, len(cycle)):
                delta = delta_inside_cycle_edge_exchange(cycle, distance_matrix, node1, node2)
                if delta < 0:
                    b1, a1, b2, a2 = find_neighbour(cycle, node1, node2)
                    possibilities.append(([cycle[node1], cycle[node2]], delta_inside_cycle_edge_exchange, cycle_idx, delta, [b1,a1,b2,a2]))
    return possibilities


def get_between_cycles_possibility(cycles, distance_matrix):
    possibilities = []
    for node1 in range(len(cycles[0])):
        before_first, after_first = find_neighbour(cycles[0], node1)
        for node2 in range(len(cycles[1])):
            before_second, after_second = find_neighbour(cycles[1], node2)
            delta = delta_inside_cycle_edge_exchange(cycles, distance_matrix, node1, node2)
            if delta < 0:
                possibilities.append(([cycles[0][node1], cycles[1][node2]], delta_inside_cycle_edge_exchange, None, delta, [before_first, after_first, before_second, after_second]))
    return possibilities

def init_moves(cycles, distance_matrix):
    possibilities = get_edge_possibility(cycles, distance_matrix)
    possibilities.extend(get_between_cycles_possibility(cycles, distance_matrix))
    return possibilities.sort(key = lambda x: x[3])

def check_if_edge_exists(cycle, node1, node2):
    for i in range(len(cycle)):
        if cycle[i] == node1 and cycle[(i + 1) % len(cycle)] == node2:
            return True
    return False


def moves_rate(cycles, distance_matrix):
    possibilities = init_moves(cycles, distance_matrix)
    while True:
        new_move = None
            
        to_remove = []
        if len(possibilities) == 0: break
        for move_id, move in enumerate(possibilities):
            nodes, action, cycle_idx, delta, neighbours = move
            if action == delta_inside_cycle_edge_exchange:
                _, a0 = find_neighbour(cycles[cycle_idx], nodes[0])
                _, a1 = find_neighbour(cycles[cycle_idx], nodes[1])
                if a0 != neighbours[1] or a1 != neighbours[3]:
                    to_remove.append(move_id)
                    continue