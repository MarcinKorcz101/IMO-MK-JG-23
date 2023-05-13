import numpy as np
import sys
import copy
# from ..lab3.algorithm_utils import delta_between_cycles_node_exchange, exchange_nodes_between_cycles

def exchange_edge_in_cycle2(cycle, nodes, change_type="after"):
    i, j = nodes[0], nodes[1]
    i_index = cycle.index(i)
    j_index = cycle.index(j)

    if i_index > j_index:
        i_index, j_index = j_index, i_index

    if change_type == "after":
        reversed = cycle[i_index + 1 : j_index + 1]
        reversed.reverse()
        cycle[i_index + 1 : j_index + 1] = reversed
    elif change_type == "before":
        reversed = cycle[i_index : j_index]
        reversed.reverse()
        cycle[i_index : j_index] = reversed
    return cycle

def delta_inside_cycle_edge_exchange2(distance_matrix, cycle, nodes, change_type="after"):
    i, j = nodes[0], nodes[1]
    i_index, j_index = cycle.index(i), cycle.index(j)

    if change_type == "after":
        next_i = cycle[(i_index + 1) % len(cycle)]
        next_j = cycle[(j_index + 1) % len(cycle)]
    else:
        next_i = cycle[i_index - 1]
        next_j = cycle[j_index - 1]

    return (
        distance_matrix[i][j]
        + distance_matrix[next_i][next_j]
        - distance_matrix[i][next_i]
        - distance_matrix[j][next_j]
    )


def delta_between_cycles_node_exchange(distance_matrix, cycles, nodes):
    first, second = nodes[0], nodes[1]
    first_cycle_idx = find_cycle_idx(cycles, first)
    second_cycle_idx = find_cycle_idx(cycles, second)
    

    before_first, after_first = find_neighbour(cycles[first_cycle_idx], first)
    before_second, after_second = find_neighbour(cycles[second_cycle_idx], second)

    first_delta = distance_matrix[before_second][first] + distance_matrix[first][after_second] - distance_matrix[before_first][first] - distance_matrix[first][after_first]
    second_delta = distance_matrix[before_first][second] + distance_matrix[second][after_first] - distance_matrix[before_second][second] - distance_matrix[second][after_second]
    return first_delta + second_delta

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

def exchange_nodes_between_cycles(cycles, nodes):
    new_cycles = copy.deepcopy(cycles)
    
    first, second = new_cycles[0].index(nodes[0]), new_cycles[1].index(nodes[1])
    new_cycles[0][first], new_cycles[1][second] = new_cycles[1][second], new_cycles[0][first]

    return new_cycles



def find_candidates(distance_matrix, k):
    candidates = []
    for i in range(len(distance_matrix)):
        candidates.append([])
        for j in range(len(distance_matrix)):
            if i != j:
                candidates[i].append((distance_matrix[i][j], j))
        candidates[i].sort()
        candidates[i] = [x[1] for x in candidates[i][:k]]
    return candidates

def find_cycle_idx(cycles, node):
    for i in range(len(cycles)):
        if node in cycles[i]:
            return i
    return None


def candidates_moves_reworked(cycles, distance_matrix, K=10):

    candidates_list = find_candidates(distance_matrix, K)
    while True:
        best_delta = 0
        best_move = None
        for a in range(len(distance_matrix)):
            a_cycle_idx = find_cycle_idx(cycles, a)
            # print(a, candidates_list[a])
            for b in candidates_list[a]:
                b_cycle_idx = find_cycle_idx(cycles, b)
                if b in cycles[1]:
                    b_cycle_idx = 1
                if a_cycle_idx == b_cycle_idx:
                    direction = "after"
                    delta = delta_inside_cycle_edge_exchange2(distance_matrix, cycles[a_cycle_idx], [a, b], direction)
                    delta_tmp = delta_inside_cycle_edge_exchange2(distance_matrix, cycles[a_cycle_idx], [a, b], 'before')
                    if delta_tmp < delta:
                        delta = delta_tmp
                        direction = 'before'
                    if delta < best_delta:
                        best_delta = delta
                        best_move = (a, b, a_cycle_idx, delta_inside_cycle_edge_exchange2, direction)
                else:
                    if a_cycle_idx == 0:
                        first = a
                        second = b
                    else:
                        first = b
                        second = a
                    
                    delta = delta_between_cycles_node_exchange(distance_matrix, cycles, [first, second])
                    
                    if delta < best_delta:
                        best_delta = delta
                        best_move = (a, b, None, delta_between_cycles_node_exchange, None)
        if best_move == None:
            break

        a, b, cycle_idx, action, direction = best_move

        if action == delta_inside_cycle_edge_exchange2:
            new_cycle = exchange_edge_in_cycle2(cycles[cycle_idx], [a, b], direction)
            cycles[cycle_idx] = new_cycle
        elif action == delta_between_cycles_node_exchange:
            if find_cycle_idx(cycles, a) == 0:
                first = a
                second = b
            else:
                first = b
                second = a
            new_cycles = exchange_nodes_between_cycles(cycles, [first, second])
            cycles = new_cycles
    
    return cycles
    